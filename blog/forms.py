from django import forms
from .models import Technician
from .models import Period
from .models import Subject
from bootstrap_datepicker_plus import DateTimePickerInput
from bootstrap_datepicker_plus import DatePickerInput
from datetime import datetime
from time import localtime
import datetime
from datetime import timedelta
#from dateutil import tz
import calendar
from django.http import HttpResponse
class SetForm(forms.Form):
    sets = forms.IntegerField(
        min_value=1,
    )
    prints = forms.IntegerField(
        min_value=0,
    )
    technician = forms.ModelChoiceField(
       widget = forms.Select,
       queryset = Technician.objects.all(),
       empty_label=None,
    )
    time = forms.DateField(
        input_formats = ['%d/%m/%Y'],
        widget=DatePickerInput(
            format='%d/%m/%Y',
    ))
    period = forms.ModelChoiceField(
       widget = forms.Select,
       queryset = Period.objects.all(),
       empty_label=None,
    )
    additional_comments = forms.CharField(
        max_length=20000,
        widget=forms.Textarea(),
    )
    room = forms.CharField(
        max_length=4,
    )
    def clean(self):
        cleaned_data = super(SetForm, self).clean()
        sets = cleaned_data.get('sets')
        prints = cleaned_data.get('prints')
        technician = cleaned_data.get('technician')
        time = cleaned_data.get('time')
        period = cleaned_data.get('period')
        additional_comments = cleaned_data.get('additional_comments')
        room = cleaned_data.get('room')
        if not sets or not time or not room:
            raise forms.ValidationError('You have to write something!')
        elif prints < 0:
            raise forms.ValidationError('You have to enter a print number bigger than 0!')
        else:
            #t = datetime.datetime.strptime(str(time), '%Y-%d-%m')
            current = datetime.datetime.now()
            
            if datetime.datetime(time.year,time.month,time.day) < datetime.datetime(current.year,current.month,current.day):
                raise forms.ValidationError("The date cannot be in the past!")
            elif datetime.datetime(time.year,time.month,time.day) == datetime.datetime(current.year,current.month,current.day):
                extracted_time = period.time
                hours, minutes = map(int, extracted_time.split(':'))
                if datetime.time(current.hour,current.minute) > datetime.time(hours,minutes):
                    raise forms.ValidationError("Period time is in the past!")
class FilterForm(forms.Form):
    initial_dt = ((i.tag, i.title)for i in Subject.objects.all())
    subject = forms.MultipleChoiceField(
       widget = forms.CheckboxSelectMultiple,
       choices = initial_dt,
       #selected = True,
       initial=['b','p','c'],
       required=False,
    )

    def clean(self):
        cleaned_data = super(FilterForm, self).clean()
        subject = cleaned_data.get('subject')
        '''if not subject:
            raise forms.ValidationError('You have to write something!')
        '''

class CalendarForm(forms.Form):
    initial_dt = ((i.tag, i.title)for i in Subject.objects.all())
    sub_list = []
    for i in Subject.objects.all():
        sub_list.append(i.tag)
    choices_technician = ((i.id, i.name) for i in Technician.objects.all())
    tech_list = []
    for i in Technician.objects.all():
        tech_list.append(i.id)
    #prin()
    date = forms.DateField(
        input_formats = ['%d/%m/%Y'],
        required=False,
        widget=DatePickerInput(
            format='%d/%m/%Y',
    ))
    subject = forms.MultipleChoiceField(
       widget = forms.CheckboxSelectMultiple,
       choices = initial_dt,
       #selected = True,
       initial=sub_list,
       required=False,
    )
    technician = forms.MultipleChoiceField(
       widget = forms.CheckboxSelectMultiple,
       choices = choices_technician,
       #selected = True,
       initial=tech_list,
       required=False,
    )
    def clean(self):
        cleaned_data = super(CalendarForm, self).clean()
        date = cleaned_data.get('date')
        subject = str(cleaned_data.get('subject'))
        technician = str(cleaned_data.get('technician'))
        current = datetime.date.today()
        if not date:
            raise forms.ValidationError("You have to write a date!")
        elif datetime.date(date.year,date.month,date.day) < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        elif subject == "[]":
            raise forms.ValidationError("You cannot leave the subject filter empty!")
        elif technician == "[]":
            raise forms.ValidationError("You cannot leave the technician filter empty!")