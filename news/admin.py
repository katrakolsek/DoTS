from django.contrib import admin
from news.models import News, Faq

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'additiondate')
    
admin.site.register(News, NewsAdmin)

class FaqAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'additiondate')
    
admin.site.register(Faq, FaqAdmin)