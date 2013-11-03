from django.db import models

class News(models.Model):
    """
    News model, shown on first page
    """
    title = models.CharField(max_length=500, blank=False)
    body = models.TextField(blank=True)
    author = models.CharField(max_length=100, blank=True)
    additiondate = models.DateField()
    
    def __unicode__(self):
        return u'%s, %s' % (self.title, self.additiondate)
    
    class Meta:
        ordering = ['-id']

class Faq(models.Model):
    """
    Frequently Asked Questions page
    """
    title = models.CharField(max_length=500, blank=True)
    body = models.TextField(blank=True)
    author = models.CharField(max_length=100, blank=True)
    additiondate = models.DateField()
    
    def __unicode__(self):
        return u'%s, %s' % (self.title, self.additiondate)
    
    class Meta:
        ordering = ['-id']