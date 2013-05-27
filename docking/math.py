from numpy import histogram, roll
from operator import itemgetter
from docking.models import Receptor
from docking.models import Docking

def AUC(xdata, ydata):
    """Given a list of x coordinates and a list of y coordinates, returns
    the area under the curve they define."""
    x = (roll(xdata, -1) - xdata)[:-1]
    y = (roll(ydata, -1) + ydata)[:-1]/2
    return sum(map(lambda x, y: x*y, x, y))

def getroc(data):
    """
    Accepts data with binary classifier and score
    """
    allscores = []
    pscores = []
    nscores = []
    for line in data:
        line = str(line)
        allscores.append(float(line.split(' ')[1]))
        if line.split(' ')[0] == "1":
            pscores.append(float(line.split(' ')[1]))
        if line.split(' ')[0] == "-1" or line.split(' ')[0] == "0":
            nscores.append(float(line.split(' ')[1]))
    hist, edge = histogram(allscores, bins=500)
    totact = len(pscores)
    totinact = len(nscores)
    #print edge
    #print hist
    phist, pedge = histogram(pscores, bins=edge)
    nhist, nedge = histogram(nscores, bins=edge)
    #print phist
    #print nhist
    selectivity = []
    oneminusspecificity = []
    csum = 0
    for i in phist:
        csum += i
        selectivity.append(float(csum)/float(totact))
    #    print i
    #print selectivity
    
    csum = 0
    for i in nhist:
        csum += i
        oneminusspecificity.append(1 - (float(totinact) - float(csum))/float(totinact))
    
    #print oneminusspecificity
    return (oneminusspecificity, selectivity)

def getEnrichment(data, procent):
    my_list = []
    for line in data:
        temp = []
        temp.append(float(str(line).split(' ')[0]))
        temp.append(float(str(line).split(' ')[1]))
        my_list.append(temp)
    combolist = []
    all_molecules = 0
    positive_all = 0
    positive_oneprocent = 0
    i = 1
    for line in my_list:
        all_molecules += 1
        combolist.append(line)
        if line[0] == 1.0:
            positive_all += 1
    sortcombo = sorted(combolist, key=itemgetter(1)) 
    # sorts nested lists and tuples
    oneprocent_molecules = round(all_molecules/100.0 * float(procent))
    for i in range(0, int(oneprocent_molecules)):
            if sortcombo[i][0] == 1.0:
                positive_oneprocent += 1
    enrichfactor = round(positive_oneprocent / float(oneprocent_molecules) * all_molecules / float(positive_all), 1)
    return enrichfactor
