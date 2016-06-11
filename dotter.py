#!/usr/bin/python

# Dots, not lines. First thing I wrote, not very exciting so I don't
# think I'll work on it any further.

import collections
import operator
import sys

from geopy import distance

import plot1090

MUL=16

misc = {}

top = collections.defaultdict(lambda: 0)

for line in sys.stdin.xreadlines():
	l = line.split(",")
	try:
		lat, lon = float(l[14]), float(l[15])
	except (IndexError, ValueError):
		continue
	
	top[(int(lat*MUL+.5),int(lon*MUL+.5))] += 1

s = list(top.items())
s.sort(key=operator.itemgetter(1))

misc.update({
	"center": {
		"lat": float(s[-1][0][0]) / MUL,
		"lng": float(s[-1][0][1]) / MUL,
	},
	"maxcount": s[-1][1],
})

# Number of meters for a dot at maxcount, which will be the approximate
# distance between centers of dots
hot = (misc["center"]["lat"], misc["center"]["lng"])
maxm = distance.distance(hot, (hot[0] + (1.0 / MUL), hot[1])).m / 2

misc.update({
	"maxm": int(maxm),
	"step": int(maxm / s[-1][1]),
})

#print "Lo %d Hi %d" % (s[0][1], s[-1][1])
#print len(s)

# Now sort it by position which I guess looks a little nicer.
#s = s[-100:]
s.sort()

spots = []
for block, count in s:
	latlon = tuple((float(x) / MUL) for x in block)
	spots.append({
		"center": dict(zip(["lat", "lng"], latlon)),
		"count": count,
	})

plot1090.write_html({
	"hotspots": spots,
	"d": misc,
}, """
	for (spot of hotspots) {
		var radius = Math.min(spot.count*d.step*2.2, d.maxm);
		var colour;
		if (spot.count > (d.maxcount / 2)) {
			var red = Math.round(Math.max(17, -102 + 357 * (spot.count / d.maxcount)));
			var colour = '#' + red.toString(16) + '1111';
		} else {
			var colour = '#111111';
		}
		var circle = new google.maps.Circle({
			strokeWeight: 0,
			fillColor: colour,
			fillOpacity: 0.35,
			map: map,
			center: spot.center,
			radius: radius
		});
	}
""", "dot1090")
