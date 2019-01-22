=====
Usage
=====

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
