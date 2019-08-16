from django.urls import path
from . import views
from django.urls import path, include 
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('login', include('django.contrib.auth.urls'), name='login'),
    path('<int:year>',views.List, name='year'),
    path('practical_select/<int:id>',views.practical_send, name='practical_select'),
    path('students',views.students, name='students'),
    path('s/<int:id>',views.students_list, name='s'),
    path('data/<student>',views.student_mark, name='data'),
]
