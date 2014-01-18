#!/usr/bin/env python
import argparse

from access import db
from access.models import User

parser = argparse.ArgumentParser()
parser.add_argument("name", help="Name of member")
parser.add_argument("email", help="Email address of member")
parser.add_argument("key_id", help="RFID key code")
args = parser.parse_args()
print "Adding user %s <%s> = %d" % (args.name, args.email, int(args.key_id))
user = User(args.name, args.email, int(args.key_id))
db.session.add(user)
db.session.commit()
