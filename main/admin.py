from django.contrib import admin
from main.models import User, Thesis, Message

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "ssn",
    ]


class ThesisAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "student",
        "refree",
        "title",
    ]


class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "sender",
        "reciever",
        "text",
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Message, MessageAdmin)
