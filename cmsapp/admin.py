from django.contrib import admin
from .models import  Subcategory, CustomUser, Category
from django.contrib.auth.admin import UserAdmin
from .models import Type_Traffic_Lights

class UserModel(UserAdmin):
    list_display = ['username', 'email', 'user_type']

admin.site.register(CustomUser, UserModel)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Type_Traffic_Lights)
