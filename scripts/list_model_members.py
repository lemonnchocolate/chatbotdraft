import tarfile, re
from pathlib import Path
models = list(Path('models').glob('*.tar.gz'))
print('Found models:', [str(m) for m in models])
invalid_chars = re.compile(r'[<>:\"\\|?*]')
for m in models:
    print('\n--', m)
    with tarfile.open(m, 'r:gz') as t:
        members = t.getmembers()
        bad = []
        for mem in members:
            name = mem.name
            if invalid_chars.search(name):
                bad.append(name)
        print('Total members:', len(members))
        if bad:
            print('Members with invalid chars:')
            for b in bad[:200]:
                print(' ', b)
        else:
            print('No invalid chars found in member names')
