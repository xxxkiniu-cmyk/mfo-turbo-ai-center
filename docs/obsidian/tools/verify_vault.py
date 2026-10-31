#!/usr/bin/env python3
"""Weryfikacja przenośnej mapy, bez uruchamiania usług i bez dostępu do sieci."""
from pathlib import Path
import json,re,subprocess,sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
notes=[p for p in root.rglob('*.md') if not any(x in p.relative_to(root).parts for x in ['Dowody','.git','.obsidian'])]
names={p.stem for p in notes};broken=[];edges=[];status_errors=[]
for p in notes:
 s=p.read_text(encoding='utf-8-sig')
 for t in re.findall(r'\[\[([^\]|#]+)',s):
  edges.append((p.stem,t))
  if t not in names:broken.append([str(p.relative_to(root)),t])
 if p.parent.name=='Moduly':
  m=re.search(r'^status: "([^"]+)"',s,re.M)
  if not m or m.group(1) not in ['DZIAŁA','NIE DZIAŁA','NIEZWERYFIKOWANY','PLANOWANY']:status_errors.append(p.name)
modules=list((root/'Moduly').glob('*.md'))
module_names={p.stem for p in modules}
me=[e for e in edges if e[0] in module_names and e[1] in module_names]
forbidden=[];suspect=[]
try:files=subprocess.check_output(['git','-C',str(root),'ls-files','-z'],text=True).split('\0')
except subprocess.CalledProcessError:files=[]
patterns=[r'gh[pousr]_[A-Za-z0-9]{25,}',r'github_pat_[A-Za-z0-9_]{30,}',r'sk-[A-Za-z0-9_-]{25,}',r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',r'(?i)(?:api[_-]?key|access[_-]?token|password)\s*[=:]\s*[\"\x27][^\"\x27\s]{12,}[\"\x27]']
for name in filter(None,files):
 p=root/name
 if name.startswith(('Dowody/','private/','backups/')) or p.name.startswith('.env') or p.suffix.lower() in ['.gguf','.exe','.pem','.key'] or 'workspace' in p.name:forbidden.append(name)
 if not p.is_file():continue
 s=p.read_text(errors='replace')
 # Własne wyrażenia skanera są wzorcami, a nie danymi uwierzytelniającymi.
 if p.resolve()!=Path(__file__).resolve() and any(re.search(x,s) for x in patterns):suspect.append(name)
r={'moduly':len(modules),'odsylacze_modulow':len(me),'unikalne_polaczenia_modulow':len({tuple(sorted(x)) for x in me}),'odsylacze_wszystkich_notatek':len(edges),'bledne_linki':broken,'bledne_statusy':status_errors,'zabronione_pliki':forbidden,'podejrzane_pliki':suspect,'sprawdzone_pliki_git':len(list(filter(None,files)))}
print(json.dumps(r,ensure_ascii=False,indent=2))
if len(modules)!=30 or broken or status_errors or forbidden or suspect:sys.exit(2)
