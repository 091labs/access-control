#!/usr/bin/env python
from access.models import User

print "Users enrolled:"
for user in User.query.all():
    print "%s <%s> = %d" % (user.name, user.email, user.key_id)
