from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponseRedirect
from news.models import News, Faq
from docking.models import Receptor, Docking
from docking.adddocking import adddocking
from docking.forms import SubmitDocking
from docking.math import getroc, getEnrichment, AUC, tresholdstable, resultstable
from json import dumps
import pybel
import string
import random

def home(request):
    allnews = News.objects.all()
    allreceptors = Receptor.objects.all()
    return render(request, 'index.html', {'allnews':allnews, 'allreceptors':allreceptors})

def get_faq(request):
    allfaq = Faq.objects.all()
    allreceptors = Receptor.objects.all()
    return render(request, 'faq.html', {'allfaq':allfaq, 'allreceptors':allreceptors})

def prediction(request):
    """
    Form for submitting user calculations
    """
    allreceptors = Receptor.objects.all()
    
    
    if 'submitdocking' in request.POST:
        form = SubmitDocking(request.POST)
        form.is_valid()
        smiles = str(form.cleaned_data['smiles'])
        name = form.cleaned_data['name']
        
        error = []
        try:
            pybel.readstring("smi", str(smiles))
        except:
            error.append("Error in SMILES or compound molecular weight too big")
        if not error:
            uniquestring = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
            dockid = adddocking(uniquestring,smiles,name)
            return HttpResponseRedirect('/docking/%s/' % uniquestring)
        else:
            form = SubmitDocking()
            return render(request, 'prediction.html', {'form':form, 'error':error, 'allreceptors':allreceptors})
    else:
        form = SubmitDocking()
        return render(request, 'prediction.html', {'form':form, 'allreceptors':allreceptors})

def receptors(request):
    allreceptors = Receptor.objects.all()
    return render(request, 'receptors.html', {'allreceptors':allreceptors})

def receptor(request, idnum):
    allreceptors = Receptor.objects.all()
    #Views for individual receptors
    try:
        offset = int(idnum)
    except ValueError:
        raise Http404()
    rec = get_object_or_404(Receptor, pk=idnum)
    
    xdata, ydata = getroc(rec.roc.split('\\n')[:-1]) #returns Se data and 1-Sp data
    rocdata = dumps(zip(xdata, ydata)) #makes nested list in JSON format to plot ROC with Flot
    auc = round(AUC(xdata, ydata), 4) #takes Se data and 1-Sp data and returns auc of ROC
    enric = getEnrichment(rec.roc.split('\\n')[:-1], 1) #calculates enrichment factor, where sec arg is procent number
    tresholds = tresholdstable(rec.treshold1)
    if rec.roc_an != "":
        xdata_an, ydata_an = getroc(rec.roc_an.split('\\n')[:-1]) #returns Se data and 1-Sp data
        rocdata_an = dumps(zip(xdata_an, ydata_an)) #makes nested list in JSON format to plot ROC with Flot
        auc_an = round(AUC(xdata_an, ydata_an), 4) #takes Se data and 1-Sp data and returns auc of ROC
        enric_an = getEnrichment(rec.roc_an.split('\\n')[:-1], 1) #calculates enrichment factor, where sec arg is procent number
        tresholds_an = tresholdstable(rec.treshold1_an)
    else:
        rocdata_an = None
        auc_an = None
        enric_an = None
        tresholds_an = None
    return render(request, 'receptor.html', {'receptor':rec, 'rocdata':rocdata, 'enric':enric, 'auc':auc, 'rocdata_an':rocdata_an, 'enric_an':enric_an, 'auc_an':auc_an, 'allreceptors':allreceptors, 'tresholds':tresholds, 'tresholds_an':tresholds_an})

def docking(request, dockid):
    allreceptors = Receptor.objects.all()
    #Views for individual docking predictions
#    try:
#        offset = int(idnum)
#    except ValueError:
#        raise Http404()
    dock = get_object_or_404(Docking, uniquestring=dockid)
    results = dock.results.split(",")
    receptors = Receptor.objects.all()
    scores = resultstable(receptors,results)
    return render(request, 'docking.html', {'docking':dock, 'scores':scores, 'allreceptors':allreceptors})

def about(request):
    allreceptors = Receptor.objects.all()
    return render(request, 'about.html', {'allreceptors':allreceptors})

def converter(request):
    if request.method == 'GET':
        mol = request.GET['name']
        molecule = pybel.readstring("mol", str(mol))
        smiles = molecule.write("smi").split('\t')[0]
        return render(request, 'converter.html', {'smiles':smiles})
    else:
        mol = ''
    return render(request, 'converter.html')
