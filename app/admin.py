from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ["id","title","body", "author"]
    list_filter = ["title","body",]
admin.site.register(Post, PostAdmin)