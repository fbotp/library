#encoding=utf-8
import re
import requests

def login(ID, Password):
    # 登录
    school_home_url = "学校图书馆url"
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'})
    r = session.get(school_home_url+'/login.aspx')
    data = dict(re.findall('<input type="hidden" name="(.*)" id=".*" value="(.*)" />', r.text))
    data['subCmd'] = 'Login'
    data['txt_LoginID'] = ID
    data['txt_Password'] = Password
    session.post(school_home_url+'/Login.aspx', data=data)
    return session
