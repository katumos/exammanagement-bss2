from Exam_Room_Management.App.models import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect


def main_page(request):
    errors = []
    if 'id' in request.GET and request.GET['id']:
        id_tmp = request.GET['id']
        if Student.objects.filter(stdID=id_tmp):
            std = Student.objects.get(stdID=id_tmp)
            return render_to_response('view_student_info_page.html', \
                                      {'std': std})
        else:
            errors.append('ID does not exist')
    return render_to_response('main_page.html', {'errors': errors})


def login_page(request):
    errors = []
    if ('user' in request.GET and request.GET['user']
        and 'pass' in request.GET and request.GET['pass']):
        user_tmp = request.GET['user']
        pass_tmp = request.GET['pass']
        if (user_tmp == 'admin' and pass_tmp == '1234'):
            return render_to_response('admin_page.html')
        else:
            errors.append('Invalid!')
    return render_to_response('login_page.html', {'errors': errors})


def admin_page(request):
    return render_to_response('admin_page.html')


def student_page(request):
    errors = []
    if ('id' in request.GET and request.GET['id'] and
        'name' in request.GET and request.GET['name']):
        id_tmp = request.GET['id']
        name_tmp = request.GET['name']
        if Student.objects.filter(stdID=id_tmp):
            errors.append('ID does exist already.')
        else:
            add_info = Student(stdID=id_tmp, stdName=name_tmp)
            add_info.save()
    else:
        errors.append('You must fill in all of the fields, \
        if you want to add information.')
    return render_to_response('student_page.html', \
        {'errors': errors, 'stds': Student.objects.order_by('stdID')})


def student_info_page(request, std_id):
    std = Student.objects.get(stdID=std_id)
    return render_to_response('student_info_page.html', {'std': std})


def edit_student_info_page(request, std_id):
    std = Student.objects.get(stdID=std_id)
    if ('id' in request.GET and request.GET['id']):
        new_id = request.GET['id']
        std.stdID = new_id
        std.save()
    if ('name' in request.GET and request.GET['name']):
        new_name = request.GET['name']
        std.stdName = new_name
        std.save()
    return render_to_response('edit_student_info_page.html', {'std': std})


def delete_student_info_confirm_page(request, std_id):
    std = Student.objects.get(stdID=std_id)
    return render_to_response('delete_student_info_confirm_page.html', \
    {'std': std})


def deleting_student_info_page(request, std_id):
    Student.objects.get(stdID=std_id).delete()
    return render_to_response('student_page.html', \
    {'stds': Student.objects.order_by('stdID')})


def subject_page(request):
    errors = []
    if ('id' in request.GET and request.GET['id'] and
        'name' in request.GET and request.GET['name']):
        id_tmp = request.GET['id']
        name_tmp = request.GET['name']
        if Subject.objects.filter(subID=id_tmp):
            errors.append('ID does exist already.')
        else:
            add_info = Subject(subID=id_tmp, subName=name_tmp)
            add_info.save()
    else:
        errors.append('You must fill in all of the fields,\
         if you want to add information.')
    return render_to_response('subject_page.html', \
    {'errors': errors, 'subs': Subject.objects.order_by('subID')})


def subject_info_page(request, sub_id):
    sub = Subject.objects.get(subID=sub_id)
    return render_to_response('subject_info_page.html', {'sub': sub})


def edit_subject_info_page(request, sub_id):
    sub = Subject.objects.get(subID=sub_id)
    if ('id' in request.GET and request.GET['id']):
        new_id = request.GET['id']
        sub.subID = new_id
        sub.save()
    if ('name' in request.GET and request.GET['name']):
        new_name = request.GET['name']
        sub.subName = new_name
        sub.save()
    return render_to_response('edit_subject_info_page.html', {'sub': sub})


def delete_subject_info_confirm_page(request, sub_id):
    sub = Subject.objects.get(subID=sub_id)
    return render_to_response('delete_subject_info_confirm_page.html',\
    {'sub': sub})


def deleting_subject_info_page(request, sub_id):
    Subject.objects.get(subID=sub_id).delete()
    return render_to_response('subject_page.html', \
    {'subs': Subject.objects.order_by('subID')})


def room_page(request):
    errors = []
    if ('id' in request.GET and request.GET['id'] and
         'size' in request.GET and request.GET['size']):
        id_tmp = request.GET['id']
        size_tmp = int(request.GET['size'])
        if ExamRoom.objects.filter(roomID=id_tmp):
            errors.append('ID does exist already.')
        else:
            add_info = ExamRoom(roomID=id_tmp, size=size_tmp,\
             subA='Empty', subB='Empty')
            add_info.save()
    else:
        errors.append('You must fill in all of the fields, \
        if you want to add information.')
    return render_to_response('room_page.html', \
    {'errors': errors, 'rooms': ExamRoom.objects.order_by('roomID')})


def room_info_page(request, room_id):
    room = ExamRoom.objects.get(roomID=room_id)
    return render_to_response('room_info_page.html', {'room': room})


def edit_room_info_page(request, room_id):
    room = ExamRoom.objects.get(roomID=room_id)
    if ('id' in request.GET and request.GET['id']):
        new_id = request.GET['id']
        room.roomID = new_id
        room.save()
    if ('size' in request.GET and request.GET['size']):
        new_size = int(request.GET['size'])
        room.size = new_size
        room.save()
    return render_to_response('edit_room_info_page.html', {'room': room})


def delete_room_info_confirm_page(request, room_id):
    room = ExamRoom.objects.get(roomID=room_id)
    return render_to_response('delete_room_info_confirm_page.html', \
    {'room': room})


def deleting_room_info_page(request, room_id):
    ExamRoom.objects.get(roomID=room_id).delete()
    return render_to_response('room_page.html', \
    {'rooms': ExamRoom.objects.order_by('roomID')})


def sorting_Examroom(request, std_id, room_id, sub_id):
    return render_to_response('sorting_page.html', \
    {'rooms': ExamRoom.objects.order_by('roomID')})
