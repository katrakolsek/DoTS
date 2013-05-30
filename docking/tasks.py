from celery.decorators import task
import pybel
from subprocess import call
from os import listdir, makedirs
from django.conf import settings
from docking.models import Receptor

def datacleaning(datafile):
    """
    converts vina report to csv
    """
    data = open(datafile, "r").readlines()
    lines = []
    save = False
    line = []

    for i in data:
        if "Output will be " in i:
            lines.append(line)
            line = []
            line.append(i.split()[3].split("_")[0])
        
        if "-----+" in i:
            save = True
        if "Writing output" in i:
            save = False
        if save == True and "-----+" not in i:
            line.append(i.split()[1])
    lines.append(line)
    print lines [0][0]
    return lines [0][0]

@task(max_retries=2, default_retry_delay=5*60)
def dockingseq(dock):
    """
    This module needs celery and compatible messaging queue system (RabbitMQ)
    """
    static = settings.STATICFILES_DIRS[0]
    respath = static+"results/"+dock.uniquestring
    makedirs(respath)
    smiles = dock.smiles
    mol = pybel.readstring('smi', smiles)
    mol.make3D(forcefield="MMFF94", steps=10)
    mol.localopt(forcefield="MMFF94", steps=500)
    mol.write("pdbqt", respath+"/orig.pdbqt", overwrite=True)
    receptors = Receptor.objects.all()
    result = ""
    for rec in receptors:
        call(["vina", "--config", static+"conf/"+rec.conf+".txt", "--receptor", static+"receptor/"+rec.pdbqt+".pdbqt", "--ligand", respath+"/orig.pdbqt", "--log", respath+"/"+rec.pdbqt+".log", "--out", respath+"/"+rec.pdbqt+"_dock.pdbqt"])
        score = ""
        score = datacleaning(respath+"/"+rec.pdbqt+".log")
        result += str(rec.pdbqt)+ ":"+str(score)+","
        if rec.pdbqt_an and rec.conf_an:
            call(["vina", "--config", static+"conf/"+rec.conf_an+".txt", "--receptor", static+"receptor/"+rec.pdbqt_an+".pdbqt", "--ligand", respath+"/orig.pdbqt", "--log", respath+"/"+rec.pdbqt_an+".log", "--out", respath+"/"+rec.pdbqt_an+"_dock.pdbqt"])
            score = ""
            score = datacleaning(respath+"/"+rec.pdbqt_an+".log")
            result += str(rec.pdbqt_an)+ ":"+str(score)+","
        print result
    dock.results = result
    dock.status = "Finished!"
    dock.save()
        