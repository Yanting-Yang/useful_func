from typing import Tuple


def size_fmt(size: float) -> Tuple[float, str]:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0:
            return size, unit
        size /= 1024.0
    return size, unit
