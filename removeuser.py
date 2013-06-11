#!/usr/bin/env python

import argparse
from userdb import UserDB

db = UserDB()
parser = argparse.ArgumentParser()
parser.add_argument("name", help="Name of user to remove.")
parser.add_argument("email", help="Email of user to remove.")
parser.add_argument("key", help="RFID key of user to remove.")
args = parser.parse_args()

db.remove_user(args.name, args.email, args.key)
