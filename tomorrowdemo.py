import tomorrow
import login

id = '学号，也是账号'
password = '密码'
seatNo = '座位编号，抓包得'
spanSelect = '预约时间'

while True:
    try:
        session = login.login(id, password)
        break
    except Exception as e:
        print(e)

flag = 59.9
while True:
    try:
        tomorrow.choose(session, seatNo, spanSelect, flag)
        break
    except Exception as e:
        print(e)
        flag = 0
