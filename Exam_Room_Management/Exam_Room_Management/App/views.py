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
#user = User.objects.create_user('admin1','nunlek05177@hotmail.com', '1234')

def main_page(request):    
    errors = []
    if 'id' in request.GET and request.GET['id'] :
        id_tmp = request.GET['id']     
        if Student.objects.filter(stdID=id_tmp) :
            std = Student.objects.get(stdID=id_tmp)
            return render_to_response('view_student_info_page.html', {'std':std})
        else :
            errors.append('ID does not exist')                
    return render_to_response('main_page.html',{'errors':errors})
    

def login_page(request):
    errors = []  
    if ('user' in request.POST and request.POST['user'] and 'pass' in request.POST and request.POST['pass']):  
    	user_tmp = request.GET['user']  
    	pass_tmp = request.GET['pass']
	#if (user_tmp == 'admin' and pass_tmp == '1234'):
    	user = authenticate(username= user_tmp,password=pass_tmp) 
    	if user is not None:
        	if user.is_active:  
             		login(user)
	    		userDetail = request.user
             		url = request.get_host() 
             		t = get_template('admin_page.html')
    	     		html = t.render(Context({'URL': url, 'USER': userDetail }))
             		return HttpResponse('admin_page.html')   
		else : 
			errors = True 
			return render_to_response('login_page.html',{'errors':errors})
        else :
		errors = True 
             	return render_to_response('login_page.html',{'errors':errors})
    else: 
	errors = True     
        return render_to_response('login_page.html',{'errors':errors})
    

def admin_page(request): 
    return render_to_response('admin_page.html')

############################################################################################

def student_page(request):
    errors = []   
    if ( 'id' in request.GET and request.GET['id'] and
         'name' in request.GET and request.GET['name'] ) :
        id_tmp = request.GET['id']     
        name_tmp = request.GET['name']                
        if Student.objects.filter(stdID=id_tmp) :
            errors.append('ID does exist already.')                   
        else :
            add_info = Student(stdID=id_tmp,stdName=name_tmp)
            add_info.save()    
    return render_to_response('student_page.html',{'errors': errors,'stds': Student.objects.order_by('stdID')})

def student_info_page(request, std_id):
    std = Student.objects.get(stdID=std_id)        
    return render_to_response('student_info.html',{'std':std})

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
    return render_to_response('edit_std_info.html',{'std':std})

def delete_student_info_confirm_page(request, std_id):    
    std = Student.objects.get(stdID=std_id)
    return render_to_response('del_std_info.html',{'std':std})

def deleting_student_info_page(request, std_id):
    Student.objects.get(stdID=std_id).delete()    
    return render_to_response('student_page.html',{'stds':Student.objects.order_by('stdID')}) 

def add_exam_subject_page(request, std_id):    
    errors = []
    if not( 'sub_id' in request.GET and request.GET['sub_id'] ) :
        errors.append('Please select one Subject.')         
        return render_to_response('add_exam_subj.html',{'errors': errors})
    sub_id = request.GET['sub_id']
    if not Subject.objects.filter(subID=sub_id) :
        errors.append('Subject does not found.')         
        return render_to_response('add_exam_subj.html',{'errors': errors})
    std = Student.objects.get(stdID=std_id)    
    for info in std.examInfo :
        for i in info :
            if i.__contains__(sub_id) :
                errors.append('Subject does exist already.')         
                return render_to_response('add_exam_subj.html',{'errors': errors})
    sub = Subject.objects.get(subID=sub_id)
    rooms = Exam_Room.objects.order_by('roomID')
    exist_room = []
    empty_room = []
    for room in rooms :
        if room.subA_timeA == sub_id and not room.isSeatATimeAFull() :
            exist_room = [room,'AA']
        elif room.subA_timeB == sub_id and not room.isSeatATimeBFull():
            exist_room = [room,'AB']    
        elif room.subB_timeA == sub_id and not room.isSeatBTimeAFull():
            exist_room = [room,'BA']
        elif room.subB_timeB == sub_id and not room.isSeatBTimeBFull():
            exist_room = [room,'BB']        
        if room.subA_timeA == 'Empty' and room.subB_timeA != sub_id :
            empty_room = [room,'AA']
        elif room.subA_timeB == 'Empty' and room.subB_timeB != sub_id :
            empty_room = [room,'AB']
        elif room.subB_timeA == 'Empty' and room.subA_timeA != sub_id :
            empty_room = [room,'BA']
        elif room.subB_timeB == 'Empty' and room.subA_timeB != sub_id :
            empty_room = [room,'BB']
    if exist_room.__len__() > 0 :
        info = []
        if exist_room[1] == 'AA' :
            exist_room[0].seatA_timeA.append(std)
            info = [sub.subID,sub.subName,exist_room[0].roomID,exist_room[0].timeA]
        elif exist_room[1] == 'AB' :
            exist_room[0].seatA_timeB.append(std)
            info = [sub.subID,sub.subName,exist_room[0].roomID,exist_room[0].timeB]
        elif exist_room[1] == 'BA' :
            exist_room[0].seatB_timeA.append(std)
            info = [sub.subID,sub.subName,exist_room[0].roomID,exist_room[0].timeA]
        else :
            exist_room[0].seatB_timeB.append(std)
            info = [sub.subID,sub.subName,exist_room[0].roomID,exist_room[0].timeB]
        std.examInfo.append(info)
        exist_room[0].save()
        std.save()
        sub.stdList.append(std)        
        sub.save()
        return student_info_page(std_id)
    elif empty_room.__len__() > 0 :
        info = []
        if empty_room[1] == 'AA' :
            empty_room[0].subA_timeA = sub.subID
            empty_room[0].seatA_timeA.append(std)
            info = [sub.subID,sub.subName,exist_room[0].roomID,exist_room[0].timeA]
        elif empty_room[1] == 'AB' :
            empty_room[0].subA_timeB = sub.subID
            empty_room[0].seatA_timeB.append(std)
            info = [sub.subID,sub.subName,exist_room[0].roomID,exist_room[0].timeB]
        elif empty_room[1] == 'BA' :
            empty_room[0].subB_timeA = sub.subID
            empty_room[0].seatB_timeA.append(std)
            info = [sub.subID,sub.subName,exist_room[0].roomID,exist_room[0].timeA]
        else :
            empty_room[0].subB_timeB = sub.subID
            empty_room[0].seatB_timeB.append(std)
            info = [sub.subID,sub.subName,exist_room[0].roomID,exist_room[0].timeB]        
        std.examInfo.append(info)        
        exist_room[0].save()
        std.save()
        sub.stdList.append(std)
        sub.roomList.append(exist_room[0])
        sub.save()
        return student_info_page(std_id)
    else :
        errors.append('All room are full, please contact Staff')   
        return render_to_response('add_exam_subj.html',{'errors': errors})   

