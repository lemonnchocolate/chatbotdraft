import tarfile, tempfile
from pathlib import Path

models = list(Path('models').glob('*.tar.gz'))
for m in models:
    print('\n==', m)
    tempdir = tempfile.mkdtemp(prefix='rasa_extr_')
    print('Tempdir:', tempdir)
    with tarfile.open(m, 'r:gz') as t:
        for mem in t.getmembers():
            try:
                t.extract(mem, path=tempdir)
            except Exception as e:
                print('Failed on member:', repr(mem.name))
                print('Error:', type(e), e)
                raise
    print('Extracted all members successfully to', tempdir)
print('\nDone')
