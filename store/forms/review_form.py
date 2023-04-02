from django import forms
from store.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control required'}),
        }
