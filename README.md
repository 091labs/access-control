access-control
==============

Code for the door access control system

auto-start
----------

The following should be placed in /etc/rc.local to start the door
control daemon and the flask interface.

```
screen -d -m -S access-control sudo python /home/pi/access-control/daemon.py
screen -S access-control -X title daemon
screen -S access-control -X screen -t flask python /home/pi/access-control/run_flask.py
```
