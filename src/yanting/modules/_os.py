import os

from tqdm import tqdm


def copy_file(src: str, dst: str = './') -> None:
    fileName = os.path.basename(src)
    size = os.stat(src).st_size
    if os.path.isdir(dst):
        dst = os.path.join(dst, fileName)
    with tqdm(total=size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                while True:
                    buf = fsrc.read(16*1024)
                    if not buf:
                        print(buf)
                        break
                    fdst.write(buf)
                    pbar.update(len(buf))
