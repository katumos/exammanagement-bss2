from Exam_Room_Management.App.models import ExamStudentInfo, ExamSubjectInfo, ExamRoomInfo, ExamStudentSeat
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout

#from django.contrib.auth.models import User
#user = User.objects.create_user('admin1', 'firstray505@gmail.com', '1234')
#user.is_active = True
#user.save()

def main_page(request):    
    errors = []
    if 'id' in request.GET and request.GET['id'] :
        id_tmp = request.GET['id']     
        if ExamStudentInfo.objects.filter(stdID=id_tmp) :
            std = ExamStudentInfo.objects.get(stdID=id_tmp)
            arrInfo = []          
            for seat in  ExamStudentSeat.objects.filter(seater=id_tmp) :
                info = []                       
                subj_id = ExamSubjectInfo.objects.get(subjName=seat.subj).subjID        
                info.append(subj_id)
                info.append(seat.subj)
                info.append(seat.roomID)
                info.append(seat.date)
                info.append(seat.time)
                arrInfo.append(info)
            return render_to_response('view_std_info.html',{'std':std,'arrInfo':arrInfo})
        else :
            errors.append('ID does not exist')                
    return render_to_response('main_page.html',{'errors':errors})

def login_page(request): 
    errors = []
    if ( 'username' in request.GET and request.GET['username']
         and 'password' in request.GET and request.GET['password'] ):
        user_tmp = request.GET['username']
        pass_tmp = request.GET['password']    
        user = authenticate(username=user_tmp, password=pass_tmp)
        if user is not None:
            if user.is_active:
                login(request, user)   
                return admin_page(request)       
            else:
                errors.append('User is not active.')
        else:
            errors.append('Invalid username or passwaord.')
    else :
        errors.append('Please login.')
    return render_to_response('login_page.html',{'errors':errors})

def logout_page(request):    
    if not request.user.is_authenticated():        
        return login_page(request)
    logout(request)    
    return login_page(request)

def admin_page(request):    
    if not request.user.is_authenticated():        
        return login_page(request)
    return render_to_response('admin_page.html')

def student_page(request):
    errors = []
    if not request.user.is_authenticated():        
        return login_page(request)       
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
    if not request.user.is_authenticated():        
        return login_page(request)
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
    errors = []
    if not request.user.is_authenticated():        
        return login_page(request)
    std = ExamStudentInfo.objects.get(stdID=std_id)
    if ( 'id' in request.GET and request.GET['id'] ) :
        new_id = request.GET['id']
        if not ExamStudentInfo.objects.filter(stdID=new_id):
            std.stdID = new_id
            std.save()
        else :
            errors.append('ID does exist already.')
    if ( 'name' in request.GET and request.GET['name'] ) :
        new_name = request.GET['name']
        if not ExamStudentInfo.objects.filter(stdName=new_name):
            std.stdName = new_name
            std.save()
        else :
            errors.append('Name does exist already.')
    return render_to_response('edit_std_info.html',{'std':std,'errors':errors})

def delete_student_info_confirm_page(request, std_id):
    if not request.user.is_authenticated():        
        return login_page(request)         
    std = ExamStudentInfo.objects.get(stdID=std_id)
    return render_to_response('student_info.html',{'std':std,'deleting':True})

def deleting_student_info_page(request, std_id):
    if not request.user.is_authenticated():        
        return login_page(request)
    ExamStudentInfo.objects.get(stdID=std_id).delete()
    for seat in ExamStudentSeat.objects.filter(seater=std_id):
        room = ExamRoomInfo.objects.get(roomID=seat.roomID,subj=seat.subj,date=seat.date,time=seat.time)        
        room.size = room.size - 1
        room.save()
    ExamStudentSeat.objects.filter(seater=std_id).delete() 
    return student_page(request) 

