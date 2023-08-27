from django import forms
from .models import *

class FilterGrades(forms.Form):
    
    grades = forms.ModelMultipleChoiceField(queryset = TechGrade.objects.all(),
                                            widget = forms.CheckboxSelectMultiple,
                                            required = False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grades'].choices = [(grade.id, grade.grade) for grade in TechGrade.objects.all()]

class SearchBar(forms.Form):
    search = forms.CharField(max_length = 200, required = False)