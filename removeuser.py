#!/usr/bin/env python

import argparse
import sys

from access import db
from access.models import User

parser = argparse.ArgumentParser()
parser.add_argument("email", help="Email of user to remove.")
args = parser.parse_args()

user = User.query.filter_by(email=args.email).first()
if not user:
    print "User not found"
    sys.exit(1)

print "Removing user %s <%s> = %d" % (user.name, user.email, user.key_id)
db.session.delete(user)
db.session.commit()
