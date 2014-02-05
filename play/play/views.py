from django.template import Context, loader
from django.http import HttpResponse
import pickle
from datetime import datetime

# Render the main page
def index(request):
    days = pickle.load(open('days.dat', 'r'))
    weather = pickle.load(open('weather.dat', 'r'))
    windns = pickle.load(open('windns.dat', 'r'))
    windai = pickle.load(open('windai.dat', 'r'))
    windc = pickle.load(open('windc.dat', 'r'))
    stevens = open('stevens.xml', 'r').readlines()
    stevens = ''.join(stevens).replace('\n','')

    t = loader.get_template('index.html')
    c = Context({ 'days': days,  'weather': weather, 'windai': windai, 'windns': windns, 'windc': windc, 'stevens' : stevens, })
    return HttpResponse(t.render(c))

# Traffic is in a special i-frame, we refresh that on a separate schedule
def traffic(request):
    refreshtime = 3600
    if (datetime.now().hour > 6 and datetime.now().hour < 11):
        refreshtime = 600
    html = '''<html>
<head>
<meta http-equiv="refresh" content="%s" >
<style media="screen" type="text/css">
	.crop { width: 250px; height: 300px; overflow: hidden; }
	.crop img { width: 383px; height: 1200px; margin: -550px 0 0 -0px; }
</style>
<body>
<div class="crop">
    <img src="http://images.wsdot.wa.gov/nwflow/flowmaps/video_map_SeattleMetro.gif" alt="WSDOT TrafficMap" />
</div>
</body></html>
''' % refreshtime
    return HttpResponse(html)