def add_exam_subject_page(request, std_id):
    errors = []
    if not request.user.is_authenticated():        
        return login_page(request)        
    std = ExamStudentInfo.objects.get(stdID=std_id)
    if 'subj' in request.GET and request.GET['subj'] :
        subj_name = request.GET['subj']         
        if ExamStudentSeat.objects.filter(seater=std_id,subj=subj_name) :
            errors.append('Subject does exist already.')
        else :            
            for room in ExamRoomInfo.objects.filter(subj=subj_name) :                
                seat = ExamStudentSeat(seater=std_id,subj=subj_name,roomID=room.roomID,time=room.time,date=room.date)
                seat.save() 
                room.size = room.size + 1
                room.save()                    
                return student_info_page(request, std_id)
                break                
    return render_to_response('add_exam_subj.html',{'errors': errors,'stdID':std.stdID,'subjs': getAvailableSubject(std_id)})

def isRoomFull(room_id, date, time, subj):    
    room = ExamRoomInfo.objects.get(roomID=room_id,date=date,time=time,subj=subj)
    if room.size == room.capacity :
        return True
    else :
        return False
    
def isSameTime(std_id, room_id, date, time):    
    if ExamStudentSeat.objects.filter(seater=std_id,date=date,time=time) :
        return True
    else :
        return False
        
def getAvailableSubject(std_id):
    ava_sub = []
    rooms = ExamRoomInfo.objects.order_by('roomID')    
    for room in rooms :
        cur = ExamSubjectInfo.objects.get(subjName=room.subj)
        if not ( ava_sub.__contains__(cur) or isRoomFull(room.roomID,room.date,room.time,room.subj) 
                 or isSameTime(std_id,room.roomID,room.date,room.time) ) :
            ava_sub.append(cur)
    return ava_sub


def subject_page(request):
    errors = []
    if not request.user.is_authenticated():        
        return login_page(request)       
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
    if not request.user.is_authenticated():        
        return login_page(request)
    subj = ExamSubjectInfo.objects.get(subjID=subj_id)
    return render_to_response('subject_info.html',{'subj':subj})

def edit_subject_info_page(request, subj_id):
    errors = []
    if not request.user.is_authenticated():        
        return login_page(request)
    subj = ExamSubjectInfo.objects.get(subjID=subj_id)
    if ( 'id' in request.GET and request.GET['id'] ) :
        new_id = request.GET['id']
        if not ExamSubjectInfo.objects.filter(subjID=new_id):
            subj.subjID = new_id
            subj.save()
        else :
            errors.append('ID does exist already.')
    if ( 'name' in request.GET and request.GET['name'] ) :
        new_name = request.GET['name']
        if not ExamSubjectInfo.objects.filter(subjName=new_name):
            subj.subjName = new_name
            subj.save()
        else :
            errors.append('Name does exist already.')
    return render_to_response('edit_subj_info.html',{'subj':subj,'errors':errors})

def delete_subject_info_confirm_page(request, subj_id):
    if not request.user.is_authenticated():        
        return login_page(request)    
    subj = ExamSubjectInfo.objects.get(subjID=subj_id)
    return render_to_response('subject_info.html',{'subj':subj,'deleting':True})

def deleting_subject_info_page(request, subj_id):
    if not request.user.is_authenticated():        
        return login_page(request)
    subj = ExamSubjectInfo.objects.get(subjID=subj_id)
    ExamStudentSeat.objects.filter(subj=subj.subjName).delete()
    ExamRoomInfo.objects.filter(subj=subj.subjName).delete()
    subj.delete()
    return subject_page(request)

def room_page(request):
    errors = []
    if not request.user.is_authenticated():        
        return login_page(request)
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
        if ExamRoomInfo.objects.filter(roomID=id_tmp,date=date,time=time,subj=subj) :             
            errors.append('Room does exist already.')
        elif ExamRoomInfo.objects.filter(roomID=id_tmp,date=date,time=time).__len__() >= 2 :             
            errors.append('Room is full.')
        elif ExamRoomInfo.objects.filter(subj=subj) and not ExamRoomInfo.objects.filter(date=date,time=time):             
            errors.append('Same Subject must have same time.')         
        elif ExamRoomInfo.objects.filter(roomID=id_tmp,subj=subj) :             
            errors.append('Subject does exist already.')                         
        else :
            add_info = ExamRoomInfo(roomID=id_tmp,size=0,capacity=15,date=date,time=time,subj=subj)
            add_info.save()
            return room_page(request)
    return render_to_response('room_page.html',{'errors': errors,'days':range(2,32),'months':range(2,13),
                                                'rooms': ExamRoomInfo.objects.order_by('roomID'),
                                                'subjs': ExamSubjectInfo.objects.order_by('subjID')})

