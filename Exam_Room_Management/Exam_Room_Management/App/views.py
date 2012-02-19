from Exam_Room_Management.App.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

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
    else :
        errors.append('You must fill in all of the fields, if you want to add information.')
    return render_to_response('student_page.html',{'errors': errors,'stds': Student.objects.all()})

def student_info_page(request, std_id):
    std = Student.objects.get(stdID=std_id)
    return render_to_response('student_info_page.html',{'std':std})

def edit_student_info_page(request, std_id):
    std = Student.objects.get(stdID=std_id)
    if ( 'id' in request.GET and request.GET['id'] ) :
        new_id = request.GET['id']
        std.stdID = new_id
        std.save()
    if ( 'name' in request.GET and request.GET['name'] ) :
        new_name = request.GET['name']
        std.stdName = new_name
        std.save()
    return render_to_response('edit_student_info_page.html',{'std':std})

def delete_student_info_page(request, std_id):
    std = Student.objects.get(stdID=std_id)
    temp = std
    std.delete()
    return render_to_response('delete_student_info_page.html',{'std':temp}) 

def subject_page(request):
    errors = []   
    if ( 'id' in request.GET and request.GET['id'] and
         'name' in request.GET and request.GET['name'] ) :
        id_tmp = request.GET['id']     
        name_tmp = request.GET['name']                
        if Subject.objects.filter(subID__icontains=id_tmp) :
            errors.append('ID does exist already.')                   
        else :
            add_info = Subject(subID=id_tmp,subName=name_tmp)
            add_info.save()        
    else :
        errors.append('You must fill in all of the fields, if you want to add information.')
    return render_to_response('subject_page.html',{'errors': errors,'subs': Subject.objects.all()})

def subject_info_page(request, sub_id):
    sub = Subject.objects.get(subID=sub_id)
    return render_to_response('subject_info_page.html',{'sub':sub})

def edit_subject_info_page(request, sub_id):
    sub = Subject.objects.get(subID=sub_id)
    if ( 'id' in request.GET and request.GET['id'] ) :
        new_id = request.GET['id']
        sub.subID = new_id
        sub.save()
    if ( 'name' in request.GET and request.GET['name'] ) :
        new_name = request.GET['name']
        sub.subName = new_name
        sub.save()
    return render_to_response('edit_subject_info_page.html',{'sub':sub})

def delete_subject_info_page(request, sub_id):
    sub = Subject.objects.get(subID=sub_id)
    temp = sub
    sub.delete()
    return render_to_response('delete_subject_info_page.html',{'sub':temp})

def room_page(request):
    errors = []   
    if ( 'id' in request.GET and request.GET['id'] and
         'size' in request.GET and request.GET['size'] ) :
        id_tmp = request.GET['id']     
        size_tmp = int(request.GET['size'])             
        if Room.objects.filter(roomID__icontains=id_tmp) :
            errors.append('ID does exist already.')                   
        else :
            add_info = Room(roomID=id_tmp,size=size_tmp)
            add_info.save()        
    else :
        errors.append('You must fill in all of the fields, if you want to add information.')
    return render_to_response('room_page.html',{'errors': errors,'rooms': Room.objects.all()})

def room_info_page(request, room_id):
    room = Room.objects.get(roomID=room_id)
    return render_to_response('room_info_page.html',{'room':room})

def edit_room_info_page(request, room_id):
    room = Room.objects.get(roomID=room_id)
    if ( 'id' in request.GET and request.GET['id'] ) :
        new_id = request.GET['id']
        room.roomID = new_id
        room.save()
    if ( 'size' in request.GET and request.GET['size'] ) :
        new_size = int(request.GET['size'])
        room.size = new_size
        room.save()
    return render_to_response('edit_room_info_page.html',{'room':room})

def delete_room_info_page(request, room_id):
    room = Room.objects.get(roomID=room_id)
    temp = room
    room.delete()
    return render_to_response('delete_room_info_page.html',{'room':temp}) 
