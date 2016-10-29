#!/usr/bin/env python2
# -*- coding: utf8 -*-
# ulogme_serve.py for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#
from __future__ import print_function   # Python 2 compatibility
from __future__ import absolute_import  # Python 2 compatibility

from webbrowser import open as openTab
from os.path import exists, join
from glob import glob
from random import choice


# XXX Unused callback function for the notifications
def open_the_ulogme_page(notification, label, args=('localhost, 8124')):
    """ Open the http://{}:{}/ URL in a new tab of your favorite browser. """
    print("notify.notify(): open_the_ulogme_page callback function ...")
    IP, PORT = args
    ulogme_url = "http://{}:{}/".format(IP, PORT)
    print("notify.notify(): Calling 'open(ulogme_url, new=2, autoraise=True)' ...")
    return openTab(ulogme_url, new=2, autoraise=True)


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
        # # print("os.getcwd(): ", os.getcwd())  # DEBUG
        # Loading the icon...
        if exists(iconpath):
            # Use GdkPixbuf to create the proper image type
            iconpng = GdkPixbuf.Pixbuf.new_from_file(iconpath)
        else:
            iconpng = None
        # print("iconpng =", iconpng)  # DEBUG
        return iconpng

except ImportError:
    def load_icon(random=True):
        return None


try:
    from gi.repository import Notify
    # One time initialization of libnotify

    def notify(body, summary=PROGRAM_NAME,
               icon="dialog-information",
               IP="localhost", PORT=8124  # FIXED use this in ulogme_serve.py
               ):
        """ Send a notification.

        - icon can be "dialog-information", "dialog-warn", "dialog-error". By default it is set to the 'pikachu.png' image
        """
        try:
            Notify.init(PROGRAM_NAME)

            # Cf. http://www.devdungeon.com/content/desktop-notifications-python-libnotify
            # Create the notification object
            notification = Notify.Notification.new(
                summary,
                body    # Optional
                # icon  # XXX Should not indicate it here
            )

            # Lowest urgency
            notification.set_urgency(0)

            # DONE add duration, lower than 10 seconds (1 second is enough).
            # XXX it does not seem to work!
            notification.set_timeout(1)

            # TODO add a Pikachu icom to the notification
            # Why Pikachu? ALWAYS PIKACHU! http://www.lsv.ens-cachan.fr/~picaro/
            iconpng = load_icon(random=True)
            if iconpng is not None:
                # Use the GdkPixbuf image
                notification.set_icon_from_pixbuf(iconpng)
                notification.set_image_from_pixbuf(iconpng)

            # # XXX add a callback that open the browser tab/page on uLogMe when clicked on it
            # # The notification will have a button that says "View uLogMe page".
            # notification.add_action(
            #     "action_click",
            #     "View uLogMe page",
            #     open_the_ulogme_page,
            #     (IP, PORT)  # Arguments given to open_the_ulogme_page
            # )

            # Actually show the notification on screen
            notification.show()

        # Ugly! XXX Catches too general exception
        except Exception as e:
            print("\nnotify.notify(): Error, notify.notify() failed, with this exception")
            print(e)


except ImportError:
    print("\nError, gi.repository.Notify seems to not be available, so notification will not be available ...")
    print("On Ubuntu, if you want notifications to work, install the 'python-gobject' and 'libnotify-bin' packages.")
    print("(For more details, cf. 'http://www.devdungeon.com/content/desktop-notifications-python-libnotify')")

    from subprocess import Popen

    def notify(body, summary=PROGRAM_NAME,
               icon="dialog-information",
               IP="localhost", PORT=8124  # XXX unused here, notify-send does not accept callback functions
               ):
        """ Send a fake notification."""
        print("notify.notify(): Warning, desktop notification from Python seems to not be available ...")
        print("Notification: '{}', from '{}' with icon '{}'.".format(body, summary, icon))  # DEBUG
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
    # notify("Test body Test body Test body Test body Test body Test body ! With icon=terminal ...", icon="terminal")
    notify("Test body Test body Test body Test body Test body Test body ! With random Pokémon icon ...")
