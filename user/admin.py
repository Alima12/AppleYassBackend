from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from user.models import Images, Address
# Register your models here.
User = get_user_model()

admin.site.register(User, UserAdmin)
admin.site.register(Images)
admin.site.register(Address)