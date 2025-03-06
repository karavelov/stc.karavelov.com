# /var/www/karavelov/stc/cmsapp/forms.py

from django import forms
from .models import Signal, Category, Subcategory

class SignalForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория",
        required=True
    )
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.none(),
        label="Подкатегория",
        required=True
    )
    signalname = forms.CharField(
        max_length=200,
        label="Име на сигнал",
        required=True
    )

    class Meta:
        model = Signal
        fields = ['category', 'subcategory', 'signalname']

    def __init__(self, *args, **kwargs):
        super(SignalForm, self).__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(cat_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set
