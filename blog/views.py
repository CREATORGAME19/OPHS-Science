from django.shortcuts import render
from .models import Practical
from .models import Technician
from .models import Year
from .models import Subject
from .models import Calendar
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from .forms import SetForm
from .forms import FilterForm
from .forms import CalendarForm
from datetime import datetime
import datetime
import random
import os
import time
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Period
def post_list(request):
    if not request.user.is_anonymous:
        year = Year.objects.all()
        if request.method == 'POST':
            form = CalendarForm(request.POST)
            if form.is_valid():
                date = request.POST.get('date')
                subject = request.POST.getlist('subject')
                technician = request.POST.getlist('technician')
                allowed_id = []
                datetimes = []
                rooms = []
                practicals = []
                technicians = []
                teachers = []
                sets = []
                prints = []
                times = []
                low_item = 0
                for i in Calendar.objects.all():
                    t_date1 = datetime.datetime.strptime(str(i.datetime), '%d/%m/%Y %H:%M')
                    t_date = datetime.date(t_date1.year,t_date1.month,t_date1.day)
                    date = datetime.datetime.strptime(str(date), '%d/%m/%Y')
                    date1 = datetime.date(date.year,date.month,date.day)
                    
                    if t_date == date1:
                        allowed_id.append(i.id)
                        times.append(datetime.time(t_date1.hour,t_date1.minute))
                    date = request.POST.get('date')
                for i in Calendar.objects.all():
                    if i.id in allowed_id:
                        for n in Practical.objects.all():
                            if n.title == i.practical:
                                if n.subject_tag in subject:
                                    for m in Technician.objects.all():
                                        if str(m.id) in technician:
                                            if m.name == i.technician:
                                                datetimes.append(i.datetime)
                                                rooms.append(i.room)
                                                practicals.append(i.practical)
                                                technicians.append(i.technician)
                                                teachers.append(i.teacher)
                                                sets.append(i.sets)
                                                prints.append(i.prints)
                for i in range(len(times)):
                    for j in range(0, len(times)-i-1):
                        if times[j] > times[j+1]:
                            t_time = times[j]
                            t_room = rooms[j]
                            t_set = sets[j]
                            t_print = prints[j]
                            t_practical = practicals[j]
                            t_datetime = datetimes[j]
                            t_teacher = teachers[j]
                            t_technician = technicians[j]
                            times[j] = times[j+1]
                            rooms[j] = rooms[j+1]
                            sets[j] = sets[j+1]
                            prints[j] = prints[j+1]
                            practicals[j] = practicals[j+1]
                            datetimes[j] = datetimes[j+1]
                            technicians[j] = technicians[j+1]
                            teachers[j] = teachers[j+1]
                            times[j+1] = t_time
                            rooms[j+1] = t_room
                            sets[j+1] = t_set
                            prints[j+1] = t_print
                            practicals[j+1] = t_practical
                            technicians[j+1] = t_technician
                            teachers[j+1] = t_teacher
                            datetimes[j+1] = t_datetime
                data = "<ol>"
                for i in range(len(sets)):
                    data = data+"<li><center><table width='25%'><tr><td>Practical</td><td>"+str(practicals[i])+"</td></tr><tr><td>Time</td><td>"+str(times[i])+"</td></tr><tr><td>Sets</td><td>"+str(sets[i])+"</td></tr><tr><td>Prints</td><td>"+str(prints[i])+"</td></tr><tr><td>Room</td><td>"+str(rooms[i])+"</td></tr><tr><td>Technician</td><td>"+str(technicians[i])+"</td></tr><tr><td>Teacher</td><td>"+str(teachers[i])+"</td></tr></table></center></li><br>"
                if len(sets) == 0:
                    data = "<p id='main'>Woohoo! Nothing is reserved!</p>"
                #prin()
                return HttpResponse("<html><head><style>#header /*Styles for Header*/{padding: 15px;color: #ffffff;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 24px;background-color: #00ddff;}#main {font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 18px;}#button {background-color: white;color: black;border: 2px #e7e7e7;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;border-radius: 5px;}#button:hover {background-color: #e7e7e7; color: black;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;}#button1 {background-color: white;color: black;border: 2px solid #e7e7e7;width=\"50%\"font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;border-radius: 5px;}#button1:hover {background-color: #e7e7e7; color: black;width=\"50%\"font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;}#title {font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 24px;}table, th, td {border: 2px solid black;}ol {text-align: center;list-style-position: inside;}</style><title>OPHS Science Request System</title></head><body><div><center><a href=\"/\"><h1 id=\"header\">OPHS Science Request System</h1></a></center></div><center><a href=\"/\" id=\"button\">Click here to return back to the home page</a><br><h5 id=\"main\">Date: "+str(date)+"</h5><br><h3 id=\"main\">Reserved Slots:</h3><div id='main'><br><center>"+str(data)+"</ol></center><br>")
        else:
            form = CalendarForm()
        return render(request, 'blog/post_list.html', {
            'form':form,
            'year':year,
        })
    else:
        return render(request, 'blog/post_list.html')

