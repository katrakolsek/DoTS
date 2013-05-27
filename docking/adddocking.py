import pybel
import openbabel

from docking.models import Receptor,Docking
from docking.filter_pains import detect_pains
from docking.tasks import dockingseq

def adddocking(uniquestring,smiles,molname):
    molname = molname.decode("windows-1252").encode('utf-8','ignore')
    try:
        mol = pybel.readstring("smi",str(smiles))
        descs = mol.calcdesc()
        #generate 2D coordinates, needs openbabel
        obConversion = openbabel.OBConversion()
        obConversion.SetInAndOutFormats("smi", "mdl")
        obmol = openbabel.OBMol()
        obConversion.ReadString(obmol, smiles)
        gen2d = openbabel.OBOp.FindType("gen2d")
        gen2d.Do(obmol)
        MDL = obConversion.WriteString(obmol)
        molfile = MDL.replace("\n", r"\n")
        CMW=descs["MW"]
        HBA=descs["HBA1"]
        HBD=descs["HBD"]
        logP=descs["logP"]
        tpsa=descs["TPSA"]
        #Get number of rotatable bonds
        smarts = pybel.Smarts(r"[!$([NH]!@C(=O))&!D1&!$(*#*)]\&!@[!$([NH]!@C(=O))&!D1&!$(*#*)]")
        rb = smarts.findall(mol)
        nrb = len(rb)
        #Get fingerprint and molecular complexity
        pains = detect_pains(mol)
        status = "Calculating..."
        results = ""
        dock = Docking(uniquestring=uniquestring,smiles=smiles,molname=molname,molfile=molfile,
                    CMW=CMW,HBA=HBA,HBD=HBD,logP=logP,tpsa=tpsa,nrb=nrb,pains=pains,
                    status=status,results=results)
        dock.save()
        dockingseq(dock)
        return dock.id
    except:
        status = "Something went wrong.."
        dock = Docking(uniquestring=uniquestring,smiles=smiles,molname=molname,status=status)
        dock.save()
        return "Error"