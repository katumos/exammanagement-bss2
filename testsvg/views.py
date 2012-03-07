from django.shortcuts import render_to_response
from django.template import *
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template

def index(request):
    return render_to_response('index.html')

def svg(request):
    html = "<html><body><svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.1\">"
    x = 50
    y = 100
    for j in range(0,5):
    	for i in range(0,6):
    		html += "<rect width=\"110\" height=\"50\"style=\"fill:rgb(192,192,192);stroke-width:1;stroke:rgb(0,0,0)\"x=\"%s\" y=\"%s\"/>"%(x,y)
		x += 200
        y += 80
	x = 50
    html += "</svg></body></html>"
    return HttpResponse(html)


