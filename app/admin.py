from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import *
from django.contrib.auth.admin import UserAdmin

#er your models here.





class UserModel(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'user_type', 'profile_pic', 'is_staff']

admin.site.register(CustomUser,UserModel)

@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']


@admin.register(Session_Year)
class SessionYearModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_start', 'session_end']

@admin.register(Student)
class StudentModelAdmin(admin.ModelAdmin):
    model = Student
    list_display = ['id', 'address', 'gender', 'join_data', 'mobile_number']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'gender', 'mobile_number', 'created_at']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'course', 'created_at']


@admin.register(Staff_Notification)
class StaffNotiAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff_id', 'message', 'created_at', 'status']



class StaffLeaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff_id', 'date', 'status', 'created_at', 'message']

admin.site.register(Staff_Leave, StaffLeaveAdmin)


@admin.register(Staff_Feedback)
class StaffFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff_id', 'feedback', 'feedback_reply', 'status', 'created_at']

@admin.register(Student_Notification)
class StudentNoti(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'message', 'created_at', 'status']


@admin.register(Student_Feedback)
class StudentFeedback(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'feedback', 'feedback_reply', 'status', 'created_at']

@admin.register(Student_Leave)
class StudentLeaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'date', 'status', 'created_at', 'message']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject_id', 'attendance_date', 'session_year_id', 'created_at']

@admin.register(Attendance_Report)
class AttReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'created_at', 'updated_at']

@admin.register(StudentResult)
class StudentResult(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'assignment_mark', 'exam_mark', 'created_at', 'updated_at']