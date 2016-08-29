#!/usr/bin/python

import sys

from geographiclib.geodesic import Geodesic

import plot1090

misc = {}

polydict = {}
polys = []

for line in sys.stdin.xreadlines():
	l = line.split(",")
	try:
		id = int(l[4], 16)
		lat, lon = float(l[14]), float(l[15])
		alt = int(l[11])
	except (IndexError, ValueError):
		continue
	if not plot1090.ALT_RANGE[0] <= alt <= plot1090.ALT_RANGE[1]:
		continue
	if id in polydict:
		last = polydict[id]["poly"][-1]
		d = Geodesic.WGS84.Inverse(last[0], last[1], lat, lon)
		# If our latest data point was >2.5km away, make a new
		# polygon instead. (Should maybe do the same with time
		# differences to avoid strange lines between approach
		# and departure.)
		if d["s12"] > 2500: # 2.5km
			# add len check!
			polys.append(polydict[id]["poly"])
			polydict[id] = {"poly": []}
		elif len(polydict[id]) >= 2:
			# Still going in the same direction? Ugly fuzzy
			# trick to try to compress files by combining
			# straight lines into a single pair of
			# coordinates. Makes files a lot smaller and
			# easier to render.
			if (abs(polydict[id]["azi"] - d["azi1"]) % 360) < 2.5:
				#print "Similar: %r %r" % (d, dlast)
				polydict[id]["poly"].pop()
		
		polydict[id]["azi"] = d["azi1"]
	else:
		polydict[id] = {"poly": []}
	polydict[id]["poly"].append((lat, lon))

misc.update({
	"center": {
		"lat": plot1090.CENTER[0],
		"lng": plot1090.CENTER[1],
	},
})

plot1090.write_html({
	"polys": [plot1090.poly2gmaps(p) for p in polys if len(p) > 1],
	"d": misc,
}, """
	for (p of polys) {
		var polygon = new google.maps.Polyline({
			path: p,
			strokeColor: '#000000',
			strokeOpacity: 0.25,
			strokeWeight: 1,
			map: map
		});
	}
""", "plot1090 - flight path lines")
