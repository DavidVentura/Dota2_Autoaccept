#!/usr/bin/python
import dbus
import glib
from dbus.mainloop.glib import DBusGMainLoop
from subprocess import call
import time

def filter_cb(bus, message):
	if message.get_member() != "Notify":
		return
	args = message.get_args_list()
	summary=args[3]
	body=args[4]
	if 'game is ready' in body:
		print "TIME FOR DOTO"
		call(["wmctrl", "-a", "Dota 2"])
		time.sleep(3) #Wait three seconds in case the computer is slow to switch.
		call(["xdotool", "key", "Return"])

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
bus.add_match_string_non_blocking( "eavesdrop=true, interface='org.freedesktop.Notifications'")
bus.add_message_filter(filter_cb)

mainloop = glib.MainLoop()
mainloop.run()
