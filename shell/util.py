import os
from typing import Optional

def print_flush(x, end='\n'): 
    print(x, end=end, flush=True)

def resolve_path(x) -> Optional[str]:
    if os.path.isfile(x):
        return os.path.abspath(x)

    PATH = os.environ['PATH'].split(os.pathsep)
    for p in PATH:
        joined = os.path.join(p, x)
        if os.path.exists(joined):
            return joined
    return None
