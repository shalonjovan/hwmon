
def read_int(path: str) -> int:
    try:
        with open(path, "r") as f:
            return int(f.read().strip())
    except Exception as e:
        raise RuntimeError(f"Failed to read int from {path}: {e}")


def read_float(path: str) -> float:
    try:
        with open(path, "r") as f:
            return float(f.read().strip())
    except Exception as e:
        raise RuntimeError(f"Failed to read float from {path}: {e}")
