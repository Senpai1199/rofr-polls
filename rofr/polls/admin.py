from django.contrib import admin
from polls.models import UserProfile, Question, Poll, UserResponse

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Poll)
admin.site.register(UserResponse)