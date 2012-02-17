from Exam_Room_Management.App.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

"""
def my_view2(request):
    errors = []
    if ( 'id' in request.POST and request.POST['id'] and
         'pass' in request.POST and request.POST['pass'] ) :        
        id_tmp = request.POST['id']
        password = request.POST['pass']
        user = authenticate(username=id_tmp,password=password)
        if user is not None :
            if user.is_active :
                login(request, user)
                return render_to_response('admin_page.html')
            else :
                errors.append('Disabled account.') 
        else :
            errors.append('Invalid login.')
        return render_to_response('login_page.html',{'errors': errors})
    else :
        errors.append('You must fill in all of the fields.')
        return render_to_response('login_page.html',{'errors': errors})
"""

def my_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s'%request.path)

def main_page(request):    
    return render_to_response('main_page.html')

def admin_page(request):
    return render_to_response('admin_page.html')

def student_page(request):
    errors = []   
    if ( 'id' in request.GET and request.GET['id'] and
         'name' in request.GET and request.GET['name'] ) :
        id_tmp = request.GET['id']     
        name_tmp = request.GET['name']                
        if Student.objects.filter(stdID__icontains=id_tmp) :
            errors.append('ID does exist already.')                   
        else :
            add_info = Student(stdID=id_tmp,stdName=name_tmp)
            add_info.save()
        return render_to_response('student_page.html',{'errors': errors,'stds': Student.objects.all()})
    else :
        errors.append('You must fill in all of the fields.')
        return render_to_response('student_page.html',{'errors': errors,'stds': Student.objects.all()})
    
