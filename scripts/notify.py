#!/usr/bin/env python2
# -*- coding: utf8 -*-
# notify.py for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
"""
Defines one useful function notify() to (try to) send a desktop notification.
"""

from __future__ import print_function   # Python 2 compatibility
from __future__ import absolute_import  # Python 2 compatibility

from webbrowser import open as openTab
from os.path import exists, join
from glob import glob
from random import choice
from subprocess import Popen


# XXX Unused callback function for the notifications
def open_the_ulogme_page(notification, label, args=("localhost", 8124)):
    """ Open the http://{}:{}/ URL in a new tab of your favorite browser. """
    print("notify.notify(): open_the_ulogme_page callback function ...")
    print("open_the_ulogme_page(): notification = {}, label = {}, args = {} ...".format(notification, label, args))
    IP, PORT = args
    ulogme_url = "http://{}:{}/".format(IP, PORT)
    print("notify.notify(): Calling 'open(ulogme_url, new=2, autoraise=True)' ...")
    return openTab(ulogme_url, new=2, autoraise=True)


# Constants for the program
PROGRAM_NAME = "uLogMe server (ulogme_serve.py)"
ICON_PATH    = join("..", "scripts", "icons", "pikachu.png")
ICON_PATHS   = glob(join("..", "scripts", "icons", "*.png"))

# Define the icon loaded function
try:
    from gi.repository import GdkPixbuf

    def load_icon(random=True):
        """ Load and open a random icon. """
        if random:
            iconpath = choice(ICON_PATHS)
        else:
            iconpath = ICON_PATH
        # print("iconpath =", iconpath)  # DEBUG
        # Loading the icon...
        if exists(iconpath):
            # Use GdkPixbuf to create the proper image type
            iconpng = GdkPixbuf.Pixbuf.new_from_file(iconpath)
        else:
            iconpng = None
        # print("iconpng =", iconpng)  # DEBUG
        return iconpng

except ImportError:
    print("\nError, gi.repository.GdkPixbuf seems to not be available, so notification icons will not be available ...")
    print("On Ubuntu, if you want notification icons to work, install the 'python-gobject' and 'libnotify-bin' packages.")
    print("(For more details, cf. 'http://www.devdungeon.com/content/desktop-notifications-python-libnotify')")

    def load_icon(random=True):
        return None


# Trying to import gi.repository.Notify
has_Notify = False
try:
    from gi.repository import Notify
    # One time initialization of libnotify
    Notify.init(PROGRAM_NAME)
    has_Notify = True
except ImportError:
    print("\nError, gi.repository.Notify seems to not be available, so notification will not be available ...")
    print("On Ubuntu, if you want notifications to work, install the 'python-gobject' and 'libnotify-bin' packages.")
    print("(For more details, cf. 'http://www.devdungeon.com/content/desktop-notifications-python-libnotify')")


# Define the first notify function, with gi.repository.Notify
def notify_gi(body, summary=PROGRAM_NAME,
              icon=None,
              IP="localhost", PORT=8124,  # FIXED use this in ulogme_serve.py
              timeout=5  # In seconds
              ):
    """
    Send a notification, with gi.repository.Notify.

    - icon can be "dialog-information", "dialog-warn", "dialog-error". By default it is set to the 'pikachu.png' image
    """
    try:
        # Trying to fix a bug:
        # g-dbus-error-quark: GDBus.Error:org.freedesktop.DBus.Error.ServiceUnknown: The name :1.5124 was not provided by any .service files (2)
        Notify.init(PROGRAM_NAME)
        # XXX maybe the PROGRAM_NAME should be random?

        # Cf. http://www.devdungeon.com/content/desktop-notifications-python-libnotify
        # Create the notification object
        if icon is not None:
            notification = Notify.Notification.new(
                summary,  # Title of the notification
                body,     # Optional content of the notification
                icon      # XXX Should not indicate it here
            )
        else:
            notification = Notify.Notification.new(
                summary,  # Title of the notification
                body      # Optional content of the notification
            )

            # Add a Pikachu icom to the notification
            # Why Pikachu? ALWAYS PIKACHU! http://www.lsv.ens-cachan.fr/~picaro/
            iconpng = load_icon(random=True)
            if iconpng is not None:
                # Use the GdkPixbuf image
                notification.set_icon_from_pixbuf(iconpng)
                notification.set_image_from_pixbuf(iconpng)

        # Lowest urgency (LOW, NORMAL or CRITICAL)
        notification.set_urgency(Notify.Urgency.LOW)

        # add duration, lower than 10 seconds (5 second is enough).
        notification.set_timeout(timeout * 1000)

        # # XXX add a callback that open the browser tab/page on uLogMe when clicked on it
        # # The notification will have a button that says "View uLogMe page".
        # #    "default",
        # notification.add_action(
        #     "action_click",
        #     "View uLogMe page",
        #     open_the_ulogme_page,
        #     (IP, PORT)  # Arguments given to open_the_ulogme_page
        # )
        # FIXME how to disable on jarvisPRO but keep it on jarvisOld ?

        # Actually show the notification on screen
        notification.show()
        return 0

    # Ugly! XXX Catches too general exception
    except Exception as e:
        print("\nnotify.notify(): Error, notify.notify() failed, with this exception")
        print(e)
        return -1


# Define the second notify function, with a subprocess call to 'notify-send'
def notify_cli(body, summary=PROGRAM_NAME,
               icon="dialog-information",
               IP="localhost", PORT=8124,  # XXX unused here, notify-send does not accept callback functions
               timeout=5  # In seconds
               ):
    """
    Send a notification, with a subprocess call to 'notify-send'.
    """
    print("notify.notify(): Warning, desktop notification from Python seems to not be available ...")
    try:
        print("notify.notify(): Trying to use the command line program 'notify-send' ...")
        if icon:
            Popen(["notify-send", "--expire-time=%s" % (timeout * 1000), "--icon=%s" % (icon), summary, body])
            print("notify.notify(): A notification have been sent, with summary = %s, body = %s, expire-time = %s and icon = %s." % (summary, body, timeout * 1000, icon))
        else:
            Popen(["notify-send", "--expire-time=%s" % (timeout * 1000), summary, body])
            print("notify.notify(): A notification have been sent, with summary = %s, body = %s and expire-time = %s." % (summary, body, timeout * 1000))
        return 0
    # Ugly! XXX Catches too general exception
    except Exception as e:
        print("\nnotify.notify(): notify-send : not-found ! Returned exception is %s." % e)
        return -1


# Define the unified notify.notify() function
def notify(body, summary=PROGRAM_NAME,
           icon=None,
           IP="localhost", PORT=8124,  # FIXED use this in ulogme_serve.py
           timeout=5  # In seconds
           ):
    print("Notification: '{}', from '{}' with icon '{}'.".format(body, summary, icon))  # DEBUG
    if not has_Notify:
        return notify_cli(body, summary=summary, icon=icon, IP=IP, PORT=PORT, timeout=timeout)
    else:
        try:
            return_code = notify_gi(body, summary=summary, icon=icon, IP=IP, PORT=PORT, timeout=timeout)
            if return_code < 0:
                return_code = notify_cli(body, summary=summary, icon=icon, IP=IP, PORT=PORT, timeout=timeout)
        except Exception:
            return_code = notify_cli(body, summary=summary, icon=icon, IP=IP, PORT=PORT, timeout=timeout)
        return return_code


if __name__ == "__main__":
    notify("Test body Test body Test body Test body Test body Test body ! With icon=terminal ...", icon="terminal")
    notify("Test body Test body Test body Test body Test body Test body ! With random Pokémon icon ...")
