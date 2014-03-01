from django import forms

class ReportForm(forms.Form):
    summary = forms.CharField(required=True,
                              widget=forms.TextInput(attrs={'required': 'required',
                                                            'class': 'form-control'}))
    details = forms.CharField(widget=forms.Textarea, required=False)
