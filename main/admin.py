from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser, Answer, Order, Message

admin.site.unregister(Group)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'date_joined']
    list_filter = ('is_staff',)
    fields = ['email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active', 'date_joined', 'password']
    readonly_fields = ['date_joined']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.set_password(obj.password)
        elif obj.password != CustomUser.objects.get(id=obj.pk).password:
            obj.set_password(obj.password)
        obj.save()


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['order', 'file_format', 'file', 'date_created']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'file', 'client', 'date_created']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['answer', 'creator', 'date_created']
    readonly_fields = ['creator']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        obj.save()
