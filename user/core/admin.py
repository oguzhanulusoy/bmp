from django.contrib import admin
from .models import User, UserToken

admin.site.register(User)
admin.site.register(UserToken)
