#!/usr/bin/env python2
# -*- coding: utf8 -*-
# ulogme_serve.py for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
from __future__ import print_function  # Python 2 compatibility

PROGRAM_NAME = "uLogMe server (ulogme_serve.py)"

try:
    from gi.repository import Notify
    # One time initialization of libnotify
    Notify.init(PROGRAM_NAME)

    def notify(body, summary=PROGRAM_NAME, icon="dialog-information"):
        """ Send a notification."""
        # XXX I could also use Popen with notify-send ? Cf. ansicolortags.notify
        try:
            # Create the notification object
            notification = Notify.Notification.new(
                summary,
                body,   # Optional
                icon  # "dialog-information"  # "dialog-warn", "dialog-error"
            )

            # # The notification will have a button that says "Reply to Message".
            # # my_callback_func is something we will have to define
            # my_callback_func = lambda x: None

            # notification.add_action(
            #     "action_click",
            #     "Reply to Message",
            #     my_callback_func,
            #     None  # Arguments
            # )

            # Lowest urgency
            notification.set_urgency(0)

            # Actually show on screen
            notification.show()
        # Ugly! XXX Catches too general exception
        except Exception as e:
            print("\nError, notify.notify failed, with this exception")
            print(e)
            # print("Exception: dir(e) =", dir(e))  # DEBUG


except ImportError:
    print("\nError, gi.repository.Notify seems to not be available, so notification will not be available ...")
    print("On Ubuntu, if you want notifications to work, install the 'python-gobject' and 'libnotify-bin' packages.")
    print("(For more details, cf. 'http://www.devdungeon.com/content/desktop-notifications-python-libnotify')")

    def notify(body, summary=PROGRAM_NAME, icon="dialog-information"):
        """ Send a fake notification."""
        print("Warning, desktop notification seems to not be available ...")
        print("Notification: '{}', from '{}' with icon '{}'.".format(body, summary, icon))


if __name__ == '__main__':
    notify("Test body Test body Test body Test body Test body Test body !", icon="terminal")