def subject_page(request):
    errors = []   
    if ( 'id' in request.GET and request.GET['id'] and
         'name' in request.GET and request.GET['name'] ) :
        id_tmp = request.GET['id']     
        name_tmp = request.GET['name']                
        if Subject.objects.filter(subID=id_tmp) :
            errors.append('ID does exist already.')                   
        else :
            add_info = Subject(subID=id_tmp,subName=name_tmp)
            add_info.save()            
    return render_to_response('subject_page.html',{'errors': errors,'subs': Subject.objects.order_by('subID')})

def subject_info_page(request, sub_id):
    sub = Subject.objects.get(subID=sub_id)
    return render_to_response('subject_info.html',{'sub':sub})

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
    return render_to_response('edit_subj_info.html',{'sub':sub})

def delete_subject_info_confirm_page(request, sub_id):    
    sub = Subject.objects.get(subID=sub_id)
    return render_to_response('del_subj_info.html',{'sub':sub})

def deleting_subject_info_page(request, sub_id):
    Subject.objects.get(subID=sub_id).delete()      
    return render_to_response('subject_page.html',{'subs':Subject.objects.order_by('subID')})

def room_page(request):
    errors = []   
    if ( 'id' in request.GET and request.GET['id'] and
         'size' in request.GET and request.GET['size'] ) :
        id_tmp = request.GET['id']     
        size_tmp = int(request.GET['size'])             
        if Exam_Room.objects.filter(roomID=id_tmp) :
            errors.append('ID does exist already.')                   
        else :
            add_info = Exam_Room(roomID=id_tmp,size=size_tmp)
            add_info.save()        
    else :
        errors.append('You must fill in all of the fields, if you want to add information.')
    return render_to_response('room_page.html',{'errors': errors,'rooms': Exam_Room.objects.order_by('roomID')})

def room_info_page(request, room_id):
    room = Exam_Room.objects.get(roomID=room_id)
    return render_to_response('room_info.html',{'room':room})

def add_exam_room_page(request, room_id): 
    errors = []           
    if ( 'timeA' in request.GET and request.GET['timeA']
         and 'subA_timeA' in request.GET and request.GET['subA_timeA']
         and 'subB_timeA' in request.GET and request.GET['subB_timeA']
         and 'timeB' in request.GET and request.GET['timeB']
         and 'subA_timeB' in request.GET and request.GET['subA_timeB']
         and 'subB_timeB' in request.GET and request.GET['subB_timeB'] ) :        
        timeA = request.GET['timeA']
        subA_timeA = request.GET['subA_timeA']
        subB_timeA = request.GET['subB_timeA']
        timeB = request.GET['timeB']
        subA_timeB = request.GET['subA_timeB']
        subB_timeB = request.GET['subB_timeB']
        if timeA == timeB :
            errors.append('Time 1 is the same as Time 2.') 
        elif subA_timeA == subB_timeA and subA_timeA != 'Empty':
            errors.append('In time 1, Subject 1 is the same as Subject 2.')            
        elif subA_timeB == subB_timeB and subA_timeB != 'Empty':
            errors.append('In time 2, Subject 1 is the same as Subject 2.')            
        else :
            room = Exam_Room.objects.get(roomID=room_id)
            room.timeA = timeA
            room.subA_timeA = subA_timeA
            room.subB_timeA = subB_timeA
            room.timeB = timeB
            room.subA_timeB = subA_timeB
            room.subB_timeB = subB_timeB
            room.save()            
            return room_page()       
    return render_to_response('add_exam_room.html',{'errors':errors,'subs': Subject.objects.order_by('subID'),'roomID':room_id})

def edit_room_info_page(request, room_id):
    room = Exam_Room.objects.get(roomID=room_id)
    if ( 'id' in request.GET and request.GET['id'] ) :
        new_id = request.GET['id']
        room.roomID = new_id
        room.save()
    if ( 'size' in request.GET and request.GET['size'] ) :
        new_size = int(request.GET['size'])
        room.size = new_size
        room.save()
    return render_to_response('edit_room_info.html',{'room':room})

def delete_room_info_confirm_page(request, room_id):    
    room = Exam_Room.objects.get(roomID=room_id)
    return render_to_response('del_room_info.html',{'room':room})

def deleting_room_info_page(request, room_id):
    Exam_Room.objects.get(roomID=room_id).delete()    
    return render_to_response('room_page.html',{'rooms':Exam_Room.objects.order_by('roomID')}) 
