=====
Usage
=====

====
From Python
====

To use pyatlonajuno in a project::

    from pyatlonajuno.lib import Juno451
    j = Juno451(username="...", password="...", host="...")

Example from ipython::

    In [6]: j.getPowerState()
    Out[6]: 'off'

    In [7]: j.setPowerState("on")
    Out[7]: 'PWON'

    In [8]: j.setSource(1)
    Out[8]: 1

    In [9]: j.setPowerState("off")
    Out[9]: 'PWOFF'

====
CLI Utility
====

Help text showing how to use the command line utility::

    08:44 $ pyatlonajuno --help
    Usage: pyatlonajuno [OPTIONS] COMMAND [ARGS]...

    Juno451 CLI.

    This cli is for controling the Atlona Juno 451 HDMI switch.

    Options:
    --username TEXT
    --password TEXT
    --hostname TEXT
    --port INTEGER
    --debug / --no-debug
    --timeout INTEGER     Seconds to wait for telnet responses
    --help                Show this message and exit.

    Commands:
    getinputstate  Get the connection status of the four inputs,...
    getpowerstate  Determine if the Juno is currently powered up
    getsource      Get the currently active input
    setpowerstate  Turn the Juno on or off
    setsource      Select an input


    08:47 $ pyatlonajuno setpowerstate --help
    Usage: pyatlonajuno setpowerstate [OPTIONS]

    Turn the Juno on or off

    Options:
    --state [on|off]  [required]
    --help            Show this message and exit.


    08:47 $ pyatlonajuno setsource --help
    Usage: pyatlonajuno setsource [OPTIONS]

    Select an input

    Options:
    --source [1|2|3|4]  [required]
    --help              Show this message and exit.
