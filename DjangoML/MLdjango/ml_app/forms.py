from django import forms
from .models import PredictionModel

class UploadFileForm(forms.ModelForm):
    class Meta:
            model = PredictionModel
            fields = ['id','title', 'file']