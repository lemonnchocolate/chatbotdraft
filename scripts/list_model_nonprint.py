import tarfile
from pathlib import Path

models = list(Path('models').glob('*.tar.gz'))
for m in models:
    print('\n==', m)
    with tarfile.open(m, 'r:gz') as t:
        members = t.getmembers()
        found = []
        for mem in members:
            name = mem.name
            nonprint = [ord(c) for c in name if ord(c) < 32]
            if nonprint:
                found.append((name, nonprint))
        if found:
            print('Members with control chars:')
            for f in found:
                print(' ', repr(f[0]), f[1])
        else:
            print('No control characters found in member names')
print('\nDone')
