import time
from datetime import timedelta


def count_down(weeks=0, days=0, hours=0, minutes=0, seconds=0):
    remain_time = timedelta(
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )
    while remain_time.total_seconds() > 0:
        time.sleep(1)
        remain_time -= timedelta(seconds=1)
        print(f"\r {remain_time} 倒计时结束后退出本进程", end="", flush=True)
