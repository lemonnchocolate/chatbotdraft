import tarfile
from pathlib import Path

reserved = {"CON","PRN","AUX","NUL"} | {f"COM{i}" for i in range(1,10)} | {f"LPT{i}" for i in range(1,10)}

models = list(Path('models').glob('*.tar.gz'))
for m in models:
    print('\n==', m)
    with tarfile.open(m, 'r:gz') as t:
        members = t.getmembers()
        problems = []
        for mem in members:
            name = mem.name
            # normalize path components
            parts = name.split('/')
            for p in parts:
                if not p:
                    continue
                if p.endswith(' ') or p.endswith('.'):
                    problems.append((name, 'trailing space/dot', p))
                up = p.split('.')[0].upper()
                if up in reserved:
                    problems.append((name, 'reserved name', p))
            if len(name) > 240:
                problems.append((name, 'too long', len(name)))
            # symlink / hardlink check
            if mem.issym() or mem.islnk():
                problems.append((name, 'link', 'symlink_or_hardlink'))
        if problems:
            print('Problems found:')
            for p in problems:
                print(' ', p)
        else:
            print('No problems found (trailing spaces/dots, reserved names, long paths, links)')
print('\nDone')
