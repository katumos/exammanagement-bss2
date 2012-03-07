from Exam_Room_Management.App.models import ExamStudentInfo,ExamSubjectInfo,ExamRoomInfo,ExamStudentSeat
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf

from Exam_Room_Management.App.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template.loader import get_template
from Exam_Room_Management.App.models import *
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.http import HttpResponse
from django.http import Http404

def main_page(request):    
    errors = []
    if 'id' in request.GET and request.GET['id'] :
        id_tmp = request.GET['id']     
        if ExamStudentInfo.objects.filter(stdID=id_tmp) :
            std = ExamStudentInfo.objects.get(stdID=id_tmp)
            return render_to_response('view_std_info.html',{'std':std})
        else :
            errors.append('ID does not exist')                
    return render_to_response('main_page.html',{'errors':errors})

def admin_page(request):
     return render_to_response('admin_page.html')


def login_page(request): 
    return render_to_response('login_page.html')

############################################################################################


def student_page(request):
    errors = []   
    if ( 'id' in request.GET and request.GET['id'] and
         'name' in request.GET and request.GET['name'] ) :
        id_tmp = request.GET['id']     
        name_tmp = request.GET['name']                
        if ExamStudentInfo.objects.filter(stdID=id_tmp) :
            errors.append('ID does exist already.')                   
        else :
            add_info = ExamStudentInfo(stdID=id_tmp,stdName=name_tmp)
            add_info.save()    
    return render_to_response('student_page.html',{'errors': errors,'stds': ExamStudentInfo.objects.order_by('stdID')})

def student_info_page(request, std_id):
    std = ExamStudentInfo.objects.get(stdID=std_id)  
    arrInfo = []          
    for seat in  ExamStudentSeat.objects.filter(seater=std_id) :
        info = []                       
        subj_id = ExamSubjectInfo.objects.get(subjName=seat.subj).subjID        
        info.append(subj_id)
        info.append(seat.subj)
        info.append(seat.roomID)
        info.append(seat.date)
        info.append(seat.time)
        arrInfo.append(info)    
    return render_to_response('student_info.html',{'std':std,'arrInfo':arrInfo})

def edit_student_info_page(request, std_id):
    std = ExamStudentInfo.objects.get(stdID=std_id)
    if ( 'id' in request.GET and request.GET['id'] ) :
        new_id = request.GET['id']
        std.stdID = new_id
        std.save()
    if ( 'name' in request.GET and request.GET['name'] ) :
        new_name = request.GET['name']
        std.stdName = new_name
        std.save()
    return render_to_response('edit_std_info.html',{'std':std})

def delete_student_info_confirm_page(request, std_id):    
    std = ExamStudentInfo.objects.get(stdID=std_id)
    return render_to_response('student_info.html',{'std':std,'deleting':True})

def deleting_student_info_page(request, std_id):
    ExamStudentInfo.objects.get(stdID=std_id).delete()    
    return student_page(request) 

def add_exam_subject_page(request, std_id):
    errors = []    
    std = ExamStudentInfo.objects.get(stdID=std_id)
    if 'subj' in request.GET and request.GET['subj'] :
        subj_name = request.GET['subj']         
        if ExamStudentSeat.objects.filter(seater=std_id,subj=subj_name) :
            errors.append('Subject does exist already.')
        else :            
            for room in ExamRoomInfo.objects.filter(subj=subj_name) :                
                seat = ExamStudentSeat(seater=std_id,subj=subj_name,roomID=room.roomID,time=room.time,date=room.date)
                seat.save()                     
                return student_info_page(request, std_id)
                break                
    return render_to_response('add_exam_subj.html',{'errors': errors,'stdID':std.stdID,'subjs': getAvailableSubject()})

def isRoomFull(room_id, date, time):
    room = ExamRoomInfo.objects.get(roomID=room_id,date=date,time=time)
    if room.size == room.capacity :
        return True
    else :
        return False

def getAvailableSubject():
    ava_sub = []
    rooms = ExamRoomInfo.objects.order_by('roomID')    
    for room in rooms :
        cur = ExamSubjectInfo.objects.get(subjName=room.subj)
        if not ( ava_sub.__contains__(cur) or isRoomFull(room.roomID,room.date,room.time) ) :
            ava_sub.append(cur)
    return ava_sub


def subject_page(request):
    errors = []   
    if ( 'id' in request.GET and request.GET['id'] and
         'name' in request.GET and request.GET['name'] ) :
        id_tmp = request.GET['id']     
        name_tmp = request.GET['name']                
        if ExamSubjectInfo.objects.filter(subjID=id_tmp) :
            errors.append('ID does exist already.')
        elif ExamSubjectInfo.objects.filter(subjName=name_tmp) :
            errors.append('Name does exist already.')                  
        else :
            add_info = ExamSubjectInfo(subjID=id_tmp,subjName=name_tmp)
            add_info.save()            
    return render_to_response('subject_page.html',{'errors': errors,'subjs': ExamSubjectInfo.objects.order_by('subjID')})

def subject_info_page(request, subj_id):
    subj = ExamSubjectInfo.objects.get(subjID=subj_id)
    return render_to_response('subject_info.html',{'subj':subj})

