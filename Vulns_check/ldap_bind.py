import ldap3
import re

nameContext=[]
addContext=False
ip='127.0.0.1'
port=389
ssl=False
server=ldap3.Server(ip, get_info = ldap3.ALL, port=port, use_ssl=ssl)
connection=ldap3.Connection(server)
connection.bind()
info=str(server.info)

with open("../logs/ldap_bind.log", "w") as f:
	f.write(info)
with open("../logs/ldap_bind.log","r") as f:
	for line in f:
		if not addContext:
			if re.match("^.+Naming contexts:",line):
				addContext=True
				pass
			else :
				pass
		elif re.match("^.+Supported controls:",line):
			addContext=False
			pass
		else :
			nameContext.append(line)
			pass

for i in nameContext:
	print(connection.search(nameContext, '(objectclass=*)'))
	print(connection.entries)