# plot1090

This is a pretty simple collection of Python scripts that will take
dump1090 port 30003 style stream of data (I think the official name for
the format is SBS1?) on stdin, and outputs generates a (huge) HTML file
with a visualisation on top of a Google Map.

There are three scripts:

* `plotter.py` Plots lines of all flights paths found in the file.
* `edge.py` The common edge plot, showing the edge of your coverage
  area, around a given central point.
* `dotter.py` First thing I wrote. Not very interesting, instead of
  lines it draws dots showing how many planes were spotted in the area
  near it.

They share a bunch of flags:

* `-a --altitude-range` Alitude range, ignore messages if the plane was
  outside that altitude range.
* `-c --center` Coordinates of center, used to automatically center the
  map there, and used as the center (receiver location) for the edge
  plot.
* `-A --api-key` Google Maps API key.  By default it'll use mine which
  for you will work only when loading result files from file:///.

# Dependencies

Nothing too special other than geographiclib:

```
sudo apt-get install python-geographiclib
```

`dotter.py` still used geopy but it's not a very interesting script
anyway.

# Example

First, start capturing some data from dump1090 (or similar):

```
nc localhost 30003 > adsb.log
```

(Hit Ctrl-C to abort, or you could use
[`timeout(1)`](http://man7.org/linux/man-pages/man1/timeout.1.html) to
limit runtime.

Plot all approach + departure traffic (below 10k) feet only from a
stream you somehow captured at LHR T5:

```
./plotter.py -a -10000 -c 51.4729347,-0.4881842 < adsb.log > paths.html
```

Edge plot of all traffic over 10k feet:

```
./edge.py -a 10000- -c 51.4729347,-0.4881842 < adsb.log > edge-plot.html
```

# Example result

![](https://gaa.st/~wilmer/lhr.png)

# Licence

Copyright © 2015 Wilmer van der Gaast

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.