def edit_subject_info_page(request, subj_id):
    subj = ExamSubjectInfo.objects.get(subjID=subj_id)
    if ( 'id' in request.GET and request.GET['id'] ) :
        new_id = request.GET['id']
        subj.subjID = new_id
        subj.save()
    if ( 'name' in request.GET and request.GET['name'] ) :
        new_name = request.GET['name']
        subj.subjName = new_name
        subj.save()
    return render_to_response('edit_subj_info.html',{'subj':subj})

def delete_subject_info_confirm_page(request, subj_id):    
    subj = ExamSubjectInfo.objects.get(subjID=subj_id)
    return render_to_response('subject_info.html',{'subj':subj,'deleting':True})

def deleting_subject_info_page(request, subj_id):
    ExamSubjectInfo.objects.get(subjID=subj_id).delete()      
    return subject_page(request)

def room_page(request):
    errors = []   
    if ( 'id' in request.GET and request.GET['id']
         and 'day' in request.GET and request.GET['day']
         and 'month' in request.GET and request.GET['month']
         and 'year' in request.GET and request.GET['year']
         and 'time' in request.GET and request.GET['time']
         and 'subj' in request.GET and request.GET['subj'] ):
        id_tmp = request.GET['id']
        day = request.GET['day']
        month = request.GET['month']
        year = request.GET['year']
        time = request.GET['time']
        subj = request.GET['subj'] 
        date = day + '-' + month + '-' + year                
        if ExamRoomInfo.objects.filter(roomID=id_tmp,date=date,time=time) :             
            errors.append('Room does exist already.')                     
        else :
            add_info = ExamRoomInfo(roomID=id_tmp,size=0,capacity=15,date=date,time=time,subj=subj)
            add_info.save()
            return room_page(request)
    return render_to_response('room_page.html',{'errors': errors,'days':range(2,32),'months':range(2,13),
                                                'rooms': ExamRoomInfo.objects.order_by('roomID'),
                                                'subjs': ExamSubjectInfo.objects.order_by('subjID')})

def room_info_page(request, room_id, date, time):    
    room = ExamRoomInfo.objects.get(roomID=room_id,date=date,time=time)    
    return render_to_response('room_info.html',{'room':room})
    
def edit_room_info_page(request, room_id, date, time):
    room = ExamRoomInfo.objects.get(roomID=room_id,date=date,time=time)
    if ( 'id' in request.GET and request.GET['id'] ) :
        new_id = request.GET['id']
        room.roomID = new_id
        room.save()
    if ( 'size' in request.GET and request.GET['size'] ) :
        new_size = int(request.GET['size'])
        room.size = new_size
        room.save()
    if ( 'cap' in request.GET and request.GET['cap'] ) :
        new_cap = int(request.GET['cap'])
        room.capacity = new_cap
        room.save()
    if ( 'subj' in request.GET and request.GET['subj'] ) :
        new_subj = request.GET['subj']
        room.subj = new_subj
        room.save()
    if ( 'day' in request.GET and request.GET['day']
         and 'month' in request.GET and request.GET['month']
         and 'year' in request.GET and request.GET['year'] ) :
        new_day = request.GET['day']
        new_month = request.GET['month']
        new_year = request.GET['year']
        room.date = new_day + '-' + new_month + '-' + new_year
        room.save()
    if ( 'time' in request.GET and request.GET['time'] ) :
        new_time = request.GET['time']
        room.time = new_time
        room.save()
    return render_to_response('edit_room_info.html',{'room':room,'days':range(2,32),'months':range(2,13),                                                
                                                'subjs': ExamSubjectInfo.objects.order_by('subjID')})

def delete_room_info_confirm_page(request, room_id, date, time):    
    room = ExamRoomInfo.objects.get(roomID=room_id,date=date,time=time)
    return render_to_response('room_info.html',{'room':room,'deleting':True})

def deleting_room_info_page(request, room_id, date, time):
    ExamRoomInfo.objects.get(roomID=room_id,date=date,time=time).delete()    
    return room_page(request)

def delete_seat_info_confirm_page(request, std_id, subj_name):    
    std = ExamStudentInfo.objects.get(stdID=std_id)  
    arrInfo = []          
    for seat in  ExamStudentSeat.objects.filter(seater=std_id) :
        info = []                       
        subj_id = ExamSubjectInfo.objects.get(subjName=seat.subj).subjID        
        info.append(subj_id)
        info.append(seat.subj)
        info.append(seat.roomID)
        info.append(seat.date)
        info.append(seat.time)
        arrInfo.append(info)    
    return render_to_response('student_info.html',{'std':std,'arrInfo':arrInfo,'delete_seat':True})

def deleting_seat_info_page(request, std_id, subj_name):
    ExamStudentSeat.objects.get(seater=std_id,subj=subj_name).delete()       
    return student_info_page(request, std_id) 


##############3

@csrf_exempt
def login1_page(request):  
    try:
        m = Member.objects.get(username=request.POST['username'],password = request.POST['password'])
	#request.session['member_id'] = m.id
        return HttpResponseRedirect('/admin/')
    except Member.DoesNotExist:
        return HttpResponse("Your username and password didn't match.")
        