def login(request):
    return render(request, 'blog/login.html')

def List(request, year):
    allowed_task = []
    for i in Practical.objects.all():
        if str(i.year_tag) == str(year):
            allowed_task.append(i.id)
        elif str(i.year_tag) == "":
            allowed_task.append(i.id)
    #prin()

    if request.method == 'POST':
        form = FilterForm(request.POST)
        subject = request.POST.getlist('subject')
        allowed_task = []
        for i in Practical.objects.all():
            if str(i.year_tag) == str(year):
                if str(i.subject_tag) in subject:
                    allowed_task.append(i.id)
        #prin()

    else:
        form = FilterForm()
    if len(allowed_task) == 0:
        allowed_task.append(4)
    tasks = Practical.objects.filter(id__in=allowed_task)
    return render(request, 'blog/task.html', {
        'tasks':tasks,
        'form':form,
    })

def practical_send(request, id):
    allowed_task = []
    for i in Practical.objects.all():
        if str(i.id) == str(id):
            allowed_task.append(i.id)
    data = Practical.objects.filter(id__in=allowed_task)
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            time = request.POST.get('time')
            period_id = request.POST.get('period')
            sets = request.POST.get('sets')
            prints = request.POST.get('prints')
            recipient_id = request.POST.get('technician')
            comments = request.POST.get('additional_comments')
            room = request.POST.get('room')
            if comments == "":
                comments = "(none)"
            recipient = []
            recipient_email = ''
            for i in Period.objects.all():
                if i.id == int(period_id):
                    period = i.title
                    period_time = i.time
            for i in Technician.objects.all():
                if i.id == int(recipient_id):
                    recipient_name = i.name
                    recipient_email = i.email
            recipient.append(recipient_email)
            for i in Practical.objects.all():
                if str(i.id) == str(id):
                    practical_name = i.title
                    practical_worksheet = i.link
                    practical_needs = i.thingsneeded
            username = request.user.username
            subject = "Practical:"+str(practical_name)+' has been requested by '+str(username)+'!'
            message = "On "+str(time)+" at "+str(period)+" the person "+str(username)+" has requested "+str(sets)+" sets of the practical (In the room "+str(room)+") "+str(practical_name)+" and "+str(prints)+" prints of the worksheet(Link: "+str(practical_worksheet)+")! Things needed for practical: "+str(practical_needs)+". Additional comments: "+str(comments)
            #prin()
            send_mail(
                subject,
                message,
                'ophsrequest@gmail.com',
                recipient,
                fail_silently=False,
            )
            dtime = str(time)+" "+str(period_time)
            calendar = Calendar.objects.create(datetime=dtime,room=room,practical=practical_name,technician=recipient_name,teacher=username,sets=sets,prints=prints)
            return HttpResponse("<html><head><style>#header /*Styles for Header*/{padding: 15px;color: #ffffff;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 24px;background-color: #00ddff;}#main {font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 18px;}#button {background-color: white;color: black;border: 2px #e7e7e7;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;border-radius: 5px;}#button:hover {background-color: #e7e7e7; color: black;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;}#button1 {background-color: white;color: black;border: 2px solid #e7e7e7;width=\"50%\"font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;border-radius: 5px;}#button1:hover {background-color: #e7e7e7; color: black;width=\"50%\"font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;}#title {font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 24px;}</style><title>OPHS Science Request System</title></head><body><div><center><a href=\"/\"><h1 id=\"header\">OPHS Science Request System</h1></a></center></div><center><h3 id=\"main\">Your submit was complete!</h3><br><a href=\"/\" id=\"button\">Click here to return back to the home page</a>")

    else:
        form = SetForm()
    return render(request, 'blog/details.html', {
        'form':form,
        'data':data,
    })
