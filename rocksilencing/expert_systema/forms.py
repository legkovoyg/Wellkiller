from django import forms
from .models import ReservoirCharacteristics


class ReservoirCharacteristicsForm(forms.ModelForm):
    class Meta:
        model = ReservoirCharacteristics
        fields = ['rock_type', 'pressure_coefficient', 'temperature', 'is_water_sensitive']
        labels = {
            'rock_type': 'Укажите тип породы коллектора',
            'pressure_coefficient': 'Укажите коэффициент аномальности пластового давления',
            'temperature': 'Укажите пластовую температуру, °C',
            'is_water_sensitive': 'Является ли коллектор водочувствительным?',
        }
        widgets = {
            'rock_type': forms.Select(attrs={'class': 'form-select'}),
            'pressure_coefficient': forms.Select(attrs={'class': 'form-select'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Температура в °C'}),
            'is_water_sensitive': forms.RadioSelect(
                choices=[(True, 'Да'), (False, 'Нет')],
                attrs={'required': 'required'}
            ),
        }

        
    def clean_is_water_sensitive(self):
        value = self.cleaned_data.get('is_water_sensitive')
        if value not in [True, False]:  # Проверяем значение
            raise forms.ValidationError('Выберите, является ли коллектор водочувствительным.')
        return value
