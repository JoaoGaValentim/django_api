from django.contrib import admin

from .models import Books, Categories

# Register your models here.
admin.site.register(Categories)
admin.site.register(Books)
