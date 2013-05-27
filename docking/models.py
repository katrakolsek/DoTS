from django.db import models

# Create your models here.

class Receptor(models.Model):
    """
    Receptors ready for docking.
    """
    name = models.CharField(max_length=500, blank=False)
    abbreviation = models.CharField(max_length=10, blank=False)
    pdbqt = models.CharField(max_length=50, blank=True)
    conf = models.CharField(max_length=50, blank=True)
    treshold1 = models.CharField(max_length=100, blank=True)
    treshold2 = models.FloatField(null=True, blank=True)
    auc = models.FloatField(null=True, blank=True) # AUC for ROC curve
    ef = models.FloatField(null=True, blank=True) # Enrichment factor
    roc = models.TextField(blank=True) # ROC curve in JSON format
    pdbqt_an = models.CharField(max_length=50, blank=True)
    conf_an = models.CharField(max_length=50, blank=True)
    treshold1_an = models.CharField(max_length=100, blank=True)
    treshold2_an = models.FloatField(null=True, blank=True)
    auc_an = models.FloatField(null=True, blank=True) # AUC for ROC curve
    ef_an = models.FloatField(null=True, blank=True) # Enrichment factor
    roc_an = models.TextField(blank=True) # ROC curve in JSON format
    roclegend = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return u'%s, %s' % (self.name, self.abbreviation)
    
    class Meta:
        ordering = ['abbreviation']

class Docking(models.Model):
    """
    Individual calculations and results
    """
    uniquestring = models.CharField(max_length=32, blank=False)
    smiles = models.CharField(max_length=500, blank=False)
    molname = models.CharField(max_length=500, blank=True)
    molfile = models.TextField(blank=True, verbose_name='MolFile')
    CMW = models.FloatField(null=True, blank=True, verbose_name='MW, calculated')
    HBA = models.IntegerField(null=True, blank=True, verbose_name='H-bond acceptors')
    HBD = models.IntegerField(null=True, blank=True, verbose_name='H-bond donors')
    logP = models.FloatField(null=True, blank=True)
    tpsa = models.FloatField(null=True, blank=True, verbose_name='Polar surface area')
    nrb = models.IntegerField(null=True, blank=True, verbose_name='Number of rotatable bonds')
    pains = models.TextField(max_length=100, verbose_name='Pan Assay Interference Compounds', blank=True)
    status = models.CharField(max_length=20, blank=True)
    results = models.TextField(blank=True)
    
    def __unicode__(self):
        return u'%s, %s' % (self.uniquestring, self.id)
    
    class Meta:
        ordering = ['id']
