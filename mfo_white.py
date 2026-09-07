#!/usr/bin/env python3
"""Jeden zapis Python przez JCODE, kontrola i jedna proba poprawy."""
import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import re
import traceback


def generate(target, task, timeout=600):
    prefix = 'to=functions.write {"content":'
    suffix = ',"file_path":' + json.dumps(str(target)) + ',"intent":'
    grammar = (
        'root ::= ' + json.dumps(prefix) + ' string ' +
        json.dumps(suffix) + ' string "}"\n' +
        r'string ::= "\"" ([^"\\\x00-\x1F] | "\\" (["\\/bfnrt] | "u" [0-9a-fA-F]{4}))* "\""' + '\n'
    )
    env = os.environ.copy()
    env["JCODE_OPENAI_EXTRA_BODY"] = json.dumps({
        "tool_choice": "none",
        "grammar": grammar,
        "max_tokens": 1024,
        "temperature": 0
    })
    env["JCODE_RUN_AUTO_POKE"] = "0"
    model = Path.home() / "mfo-models/Qwen2.5-Coder-3B-Instruct-Q4_K_M.gguf"
    if not model.is_file() or not shutil.which("jcode"):
        raise RuntimeError("Brak pliku modelu lub komendy jcode.")

    message = (
        f"Zapisz kompletny plik {target} narzedziem write. "
        "Content ma zawierac tylko poprawny kod Python, bez >> i bez markdown. "
        "Odpowiedz: to=functions.write oraz JSON z content, file_path, intent.\n"
        + task
    )
    cmd = [
        "jcode", "--no-update", "--provider-profile", "local_llama",
        "--tool-profile", "lite", "--tools", "write",
        "--model", str(model), "--trace", "run", message
    ]
    proc = subprocess.Popen(
        cmd, env=env, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, encoding="utf-8", errors="replace", bufsize=1
    )
    expired = threading.Event()

    def expire():
        expired.set()
        proc.kill()

    timer = threading.Timer(timeout, expire)
    timer.daemon = True
    timer.start()
    grace, done = None, False
    try:
        for line in proc.stdout:
            print(line, end="", flush=True)
            if not done and line.startswith("[trace] tool_exec_done name=write id="):
                done = True
                proc.send_signal(signal.SIGINT)
                grace = threading.Timer(5, proc.kill)
                grace.daemon = True
                grace.start()
        proc.wait()
    finally:
        timer.cancel()
        if grace:
            grace.cancel()
        if proc.poll() is None:
            proc.kill()
            proc.wait()
        proc.stdout.close()

    if expired.is_set():
        raise RuntimeError(f"Limit czasu JCODE: {timeout:g} s.")
    if not done or not target.is_file():
        raise RuntimeError("Brak potwierdzonego zapisu write.")
    print("JCODE_WRITE_DONE — kontrolowane zatrzymanie po write.", flush=True)


def normalize(raw):
    lines, changes = raw.splitlines(keepends=True), []
    indices = [i for i, line in enumerate(lines) if line.strip()]
    if len(indices) >= 2:
        first, last = indices[0], indices[-1]
        if (lines[first].strip().lower() in ("```", "```python", "```py")
                and lines[last].strip() == "```"):
            lines = lines[first + 1:last]
            changes.append("usunieto otaczajacy blok Markdown")
    for i, line in enumerate(lines):
        if line.strip():
            stripped = line.lstrip()
            leading_ws = line[:len(line) - len(stripped)]
            match = re.match(r"^>+\s*", stripped)
            if match:
                lines[i] = leading_ws + stripped[match.end():]
                changes.append("usunieto poczatkowy znacznik: " + repr(match.group(0)))
            break
    return "".join(lines), changes


def run_program(target, expected):
    with tempfile.TemporaryFile() as output:
        try:
            result = subprocess.run(
                [sys.executable, str(target)], cwd=target.parent,
                stdin=subprocess.DEVNULL, stdout=output,
                stderr=subprocess.STDOUT, timeout=15
            )
        except subprocess.TimeoutExpired:
            return "Program przekroczyl limit wykonania 15 s."
        size = output.seek(0, 2)
        output.seek(max(0, size - 8000))
        text = output.read(8000).decode("utf-8", errors="replace")
    print(text, end="" if text.endswith("\n") else "\n", flush=True)
    if result.returncode != 0:
        return f"Program zakonczyl sie kodem {result.returncode}:\n{text}"
    if expected and expected not in [line.strip() for line in text.splitlines()]:
        return f"Brak wymaganego wiersza wyjscia: {expected!r}.\n{text}"
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true",
                        help="Uruchom wygenerowany program; limit 15 s.")
    parser.add_argument("--expect", help="Wymagany wiersz wyjscia; wymaga --run.")
    parser.add_argument("file", help="Sciezka NOWEGO pliku .py.")
    parser.add_argument("task", help="Opis programu do napisania.")
    args = parser.parse_args()
    target = Path(args.file).expanduser()
    if target.exists() or target.is_symlink():
        parser.error("Plik juz istnieje. Wybierz nowa nazwe.")
    if target.suffix.lower() != ".py":
        parser.error("Ten pomocnik obsluguje pliki .py.")
    if args.expect and not args.run:
        parser.error("--expect wymaga --run.")
    target = target.resolve()
    request = args.task
    if args.expect:
        request += f"\nPo poprawnym wykonaniu zadania wypisz: print({args.expect!r})."
    original = request

    for attempt in (1, 2):
        print(f"\nMFO WRITE — proba {attempt}/2: {target}", flush=True)
        generate(target, request)
        raw = target.read_text(encoding="utf-8")
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", delete=False,
                dir=target.parent, prefix=target.name + ".mfo-raw-",
                suffix=".txt") as backup:
            backup.write(raw)
        print("SUROWY_KOD:", backup.name, flush=True)

        code, changes = normalize(raw)
        error = None
        try:
            if not code.strip():
                raise ValueError("Model zapisal pusty kod.")
            compile(code, str(target), "exec")
        except (SyntaxError, ValueError) as exc:
            error = "".join(traceback.format_exception_only(type(exc), exc))

        if error is None:
            if changes:
                target.write_text(code, encoding="utf-8")
                print("KOREKTA_POMOCNIKA:", "; ".join(changes), flush=True)
            else:
                print("KOD_MODELU_BEZ_KOREKT", flush=True)
            print("MFO_SYNTAX_OK", flush=True)
            if args.run:
                error = run_program(target, args.expect)

        if error is None:
            if args.run:
                print("MFO_RUN_OK", flush=True)
            print("MFO_WRITE_OK:", target, flush=True)
            return 0

        print("MFO_CHECK_FAIL:", error, flush=True)
        if attempt == 1:
            request = (
                original +
                "\nPopraw ponizszy kod po bledzie. Zapisz caly plik ponownie.\n"
                "KOD:\n" + code[:6500] + "\nBLAD:\n" + error[-2000:]
            )

    print("MFO_WRITE_FAIL — kod nie przeszedl kontroli po 2 probach.", flush=True)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (Exception, KeyboardInterrupt) as exc:
        print("\nMFO_WRITE_FAIL:", type(exc).__name__, str(exc), file=sys.stderr)
        sys.exit(1)
