import datetime
import random
import time

today = datetime.datetime.strptime(str(datetime.date.today()), '%Y-%m-%d')
oneday = datetime.timedelta(days=1) # 定义时间增量
tomorrow = today+ oneday
now_time = datetime.datetime.today()
seconds_remaining =  (tomorrow - now_time).seconds
print(type(seconds_remaining))
print(seconds_remaining//3600,'h', seconds_remaining%3600//60, 'm')

cap_num = ''
for i in range(6):
    cap_num += str(random.randint(0,9))
print(cap_num)