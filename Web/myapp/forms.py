# myapp/forms.py
from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_file']
        widgets = {
            'video_file': forms.FileInput(attrs={'class': 'inputfile'}),
        }
