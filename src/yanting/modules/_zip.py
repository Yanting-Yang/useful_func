import os
from zipfile import ZipFile, ZIP_DEFLATED

from tqdm import tqdm

from .format import size_fmt


def zip_file(src: str, dst: str = './') -> None:
    basename = os.path.basename(src)

    filenames = list()
    for root, _, files in os.walk(src):
        if files:
            filenames.extend([os.path.join(root, name) for name in files])
        else:
            filenames.append(root)

    arcnames = list()
    arcnames = [name.replace(src, basename, 1) for name in filenames]

    if os.path.isdir(dst):
        dst = os.path.join(dst, f'{basename}.zip')

    with ZipFile(dst, 'w', compression=ZIP_DEFLATED) as myzip:
        for filename, arcname in tqdm(list(zip(filenames, arcnames))):
            myzip.write(filename, arcname)
    _zipinfo(dst)


def unzip_file(src: str, dst: str = './') -> None:
    _zipinfo(src)
    with ZipFile(src, 'r') as myzip:
        infolist = myzip.infolist()
        for member in tqdm(infolist):
            myzip.extract(member, dst)


def _zipinfo(src: str) -> None:
    with ZipFile(src, 'r') as myzip:
        infolist = myzip.infolist()
        is_dir = [_ZipInfo.is_dir() for _ZipInfo in infolist]
        compress_size_list = [_ZipInfo.compress_size for _ZipInfo in infolist]
        file_size_list = [_ZipInfo.file_size for _ZipInfo in infolist]

    compress_size = float(sum(compress_size_list))
    file_size = float(sum(file_size_list))

    ratio = compress_size/file_size
    compress_size, compress_size_unit = size_fmt(compress_size)
    file_size, file_size_unit = size_fmt(file_size)
    folder_num = sum(is_dir)
    file_num = len(is_dir) - folder_num

    s = (f'Archive {compress_size:.1f} {compress_size_unit}\n'
         + f'Original {file_size:.1f} {file_size_unit}\n'
         + f'a total of {file_num} Files and {folder_num} Folders\n'
         + f'ratio = {ratio:.2%}')
    print(s)