def room_info_page(request, room_id, date, time, subj):
    if not request.user.is_authenticated():        
        return login_page(request) 
    room = ExamRoomInfo.objects.get(roomID=room_id,date=date,time=time,subj=subj)    
    return render_to_response('room_info.html',{'room':room})
    
def edit_room_info_page(request, room_id, date, time, subj):
    errors = []
    if not request.user.is_authenticated():        
        return login_page(request)
    room = ExamRoomInfo.objects.get(roomID=room_id,date=date,time=time,subj=subj)
    if ( 'id' in request.GET and request.GET['id'] ) :
        new_id = request.GET['id']
        if not ExamRoomInfo.objects.filter(roomID=new_id):
            room.roomID = new_id
            room.save()
        else :
            errors.append('ID does exist already.')
    if ( 'cap' in request.GET and request.GET['cap'] ) :
        new_cap = int(request.GET['cap'])
        room.capacity = new_cap
        room.save()    
    return render_to_response('edit_room_info.html',{'room':room})

def delete_room_info_confirm_page(request, room_id, date, time, subj):
    if not request.user.is_authenticated():        
        return login_page(request)
    room = ExamRoomInfo.objects.get(roomID=room_id,date=date,time=time,subj=subj)
    return render_to_response('room_info.html',{'room':room,'deleting':True})

def deleting_room_info_page(request, room_id, date, time, subj):
    if not request.user.is_authenticated():        
        return login_page(request)
    ExamRoomInfo.objects.get(roomID=room_id,date=date,time=time,subj=subj).delete()    
    return room_page(request)

def deleting_seat_info_page(request, std_id, subj_name, room_id):
    if not request.user.is_authenticated():        
        return login_page(request)
    ExamStudentSeat.objects.get(seater=std_id,subj=subj_name).delete()  
    room = ExamRoomInfo.objects.get(roomID=room_id, subj=subj_name)  
    room.size = room.size - 1
    room.save()   
    return student_info_page(request, std_id) 

def view_seat_info_page(request, room_id, date, time):    
    subj = []       
    iSubj = [0,5,10,
             1,6,11,
             2,7,12,
             3,8,13,
             4,9,14]       
    seatSubjA = []
    seatSubjB = []
    if not ExamRoomInfo.objects.filter(roomID=room_id,date=date,time=time):
        return render_to_response('seat.svg',{'error':True})
    for room in ExamRoomInfo.objects.filter(roomID=room_id,date=date,time=time):
        subj.append(room.subj)
    for seat in ExamStudentSeat.objects.filter(roomID=room_id,date=date,time=time).order_by('seater'):
        if seat.subj == subj[0] :
            seatSubjA.append(seat.seater)            
        else :
            seatSubjB.append(seat.seater)
    while seatSubjA.__len__() < 15 :
        seatSubjA.append('-')
    while seatSubjB.__len__() < 15 :
        seatSubjB.append('-')      
    count = 0
    rectPos = []    
    y = 100    
    for i in range(0,5):
        x = -50
        y = y + 80
        row_pos = []        
        for j in range(0,6):
            pos = []
            x = x + 130 + (i*0) #used i
            pos.append(x)
            pos.append(y)
            pos.append(x+5)
            pos.append(y+28)
            if j % 2 == 0 :                
                pos.append(seatSubjA[iSubj[count]])
            else : 
                pos.append(seatSubjB[iSubj[count]])
                count = count + 1
            row_pos.append(pos)                    
        rectPos.append(row_pos)   
    subjA = []
    subjB = []
    if ExamSubjectInfo.objects.filter(subjName=subj[0]):
        subjA = ExamSubjectInfo.objects.get(subjName=subj[0])  
    if subj.__len__() > 1 :      
        if ExamSubjectInfo.objects.filter(subjName=subj[1]) :
            subjB = ExamSubjectInfo.objects.get(subjName=subj[1])    
    return render_to_response('seat.svg',{'rectPos':rectPos,'roomID':room_id,'date':date,'time':time,
                                          'subjA':subjA,'subjB':subjB})
