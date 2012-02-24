from django.shortcuts import render_to_response
from django.template import *
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from Data.models import AdminData

def main(request):
    return render_to_response('main.html')

def form (request):
    return render_to_response('FormExam.html')

def out(request):
    if 'username' in request.GET and request.GET['UserName'] and 'password' in request.GET and request.GET['Password'] :
    
    	number_machine = request.GET['username']
        symptoms = request.GET['password']

	Add_db = com_data.objects.create(UserName = UserName,Password = Password)

        Add_db.save() 
        return  render_to_response ('FormExam.html')

    else :
	
    	return render_to_response('FormExam.html')






