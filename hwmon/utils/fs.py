# hwmon/utils/fs.py

def read_str(path: str) -> str:
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""
    except PermissionError as e:
        raise RuntimeError(f"Permission denied: {path}") from e


def read_int(path: str) -> int:
    val = read_str(path)
    return int(val) if val else 0


def read_kv_dir(base: str) -> dict:
    """
    Reads a directory of files into {filename: value}
    """
    import os
    data = {}
    for name in os.listdir(base):
        path = f"{base}/{name}"
        if not os.path.isfile(path):
            continue
        data[name] = read_str(path)
    return data
