from django.contrib import admin
from news.models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'additiondate')
    
admin.site.register(News, NewsAdmin)