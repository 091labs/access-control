import argparse
from userdb import UserDB

db = UserDB()
parser = argparse.ArgumentParser()
parser.add_argument("name", help="Name of member")
parser.add_argument("email", help="Email address of member")
parser.add_argument("code", help="RFID key code")
args = parser.parse_args()
print "Adding user %s <%s> = %s" % (args.name, args.email, args.code)
db.add_user(args.name, args.email, args.code)
