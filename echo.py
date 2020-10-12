from datetime import datetime

container_started_at = datetime.now()


def main(**kwargs):
    return {
        "kwargs": kwargs,
        "now": datetime.now().isoformat(),
        "container_started_at": container_started_at.isoformat(),
    }
