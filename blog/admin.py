from django.contrib import admin
from .models import Practical
from .models import Year
from .models import Technician
from .models import Subject
from .models import Calendar
from .models import Period
admin.site.register(Practical)
admin.site.register(Year)
admin.site.register(Technician)
admin.site.register(Subject)
admin.site.register(Calendar)
admin.site.register(Period)
