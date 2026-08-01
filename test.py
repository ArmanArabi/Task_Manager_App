'''
import os

print(os.path.join(os.path.dirname(os.path.dirname(__file__))))

'''

'''
import passlib
import bcrypt
print(passlib.__version__)
print(bcrypt.__version__)
'''


'''
import datetime
print(f"1:{datetime.datetime.fromtimestamp(1516239022)}")
print(f"2: {datetime.datetime.now()}")
print(f'3: {datetime.datetime.now(datetime.timezone.utc)}')

'''



from datetime import datetime, timezone

# ۱. ساعت محلی ویندوز تو (همان چیزی که در گوشه صفحه می‌بینی)
print("Local Time:", datetime.now())

# ۲. ساعت جهانی UTC (که JWT با این ساعت کار می‌کند)
print("UTC Time:  ", datetime.now(timezone.utc))

# ۳. زمان فعلی به صورت Timestamp (که در توکن‌ها ذخیره می‌شود)
import time
print("Timestamp: ", time.time())
