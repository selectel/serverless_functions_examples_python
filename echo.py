import sys
from datetime import datetime

container_started_at = datetime.now()


def main(**kwargs):
    return {
        "kwargs": kwargs,
        "now": datetime.now().isoformat(),
        "container_started_at": container_started_at.isoformat(),
    }


# Call handler-function if code runs locally.
# $ python echo.py param="param pam pam" a=1
if __name__ == "__main__":
    args = sys.argv[1:]
    kwargs = dict([arg.split('=') for arg in args]) if args else {}
    print(main(**kwargs))
