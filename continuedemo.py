import continueseat
import login

id = 'xxx'
password = 'xxx'

session = login.login(id, password)
continueseat.continuewhen(session, __file__.split('/')[-1])
