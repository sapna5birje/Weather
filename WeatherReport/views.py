from django.shortcuts import render, redirect, reverse

# Create your views here.
#from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime,calendar,datetime


def index(request):
	return render(request, 'templates.html')

def weather(request):
	City=request.POST.get('City')
	if not City:
		return render(request, 'templates.html', {'ERROR':'Please enter City'})

	
	current_user = request.user
	response = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+City+'&appid=8320f9d1cefcdcdd0195f77470fdaa67')
	geodata = response.json()
	temp=int(geodata['main']['temp']-273)
	feelslike=int(geodata['main']['feels_like']-273)
	humidity=int(geodata['main']['humidity'])
	icon=geodata['weather'][0]['icon']
	iconURL = "http://openweathermap.org/img/wn/";
	src = iconURL + icon + "@2x.png";
	print(src)

	now = datetime.datetime.now()
	day=now.strftime("%A")
	responseforcaste=requests.get('https://api.openweathermap.org/data/2.5/forecast?q='+City+'&appid=8320f9d1cefcdcdd0195f77470fdaa67')
	forcasteresults=responseforcaste.json()
	forcasteresult=forcasteresults['list']
	listtemp=[]
	listday=[]
	listfeels=[]
	weekday=[]
	for n in range(len(forcasteresult)):
			v=forcasteresult[n]['dt_txt'].split()
			if v[0] in listday:
				pass;
			else:
				listday.append(v[0])
				listtemp.append(int(forcasteresult[n]['main']['temp']-273))
				listfeels.append(int(forcasteresult[n]['main']['feels_like']-273))

	for n in range(len(listday)):
		born = datetime.datetime.strptime(listday[n], '%Y-%m-%d').weekday()
		v=calendar.day_name[born]
		weekday.append(v)




	return render(request, 'details.html', {
    	'ip':temp ,
    	'feelslike':feelslike,
    	'curentuser':current_user,
    	'day':day,
    	'forcasteresults':listtemp,
    	'listfeels':listfeels,
    	'listday':weekday,
    	'humidity':humidity,
    	'icon':src
    })
