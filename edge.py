#!/usr/bin/python

import collections
import sys

from geographiclib.geodesic import Geodesic

import plot1090

MUL=4
MAX=500000

misc = {}

center = plot1090.CENTER
dists = collections.defaultdict(lambda: {"dist": 0, "latlon": center})

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
	d = Geodesic.WGS84.Inverse(center[0], center[1], lat, lon)
	#print center[0], center[1], lat, lon, d["azi1"], d["azi2"]
	rad = round((d["azi1"] % 360) * MUL)
	if d["s12"] > MAX:
		continue
	if d["s12"] > dists[rad]["dist"]:
		dists[rad] = {
			"dist": d["s12"],
			"latlon": (lat, lon),
		}

poly = []
for rad, dist in sorted(dists.items()):
	poly.append({"lat": dist["latlon"][0], "lng": dist["latlon"][1]})

misc.update({
	"center": {
		"lat": center[0],
		"lng": center[1],
	},
})

plot1090.write_html({
	"poly": poly,
	"d": misc,
}, """
	var polygon = new google.maps.Polyline({
		path: poly,
		strokeColor: '#000000',
		strokeOpacity: 0.8,
		strokeWeight: 1,
		map: map
	});
""", "plot1090 - edge plot")
