#encoding=utf-8
import requests
import re
import datetime
import os
import time
import sys

def choose(session, seatNo, spanSelect, flag):
    school_home_url = "学校图书馆网址"
    date = datetime.datetime.now()+datetime.timedelta(days=1, hours=1)
    date = date.strftime('%Y/%m/%d')
    seatShortNo = seatNo[-3:]
    roomNo = seatNo[:6]
    if flag:
        session.get(school_home_url+'/BookSeat/BookSeatListForm.aspx')
    r = session.get(school_home_url+'/BookSeat/BookSeatMessage.aspx?seatNo='+seatNo+'&seatShortNo='+seatShortNo+'&roomNo='+roomNo+'&date='+date+'&timeSpan=')
    data = dict(re.findall('<input type="hidden" name="(.*)" id=".*" value="(.*)" />', r.text))
    data['subCmd'] = 'select'
    data['spanSelect'] = spanSelect
    r = session.post(school_home_url+'/BookSeat/BookSeatMessage.aspx?seatNo='+seatNo+'&seatShortNo='+seatShortNo+'&roomNo='+roomNo+'&date='+date+'&timeSpan=', data=data)
    data.update(re.findall('<input type="hidden" name="(.*)" id=".*" value="(.*)" />', r.text))
    data['subCmd'] = 'query'
    if flag:
        timer = os.popen('date')
        time.sleep(flag-int(timer.read().split(':')[-1][:2]))
        timer.close()
    while '成功' not in r.text and '已有' not in r.text:
        try:
            r = session.post(school_home_url+'/BookSeat/BookSeatMessage.aspx?seatNo='+seatNo+'&seatShortNo='+seatShortNo+'&roomNo='+roomNo+'&date='+date+'&timeSpan=', data=data)
        except Exception as e:
            print(e)
            continue
        result = re.findall('<h5 id="MessageTip">(.*)</h5>', r.text)[0]
        print(seatShortNo+result)
        if '黑名单' in result or '已经被预约' in result or '对不起当前阅览室已经没有可预约的座' in result:
            session.close()
            sys.exit()
    session.close()