def students(request):
    allowed_tasks = []
    for i in Task.objects.all():
        if request.user.get_short_name() == i.school:
            allowed_tasks.append(i.id)

    tasks = Task.objects.filter(id__in=allowed_tasks)
    return render(request, 'blog/students_data.html', {'tasks':tasks})
def students_list(request, id):
    students_list = []
    student_name = ""
    for i in Task.objects.all():
        if i.id == id:
            for o in range(len(i.students)-2):
                if i.students[o+2] == ",":
                    students_list.append(student_name)
                    student_name = ""
                else:
                    student_name=str(student_name)+i.students[o+2]
            with open("id.txt", "w") as t:
                t.write(str(id))

            return render(request, 'blog/students_list.html', {'students_list':students_list})

def student_mark(request, student):
    with open("id.txt") as t:
        id = t.read()
    comma_counter = 0
    counter = 0
    old_marks = ""
    marks_comma_counter = 0
    Loop = True
    for i in Task.objects.all():
        if i.id == int(id):
            find0 = i.students.find(student)
            for o in range(find0):
                if i.students[o] == ",":
                    comma_counter += 1
            while Loop == True:
                if marks_comma_counter == comma_counter+1:
                    Loop = False
                elif i.marks[counter] == ",":
                    marks_comma_counter +=1
                elif marks_comma_counter == comma_counter:
                    old_marks = old_marks+str(i.marks[counter])
                counter += 1
            expectedoutput = i.output
            endinput = i.input
            keywords = i.keyterms
            endinput_list = []
            ichars = []
            for n in range(len(endinput)-2):
                if not endinput[n+2] == ",":
                    ichars.append(endinput[n+2])
                else:
                    ichars.append("END")
            iword = ""
            for n in range(len(ichars)):
                if ichars[n] != "END":
                    iword = str(iword)+str(ichars[n])
                else:
                    endinput_list.append(iword)
                    iword = ""
            keywords_list =[]
            kword = ""
            for n in range(len(keywords)-2):
                if not keywords[n+2] == ",":
                    kword = str(kword)+str(keywords[n+2])
                else:
                    keywords_list.append(kword)
                    kword = ""
            char1 = []
            word1 = ""
            words1 =[]

            for n in range(len(expectedoutput)-2):
                if not expectedoutput[n+2] == ",":
                    char1.append(expectedoutput[n+2])
                elif expectedoutput[n+2] == ",":
                    char1.append("END")
            for n in range(len(char1)):
                if char1[n] != "END":
                    word1 = word1+char1[n]
                else:
                    words1.append(word1)
                    word1 = ""
            total_marks = (len(words1))+len(endinput_list)+len(keywords_list)
            return HttpResponse("<html><head><style>#header /*Styles for Header*/{padding: 15px;color: #ffffff;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 24px;background-color: #00ddff;}#main {font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 18px;}#button {background-color: white;color: black;border: 2px #e7e7e7;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;border-radius: 5px;}#button:hover {background-color: #e7e7e7; color: black;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;}#button1 {background-color: white;color: black;border: 2px solid #e7e7e7;width=\"50%\"font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;border-radius: 5px;}#button1:hover {background-color: #e7e7e7; color: black;width=\"50%\"font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;}#title {font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 24px;}</style><title>MARKER</title></head><body><div><center><a href=\"/\"><h1 id=\"header\">MARKER</h1></a></center></div><center><p id=\"main\">The student "+str(student)+" has got "+str(old_marks)+" out of "+str(total_marks)+" on "+str(i.title)+"</p><br><a href=\"/\" id=\"button\">Click here to return back to the home page</a>")

