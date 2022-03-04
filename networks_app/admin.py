from django.contrib import admin
from .models import AwinProductLink


# class AwinProductLinkAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'state')


admin.site.register(AwinProductLink)
