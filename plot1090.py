import getopt
import json
import sys

ALT_RANGE = (0, 999999)

CENTER = (51.4768033, 0)

# Will work for file:/// URLs, if you want to throw stuff online you'll
# need to request your own key.
API_KEY = "AIzaSyBFHaZ3hPmn908XJVXRPbxshuzfzUkzwlg"

opts, r = getopt.getopt(sys.argv[1:], "c:a:A:", ["center=", "altitude-range=", "api-key="])
for k, v in opts:
	if k in ("-c", "--center"):
		CENTER = tuple(float(x) for x in v.split(",")[0:2])
	elif k in ("-a", "--altitude-range"):
		lo, hi = v.split("-")
		ALT_RANGE = ((lo and int(lo) or ALT_RANGE[0]),
		             (hi and int(hi) or ALT_RANGE[1]))
	elif k in ("-A", "--api-key"):
		API_KEY = v
	else:
		raise RuntimeError("BUG flag: %s" % (k, v))

def poly2gmaps(poly):
	"""GMaps API wants its polygons in a bulky dict, here we
	generate one from more convenient tuple form."""
	return [{"lat": lat, "lng": lon} for (lat, lon) in poly]


def write_html(vars, js, title="plot1090"):
	"""Throws data (after json-encoding) and some JavaScript code
	into a very simple Google Maps API client HTML page."""
	jsvars = []
	for v in sorted(vars):
		jsvars.append("%s = %s;" % (v, json.JSONEncoder().encode(vars[v])))

	print """\
<!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no">
	<meta charset="utf-8">
	<title>%(title)s</title>
	<style>
		html, body {
			height: 100%%;
			margin: 0;
			padding: 0;
		}
		#map {
			height: 100%%;
		}
	</style>
</head>
<body>
	<div id="map"></div>
	<script>

%(vars)s

function initMap() {
	// Create the map.
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 8,
		center: d.center,
		mapTypeId: google.maps.MapTypeId.TERRAIN
	});
%(js)s
}

	</script>
	<script async defer
	    src="https://maps.googleapis.com/maps/api/js?key=%(api_key)s&signed_in=true&callback=initMap"></script>
	</body>
</html>
""" % {
	"title": title,
	"vars": "\n".join(jsvars),
	"js": js,
	"api_key": API_KEY,
}
