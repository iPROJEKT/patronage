from datetime import datetime, timedelta


FROM_TIME = (
        datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')
TO_TIME = (
        datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')
MIN_LEGTH_PROJEKT = 1
MAX_LEGTH_PROJEKT = 100
START_INVERSED_AMOUNT = 0
