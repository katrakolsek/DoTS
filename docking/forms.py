from django import forms

class SubmitDocking(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'span2','placeholder':'Name, optional'}))
    smiles = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'span5','placeholder':'SMILES', 'required':''}))
