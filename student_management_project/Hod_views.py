from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Course, Session_Year, Student,CustomUser, Staff,Subject, Staff_Notification,Staff_Leave,Staff_Feedback, Student_Notification,Student_Feedback, Student_Leave, Attendance, Attendance_Report
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User


@staff_member_required(redirect_field_name='next', login_url='login')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()
    student_gender_other = Student.objects.filter(gender='Other').count()
    context = {
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female,
        'student_gender_other':student_gender_other
    }

    return render(request, 'Hod/home.html', context)


@staff_member_required(redirect_field_name='next', login_url='login')
def ADD_STUDENT(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    # print(course, session_year)
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        join_date = request.POST.get('join_date')
        mobile_number = request.POST.get('mobile_number')
        # print(profile_pic,first_name,last_name, username, email, password, address, gender, course_id, session_year_id, join_date, mobile_number)
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken')
            return redirect('add_student')
        else:
            user = CustomUser(first_name=first_name, last_name=last_name, username= username, email=email, profile_pic=profile_pic, user_type=3)
            user.set_password(password)
            user.save()
            course = Course.objects.get(id=course_id)
            session_year = Session_Year.objects.get(id=session_year_id)
            student = Student(admin= user, address=address, session_year_id= session_year, branch_id=course, gender=gender, join_data=join_date, mobile_number=mobile_number)
            student.save()
            messages.success(request, user.first_name+ "  " + user.last_name + " Are Successfully Added. !!!")
            return redirect('add_student')

    context = {
        'course':course,
        'session_year':session_year,
    }
    return render(request, 'Hod/add_student.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def VIEW_STUDENT(request):
    student = Student.objects.all()
    # print(student)
    context ={
        'student':student
    }
    return render(request, 'Hod/view_student.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id = id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()

    context = {
        'student':student,
        'course':course,
        'session_year':session_year
    }
    return render(request, 'Hod/edit_student.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id= request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        join_date = request.POST.get('join_date')
        mobile_number = request.POST.get('mobile_number')
        # print(profile_pic, first_name, last_name, username, email, password, address, gender, course_id,
              # session_year_id, join_date, mobile_number)
        user = CustomUser.objects.get(id = student_id)
        # user.profile_pic = profile_pic
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        if password != None and password != "":
            user.password = password
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()

        student = Student.objects.get(admin = student_id)
        student.address = address
        student.gender = gender
        course = Course.objects.get(id = course_id)
        student.branch_id = course

        session_year = Session_Year.objects.get(id = session_year_id)
        student.session_year_id = session_year

        student.join_data = join_date
        student.mobile_number = mobile_number
        student.save()
        messages.success(request, 'Data Updated is successfully. !!!')
        return redirect('view_student')
    return render(request, 'Hod/edit_student.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def DELETE_STUDENT(request, admin):
    student = CustomUser.objects.get(id = admin)
    student.delete()
    messages.success(request, 'Record is delete successfully. !!!')
    return redirect('view_student')
    return render(request, 'Hod/view_student.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def ADD_COURSE(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        # print(course_name)
        course = Course(name=course_name)
        course.save()
        messages.success(request, 'Course Add successfully. !!!')
        return redirect('add_course')
    return render(request, 'Hod/add_course.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context = {
        'course':course
    }
    return render(request, 'Hod/view_course.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def EDIT_COURSE(request,id):
    course = Course.objects.get(id=id)
    context = {
        'course':course
    }
    return render(request, 'Hod/edit_course.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def UPDATE_COURSE(request):
    if request.method == "POST":
        name = request.POST.get('course_name')
        course_id = request.POST.get('course_id')
        # print(course_name,course_id)
        course = Course.objects.get(id = course_id)
        course.name = name
        course.save()
        messages.success(request, "Course Updated Successfully !!!.")
        return redirect('view_course')
    return render(request, 'Hod/edit_course.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def DELETE_COURSE(request, id):
    course = Course.objects.get(id = id)
    course.delete()
    messages.success(request, 'Course Is deleted Successfully. !!!')
    return redirect('view_course')

@staff_member_required(redirect_field_name='next', login_url='login')
def ADD_STAFF(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        mobile_number = request.POST.get('mobile_number')

        if CustomUser.objects.filter(email= email).exists():
            messages.warning(request, 'Email is already Exists. !!!')
            return redirect('add_staff')
        if CustomUser.objects.filter(username= username).exists():
            messages.warning(request, 'Username is already Exists. !!!')
            return redirect('add_staff')
        else:
            user = CustomUser(user_type=2 ,first_name=first_name, last_name=last_name, username=username, email=email,profile_pic=profile_pic)
            user.set_password(password)
            user.save()

            staff = Staff(admin = user ,address=address, gender=gender, mobile_number=mobile_number)
            staff.save()
            messages.success(request, 'Staff Add is Successful. !!!')
            return redirect('add_staff')
        # print(profile_pic, first_name, last_name, username, email, password, address, gender, mobile_number)
    return render(request, 'Hod/add_staff.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff
    }
    return render(request, 'Hod/view_staff.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def EDIT_STAFF(request, id):
    staff = Staff.objects.get(id=id)
    context = {
        'staff':staff
    }
    return render(request, 'Hod/edit_staff.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def UPDATE_STAFF(request):
    if request.method == "POST":
        id = request.POST.get('staff_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        mobile_number = request.POST.get('mobile_number')
        profile_pic = request.POST.get('profile_pic')
        password = request.POST.get('password')

        user = CustomUser.objects.get(id = id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        if password != None and password != "":
            user.password = password
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()
        staff  = Staff.objects.get(admin=id)
        staff.address = address
        staff.gender = gender
        staff.mobile_number = mobile_number
        staff.save()
        messages.success(request, 'Staff is Updated successful. !!!')
        return redirect('view_staff')

    return render(request, 'Hod/edit_staff.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def DELETE_STAFF(request, id):
    staff = CustomUser.objects.get(id= id)
    staff.delete()
    messages.success(request, 'Staff is Deleted Successful. !!!')
    return redirect('view_staff')

    return render(request, 'Hod/view_staff.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def ADD_SUBJECT(request):
    course = Course.objects.all()
    staff = Staff.objects.all()

    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)

        subject = Subject(name = subject_name, course=course, staff= staff)
        subject.save()
        messages.success(request, "Subject Add Successfully. !!!")
        return redirect('add_subject')
    context = {
        'course': course,
        'staff': staff
    }
    return render(request, 'Hod/add_subject.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def VIEW_SUBJECT(request):
    subject = Subject.objects.all()
    context = {
        'subject':subject
    }
    return render(request, 'Hod/view_subject.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def EDIT_SUBJECT(request, id):
    subject = Subject.objects.get(id = id)
    course = Course.objects.all()
    staff = Staff.objects.all()
    context = {
        'subject': subject,
        'course':course,
        'staff':staff
    }
    return render(request, 'Hod/edit_subject.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def UPDATE_SUBJECT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
        print(subject_id,name, course_id, staff_id)
        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)

        subject = Subject.objects.get(id= subject_id)
        subject.name = name
        subject.course = course
        subject.staff = staff
        subject.save()
        messages.success(request, 'Subject Updated successful. !!!')
        return redirect('view_subject')
    return render(request, 'Hod/view_subject.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def DELETE_SUBJECT(request, id):
    subject = Subject.objects.filter(id = id)
    subject.delete()
    messages.success(request, 'Subject Deleted successfully. !!!')
    return redirect('view_subject')

@staff_member_required(redirect_field_name='next', login_url='login')
def ADD_SESSION(request):
    if request.method == "POST":
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')
        session = Session_Year(session_start=session_year_start, session_end=session_year_end)
        session.save()
        messages.success(request, "Session Add successfully.!!!")
        return redirect('add_session')
    return render(request, 'Hod/add_session.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def VIEW_SESSION(request):
    session = Session_Year.objects.all()
    return render(request, 'Hod/view_session.html', {'session':session})

@staff_member_required(redirect_field_name='next', login_url='login')
def EDIT_SESSION(request,id):
    session = Session_Year.objects.filter(id = id)
    context = {
        'session':session
    }
    return render(request, 'Hod/edit_session.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def UPDATE_SESSION(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')
        session = Session_Year(id = session_id, session_start= session_year_start, session_end = session_year_end)
        session.save()
        messages.success(request, 'Session Updated Successfully. !!!')
        return redirect('view_session')

    return render(request, 'Hod/view_session.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def DELETE_SESSION(request, id):
    session = Session_Year.objects.get(id = id)
    session.delete()
    messages.success(request, 'Session Deleted Successfully. !!!')
    return redirect('view_session')



# This is a Staff Notification
@staff_member_required(redirect_field_name='next', login_url='login')
def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification  = Staff_Notification.objects.all().order_by('-id')[0:5]
    context = {
        'staff':staff,
        'see_notification':see_notification
    }
    return render(request, 'Hod/staff_notification.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def SAVE_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')
        staff = Staff.objects.get(admin=staff_id)
        notification = Staff_Notification(staff_id = staff, message = message)
        notification.save()
        messages.success(request, 'Message Send is successfully. !!!')
        return redirect('staff_send_notification')
    return render(request, 'Hod/staff_notification.html')

@staff_member_required(redirect_field_name='next', login_url='login')
def STAFF_LEAVE_VIEW(request):
    staff_leave = Staff_Leave.objects.all()
    context = {
        'staff_leave':staff_leave
    }
    return render(request, 'Hod/staff_leave.html', context)


@staff_member_required(redirect_field_name='next', login_url='login')
def STAFF_APPROVE_LEAVE(request, id):
    leave = Staff_Leave.objects.get(id = id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')

@staff_member_required(redirect_field_name='next', login_url='login')
def STAFF_DISAPPROVE_LEAVE(request, id):
    leave =Staff_Leave.objects.get(id = id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')

@staff_member_required(redirect_field_name='next', login_url='login')
def STAFF_FEEDBACK(request):
    feedback =Staff_Feedback.objects.all()
    context={
        "feedback":feedback,
    }

    return render(request, 'Hod/staff_feedback.html',context)


@staff_member_required(redirect_field_name='next', login_url='login')
def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')
        feedback = Staff_Feedback.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        return redirect('staff_feedback_reply')

@staff_member_required(redirect_field_name='next', login_url='login')
def STUDENT_SEND_NOTIFICATION(request):
    student = Student.objects.all()
    notification = Student_Notification.objects.all()
    context={
        'student':student,
        'notification':notification,
    }

    return render(request, 'Hod/student_notification.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def SAVE_STUDENT_NOTIFICATION(request):
    if request.method == "POST":
        message = request.POST.get('message')
        student_id = request.POST.get('student_id')
        student = Student.objects.get(admin=student_id)
        stud_notification = Student_Notification(student_id=student, message=message)
        stud_notification.save()
        messages.success(request, 'Student Notification Are send Successfully !!!')
        return redirect('student_send_notification')

@staff_member_required(redirect_field_name='next', login_url='login')
def STUDENT_FEEDBACK(request):
    feedback = Student_Feedback.objects.all().order_by('-id')[0:5]
    context = {
        'feedback':feedback
    }
    return render(request, 'Hod/student_feedback.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')
        feedback = Student_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        messages.success(request, 'Reply send successfully !!!')
        return redirect('student_feedback_reply')

@staff_member_required(redirect_field_name='next', login_url='login')
def STUDENT_LEAVE_VIEW(request):
    student_leave = Student_Leave.objects.all()
    context = {
        'student_leave':student_leave
    }
    return render(request, 'Hod/student_leave.html', context)

@staff_member_required(redirect_field_name='next', login_url='login')
def STUDENT_APPROVE_LEAVE(request, id):
    leave = Student_Leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('student_leave_view')

@staff_member_required(redirect_field_name='next', login_url='login')
def STUDENT_DISAPPROVE_LEAVE(request, id):
    leave = Student_Leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    return redirect('student_leave_view')

@staff_member_required(redirect_field_name='next', login_url='login')
def VIEW_ATTENDANCE(request):
    subject = Subject.objects.all()
    session_year = Session_Year.objects.all()
    action = request.GET.get('action')

    get_session_year = None
    get_subject = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            attendance = Attendance.objects.filter(subject_id=get_subject, attendance_date=attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)
    context = {
        'subject': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'attendance_date': attendance_date,
        'attendance_report': attendance_report
    }
    return render(request, 'Hod/view_attendance.html', context)