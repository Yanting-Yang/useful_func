import tarfile
import os

from tqdm import tqdm

from .format import size_fmt


def tar(src: str, dst: str = './') -> None:
    basename = os.path.basename(src)

    names = list()
    for root, _, files in os.walk(src):
        if files:
            names.extend([os.path.join(root, name) for name in files])
        else:
            names.append(root)

    arcnames = list()
    arcnames = [name.replace(src, basename, 1) for name in names]

    if os.path.isdir(dst):
        dst = os.path.join(dst, f'{basename}.tar.gz')

    with tarfile.open(dst, 'w:gz') as mytar:
        for name, arcname in tqdm(list(zip(names, arcnames))):
            mytar.add(name, arcname, recursive=False)
    tarinfo(dst)


def tarinfo(name: str) -> None:
    archive_size = os.stat(name).st_size

    original_size = 0
    with tarfile.open(name, 'r') as mytar:
        while True:
            member = mytar.next()
            if member is None:
                break
            original_size += member.size

    table = {
        'archive_size': size_fmt(archive_size)[0],
        'archive_unit': size_fmt(archive_size)[1],
        'original_size': size_fmt(original_size)[0],
        'original_unit': size_fmt(original_size)[1]}

    s = 'Archive {archive_size:.1f} {archive_unit}, Original {original_size:.1f} {original_unit}'
    print(s.format(**table))
    print(f'Ratio = {archive_size/original_size:.2%}')
