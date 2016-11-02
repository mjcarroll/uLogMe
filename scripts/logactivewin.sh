#!/bin/bash
# logactivewin.sh for https://github.com/Naereen/uLogMe/
# MIT Licensed, https://lbesson.mit-license.org/
#

# Use https://bitbucket.org/lbesson/bin/src/master/.color.sh to add colors in Bash scripts
[ -f color.sh ] && . color.sh

LANGUAGE=en
LANG=en_US.utf8

# logs the active window titles over time. Logs are written
# in ../logs/windowX.txt, where X is unix timestamp of 7am of the
# recording day. The logs are written if a window change event occurs
# (with 2 second frequency check time), or every 10 minutes if
# no changes occur.

waittime="2"  # number of seconds between executions of loop
maxtime="600"  # if last write happened more than this many seconds ago, write even if no window title changed


type xprintidle >/dev/null 2>&1 || echo -e "${red}WARNING: 'xprintidle' not installed${white}, idle time detection will not be available (screen saver / lock screen detection only) ..."

# Get idle time in seconds. If xprintidle is not installed, returns 0.
function get_idle_time() {
    type xprintidle >/dev/null 2>&1 && echo $(( $(timeout -s 9 1 xprintidle) / 1000 )) || echo 0
    # TODO code it better!
}

#------------------------------

mkdir -p ../logs
last_write="0"
lasttitle=""

while true
do
	islocked=true
	# Try to figure out which Desktop Manager is running and set the
	# screensaver commands accordingly.
	if [[ X"$GDMSESSION" == X'xfce' ]]; then
		# Assume XFCE folks use xscreensaver (the default).
		screensaverstate=$(xscreensaver-command -time | cut -f2 -d: | cut -f2-3 -d' ')
		if [[ $screensaverstate =~ "screen non-blanked" ]]; then
			islocked=false
		fi
	elif [[ X"$GDMSESSION" == X'ubuntu' || X"$GDMSESSION" == X'ubuntu-2d' || X"$GDMSESSION" == X'gnome-shell' || X"$GDMSESSION" == X'gnome-classic' || X"$GDMSESSION" == X'gnome-fallback' || X"$GDMSESSION" == X'cinnamon' ]]; then
		# Assume the GNOME/Ubuntu/cinnamon folks are using gnome-screensaver.
		screensaverstate=$(gnome-screensaver-command -q 2>&1 /dev/null)
		if [[ $screensaverstate =~ .*inactive.* ]]; then
			islocked=false
		fi
	elif [[ X"$XDG_SESSION_DESKTOP" == X'KDE' ]]; then
		islocked=$(qdbus org.kde.screensaver /ScreenSaver org.freedesktop.ScreenSaver.GetActive)
	else
		# If we can't find the screensaver, assume it's missing.
		islocked=false
	fi

	if [ "$islocked" = true ]; then
		curtitle="__LOCKEDSCREEN"  # Special tag
	else
		id="$(xdotool getactivewindow)"
		# curtitle=$(wmctrl -lpG | while read -a a; do w=${a[0]}; if (($((16#${w:2}))==id)) ; then echo "${a[@]:8}"; break; fi; done)
		# Quicker and simpler method!
		curtitle="$(xdotool getwindowname "${id}")"
	fi

    # Detect suspend, code from https://github.com/karpathy/ulogme/commit/6a28d34defee65726d55211fe742303737bc757a
    # FIXME this does not work! I should include his changes
    was_awaken=false
    # suspended_at=$(grep -E ': (performing suspend|Awake)' /var/log/pm-suspend.log | tail -n 2 | tr '\n' '|' | sed -rn 's/^(.*): performing suspend.*\|.*: Awake.*/\1/p')
    suspended_at="$(grep "Freezing user space processes ... *$" /var/log/kern.log | tail -n 1 | awk ' { print $1 " " $2 " " $3 } ')"
    if [ -n "$suspended_at" ]; then
        suspended_at="$(date -d "$suspended_at" +%s)"
        if [ "$suspended_at" -ge "$last_write" ]; then
            echo -e "${red}Suspend occured after last event${white}, '${black}was_awaken${white}' = true ...${white}"
            was_awaken=true
        fi
    fi

	perform_write=false
	# if window title changed, perform write
	if [[ X"$lasttitle" != X"$curtitle" || "$was_awaken" = true ]]; then
		perform_write=true
	fi

	T="$(date +%s)"

	# if more than some time has elapsed, do a write anyway
	#elapsed_seconds=$(expr $T - $last_write)
	#if [ $elapsed_seconds -ge $maxtime ]; then
	#	perform_write=true
	#fi

	# additional check, do not log private browsing windows (if you have something to hide?)
	# XXX customize here the regexp capturing the titles you don't want to count
	if echo "$curtitle" | grep "\(privée\|InPrivate\|Private\|Incognito\)"  &>/dev/null
	then
		echo -e "${red}Not logged private window title ...${white}"
		curtitle=""
	fi;

	# log window switch if appropriate
	if [ "$perform_write" = true -a -n "$curtitle"  ]; then
        # Get rewind time, day starts at 7am and ends at 6:59am next day
        rewind7am=$(python ./rewind7am.py)
        # One logfile daily
        log_file="../logs/window_${rewind7am}.txt"
        # If computer was just awaken, log suspend event unless it happened before 7am
        if [ "$was_awaken" = true -a "${suspended_at:-0}" -ge "$rewind7am" ]; then
            echo "$suspended_at __SUSPEND" >> "$log_file"
		fi
		echo "$T $curtitle" >> "$log_file"
		echo -e "Logged ${yellow}window title${white}: ${magenta}$(date)${white} '${green}$curtitle${white}' into '${black}$log_file${white}'"
		last_write="$T"
	fi

	lasttitle="$curtitle"  # swap
	sleep "$waittime"  # sleep
done




