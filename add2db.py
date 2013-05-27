import csv
from docking.models import Receptor
from news.models import News

def addrec(csvfile):
    csvdata = csv.reader(open(csvfile), dialect="excel")
    print csvdata.next()
    userinput =  raw_input("Is this ok? yes/no: ")
    if userinput == "yes":
        for line in csvdata:
            rec = Receptor(name=line[0], abbreviation=line[1], pdbqt=line[2], conf=line[3], treshold1=line[4], treshold2=float(line[5]), auc=float(line[6]), ef=float(line[7]), roc=line[8], pdbqt_an=line[9], conf_an=line[10], treshold1_an=line[11], treshold2_an=float(line[12]), auc_an=float(line[13]), ef_an=float(line[14]), roc_an=line[15], roclegend=line[16], description=line[17])
            rec.save()
    else:
        ret = "Aborted by user"
        return ret
    
def addnews(csvfile):
    csvdata = csv.reader(open(csvfile), dialect="excel")
    print csvdata.next()
    userinput =  raw_input("Is this ok? yes/no: ")
    if userinput == "yes":
        for line in csvdata:
            news = News(title=unicode(line[0]), body=unicode(line[1]), author=unicode(line[2]))
            news.save()
    else:
        ret = "Aborted by user"
        return ret