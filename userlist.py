import argparse
from userdb import UserDB

db = UserDB()
print "Users enrolled:"
for row in db.get_all():
    print "%s <%s> = %s" % (row.name, row.email, row.rfidkey)
