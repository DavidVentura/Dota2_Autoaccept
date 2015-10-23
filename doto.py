#!/usr/bin/env python
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from subprocess import call
import time

try:
	import glib
except ImportError:
	from gi.repository import GLib as glib

switch_back=0

def filter_cb(bus, message):
	if message.get_member() != "Notify":
		return
	args = message.get_args_list()
	summary=args[3]
	body=args[4]
	if 'game is ready' in body:
		print("TIME FOR DOTO")
		current_window=call(["xdotool","getwindowfocus", "getwindowname"])
		call(["wmctrl", "-a", "Dota 2"])
		time.sleep(2) #Wait in case the computer is slow to switch.
		call(["xdotool", "key", "Return"])
		if switch_back:
			time.sleep(2)
			call(["wmctrl", "-a", current_window])


def main():
	DBusGMainLoop(set_as_default=True)
	bus = dbus.SessionBus()
	bus.add_match_string_non_blocking( "eavesdrop=true, interface='org.freedesktop.Notifications'")
	bus.add_message_filter(filter_cb)
	
	mainloop = glib.MainLoop()
	mainloop.run()

main()
