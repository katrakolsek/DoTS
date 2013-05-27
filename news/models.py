from django.db import models

class News(models.Model):
    """
    News model, shown on first page
    """
    title = models.CharField(max_length=500, blank=False)
    body = models.TextField(blank=True)
    author = models.CharField(max_length=100, blank=True)
    additiondate = models.DateField(auto_now=True, auto_now_add=True) #automatically updates date and adds date upon creation
    
    def __unicode__(self):
        return u'%s, %s' % (self.title, self.additiondate)
    
    class Meta:
        ordering = ['-id']
