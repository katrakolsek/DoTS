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
    sensitivity = []
    oneminusspecificity = []
    csum = 0
    for i in phist:
        csum += i
        sensitivity.append(float(csum)/float(totact))
    #    print i
    #print sensitivity
    
    csum = 0
    for i in nhist:
        csum += i
        oneminusspecificity.append(1 - (float(totinact) - float(csum))/float(totinact))
    
    #print oneminusspecificity
    return (oneminusspecificity, sensitivity)

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

def tresholdstable(treshold):
    tlist = treshold.split(';')
    c = 1
    treshold = '''<table class="table table-striped">
        <thead>
        <tr>
        <th>Score</th>
        <th>Sensitivity</th>
        <th>Specificity</th>
        <th><abbr title="Positive predictive value">PPV</abbr></th>
        <th><abbr title="Negative predictive value">NPV</abbr></th>
        </tr>
        </thead>
        <tbody>
        <tr>
        '''
    for t in tlist:
        if c == 1:
            color = "red"
        elif c == 2:
            color = "orange"
        elif c == 3:
            color = "yellow"
        slist = t.split(" ")
        for s in slist:
            treshold += '<td>%s</td>' % s
        if c != 3:
            treshold += '''
            </tr>
            <tr>
            '''
        else:
            treshold += '''
            </tr>
            '''
        c += 1
    treshold += '''
    </tr>
    </tbody>
    </table>
    '''
    return treshold

def resultstable(receptors,results,dockid):
    scores = '''
    <div class="bs-docs-grid">
    <div class="row show-grid">
    '''
    c = 0
    for rec in receptors:
        if c%3 == 0:
            scores += '''
            </div>
            <div class="row show-grid">
            '''
        treshold1 = float(rec.treshold1.split(';')[0].split(' ')[0])
        treshold2 = float(rec.treshold1.split(';')[1].split(' ')[0])
        treshold3 = float(rec.treshold1.split(';')[2].split(' ')[0])
        for result in results:
            if rec.pdbqt in result:
                score = float(result.split(":")[1])
                if score < treshold1:
                    color = "#e74c3c" #red
                elif score >= treshold1 and score < treshold2:
                    color = "#e67e22" #orange
                elif score >= treshold2 and score < treshold3:
                    color = "#f1c40f" #yellow
                else:
                    color = "#2ecc71" #green
                scores += '<div class="col-md-2 col-sm-4" style="border-style:solid;border-width:1px;border-color:white; background:' + color + '"><strong><a href="/static/results/' + dockid + '/' + result.split(":")[0] + '_dock.pdbqt" style="color:black">' + rec.abbreviation + ": " + result.split(":")[1] + '</a></strong></div>'
        c += 1
        if rec.pdbqt_an and rec.conf_an:
            if c%3 == 0:
                scores += '''
                </div>
                <div class="row show-grid">
                '''
            for result in results:
                if rec.pdbqt_an in result:
                    score = float(result.split(":")[1])
                    if score < treshold1:
                        color = "#e74c3c" #red
                    elif score >= treshold1 and score < treshold2:
                        color = "#e67e22" #orange
                    elif score >= treshold2 and score < treshold3:
                        color = "#f1c40f" #yellow
                    else:
                        color = "#2ecc71" #green
                    scores += '<div class="col-md-2 col-sm-4" style="border-style:solid;border-width:1px;border-color:white; background:' + color + '"><strong><a href="/static/results/' + dockid + '/' + result.split(":")[0] + '_dock.pdbqt" style="color:black">' + rec.abbreviation + ": " + result.split(":")[1] + '</a></strong></div>'
            c += 1
    scores += '</div></div>'
    return scores