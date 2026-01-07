import tarfile
from pathlib import Path

for m in Path('models').glob('*.tar.gz'):
    dest = Path('models') / (m.stem + '_dir')
    dest.mkdir(parents=True, exist_ok=True)
    print('Extracting', m, 'to', dest)
    with tarfile.open(m, 'r:gz') as t:
        t.extractall(path=str(dest))
print('Done')
