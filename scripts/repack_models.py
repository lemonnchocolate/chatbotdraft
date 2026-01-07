import tarfile
from pathlib import Path

for d in Path('models').glob('*.tar_dir'):
    out = d.with_suffix('.repack.tar.gz')
    print('Repacking', d, '->', out)
    with tarfile.open(out, 'w:gz') as t:
        for p in d.rglob('*'):
            arcname = str(p.relative_to(d)).replace('\\','/')
            t.add(p, arcname=arcname)
print('Done')
