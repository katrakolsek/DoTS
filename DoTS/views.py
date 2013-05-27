from django.shortcuts import render, render_to_response, get_object_or_404, HttpResponseRedirect
from news.models import News
from docking.models import Receptor, Docking
from docking.adddocking import adddocking
from docking.forms import SubmitDocking
from docking.math import getroc, getEnrichment, AUC
from json import dumps
import pybel
import string
import random

def home(request):
    allnews = News.objects.all()
    allreceptors = Receptor.objects.all()
    return render(request, 'index.html', {'allnews':allnews, 'allreceptors':allreceptors})

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
            error.append("Error in SMILES")
        if not error:
            uniquestring = ''.join(random.choice(string.ascii_lowercase) for x in range(10))
            dockid = adddocking(uniquestring,smiles,name)
            return HttpResponseRedirect('/docking/%s/' % dockid)
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
    if rec.roc_an != "":
        xdata_an, ydata_an = getroc(rec.roc_an.split('\\n')[:-1]) #returns Se data and 1-Sp data
        rocdata_an = dumps(zip(xdata_an, ydata_an)) #makes nested list in JSON format to plot ROC with Flot
        auc_an = round(AUC(xdata_an, ydata_an), 4) #takes Se data and 1-Sp data and returns auc of ROC
        enric_an = getEnrichment(rec.roc_an.split('\\n')[:-1], 1) #calculates enrichment factor, where sec arg is procent number
    else:
        rocdata_an = None
        auc_an = None
        enric_an = None
    return render(request, 'receptor.html', {'receptor':rec, 'rocdata':rocdata, 'enric':enric, 'auc':auc, 'rocdata_an':rocdata_an, 'enric_an':enric_an, 'auc_an':auc_an, 'allreceptors':allreceptors})

def docking(request, idnum):
    allreceptors = Receptor.objects.all()
    #Views for individual docking predictions
    try:
        offset = int(idnum)
    except ValueError:
        raise Http404()
    dock = get_object_or_404(Docking, pk=idnum)
    results = dock.results.split(",")
    receptors = Receptor.objects.all()
    scores = []
    for rec in receptors:
        for result in results:
            if rec.pdbqt in result:
                scores.append(rec.abbreviation+": </td><td>"+result.split(":")[1])
        if rec.pdbqt_an and rec.conf_an:
            for result in results:
                if rec.pdbqt_an in result:
                    scores.append(rec.abbreviation+" an.: </td><td>"+result.split(":")[1])
    return render(request, 'docking.html', {'docking':dock, 'scores':scores, 'allreceptors':allreceptors})

def about(request):
    allreceptors = Receptor.objects.all()
    return render(request, 'about.html', {'allreceptors':allreceptors})