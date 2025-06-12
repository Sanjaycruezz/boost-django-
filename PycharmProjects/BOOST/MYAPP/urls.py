from django.contrib import admin
from django.urls import path, include

from MYAPP import views

urlpatterns = [
    path('',views.login),
    path('logout',views.logout),
    path('view_tips',views.view_tips),
    path('view_tips_delete/<id>',views.view_tips_delete),
    path('edit_tip/<id>', views.edit_tip),
    path('edit_tip_post', views.edit_tip_post),
    path('view_complaints',views.view_complaints),
    path('view_feedback',views.view_feedback),
    path('view_user',views.view_user),
    path('loginnew',views.loginnew),
    path('home_page', views.home_page),
    path('add_tip', views.add_tip),
    path('add_tip_post', views.add_tip_post),
    path('reply/<id>', views.reply),
    path('reply_post',views.reply_post),



    path('android_login',views.android_login),
    path('view_profile',views.view_profile),
    path('/ViewMyComplaints', views.ViewMyComplaints),
    path('/SendAppComplaint', views.SendAppComplaint),
    path('/DeleteMyComplaint', views.DeleteMyComplaint),
    path('viewfeedback', views.viewfeedback),
    path('sendfeedback', views.sendfeedback),
    path('/registrationcode',views.registrationcode),
    path('/diet_plan', views.diet_plan),
    path('/workout_plan', views.workout_plan),
    path('/get_user_details', views.get_user_details),
    path('/update_profile',views.update_profile),
    path('/chatbot_response', views.chatbot_response),
    path('/workbot_response',views.workbot_response),
    path('/dietbot_response',views.diet_plan),
    path('getbmi',views.getbmi),
    path('forgot_password_flutter',views.forgot_password_flutter),
    path('/change_password',views.change_password),
    path('web_change_password', views.web_change_password),
    path('/upload_image', views.upload_image),
    path('forgot_password_web', views.forgot_password_web),
    path('user_home_page', views.user_home_page),
    path('view_user_excercise_information', views.view_user_excercise_information),
    path('excercises', views.excercises),
    path('biceps',views.biceps),
    path('lunges', views.lunges),
    path('plank', views.plank),
    path('squat', views.squat),
    path('update_count', views.update_count),
]
