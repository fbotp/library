#encoding=utf-8
import requests
import re
import datetime
from crontab import CronTab
import sys

file = ''
default_hour, default_minute = 9, 30

def changecron(hour, minute):
    global file
    with CronTab(user='zero') as cron:
        for job in cron:
            if job.comment == file:
                job.hour.on(int(hour))
                job.minute.on(int(minute))
    sys.exit()

def continuewhen(session, name):
    global file
    school_home_url = "学校图书馆url"
    file = name
    data = {}
    data['subCmd'] = 'ContinuedWhen'
    data['subBookNo'] = ''
    last = re.findall('<h5 id="lblenterOutTime">(.*)</h5>', session.get(school_home_url+'/UserInfos/UserInfo.aspx').text)[0]
    if last == '无':
        print('无座')
        session.close()
        changecron(default_hour, default_minute)
    last = datetime.datetime.strptime(last, '%H:%M:%S') + datetime.timedelta(hours=3, minutes=50)
    if last > datetime.datetime.now().strptime(datetime.datetime.now().strftime('%H:%M:%S'), '%H:%M:%S'):
        session.close()
        if last.hour >= 21:
            print('太晚了')
            changecron(default_hour, default_minute)
        print('下次续时时间:', last.hour, ':', last.minute+1)
        changecron(last.hour, last.minute+1)
    while True:
        try:
            r = session.post(school_home_url+'/UserInfos/UserInfo.aspx', data=data)
        except Exception as e:
            print(e)
            continue
        result = re.findall('<span id="spanWarmInfo" name="spanWarmInfo" style="color: Red">(.*)</span>', r.text)[0]
        print(result)
        session.close()
        if '直到闭馆时' in result:
            changecron(default_hour, default_minute)
        last = datetime.datetime.now() + datetime.timedelta(hours=3, minutes=50)
        if last.hour >= 21:
            changecron(default_hour, default_minute)
        changecron(last.hour, last.minute+1)
