#!/usr/bin/env python2
# -*- coding: utf8 -*-
# ulogme_serve.py for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
from __future__ import print_function   # Python 2 compatibility
from __future__ import absolute_import  # Python 2 compatibility

PROGRAM_NAME = "uLogMe server (ulogme_serve.py)"

try:
    from gi.repository import Notify
    # One time initialization of libnotify
    Notify.init(PROGRAM_NAME)

    def notify(body, summary=PROGRAM_NAME, icon="dialog-information"):
        """ Send a notification."""
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
            print("\nnotify.notify(): Error, notify.notify() failed, with this exception")
            print(e)
            # print("Exception: dir(e) =", dir(e))  # DEBUG


except ImportError:
    print("\nError, gi.repository.Notify seems to not be available, so notification will not be available ...")
    print("On Ubuntu, if you want notifications to work, install the 'python-gobject' and 'libnotify-bin' packages.")
    print("(For more details, cf. 'http://www.devdungeon.com/content/desktop-notifications-python-libnotify')")

    from subprocess import Popen

    def notify(body, summary=PROGRAM_NAME, icon="dialog-information"):
        """ Send a fake notification."""
        print("notify.notify(): Warning, desktop notification from Python seems to not be available ...")
        # print("Notification: '{}', from '{}' with icon '{}'.".format(body, summary, icon))
        try:
            print("notify.notify(): Trying to use the command line program 'notify-send' ...")
            if icon:
                Popen(['notify-send', summary, body, "--icon=%s" % (icon)])
                print("notify.notify(): A notification have been sent, with summary = %s, body = %s, and icon = %s." % (summary, body, icon))
            else:
                Popen(['notify-send', summary, body])
                print("notify.notify(): A notification have been sent, with summary = %s, and body = %s." % (summary, body))
            return 0
        # Ugly! XXX Catches too general exception
        except Exception as e:
            print("notify.notify(): notify-send : not-found ! Returned exception is %s." % e)
            return -1


if __name__ == '__main__':
    notify("Test body Test body Test body Test body Test body Test body !", icon="terminal")
