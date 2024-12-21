from django import forms
from .models import ReservoirCharacteristics


class ReservoirCharacteristicsForm(forms.ModelForm):
    class Meta:
        model = ReservoirCharacteristics
        fields = ['rock_type', 'pressure_coefficient', 'temperature', 'is_water_sensitive']
        labels = {
            'rock_type': 'Тип породы коллектора',
            'pressure_coefficient': 'Коэффициент аномальности пластового давления',
            'temperature': 'Пластовая температура, °C',
            'is_water_sensitive': 'Является ли коллектор водочувствительным?',
            # 'additional-questions':'Включить дополнительные вопросы'
        }
        widgets = {
            'rock_type': forms.Select(attrs={'class': 'form-select'}),
            'pressure_coefficient': forms.Select(attrs={'class': 'form-select'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Температура в °C'}),
            'is_water_sensitive': forms.RadioSelect(
                choices=[(True, 'Да'), (False, 'Нет')],
                attrs={'required': 'required', 'class': 'is_water_sensitive'}
            ),
            # 'additional-questions': forms.CheckboxInput(
            #     attrs={'class': 'form-checkbox'}
            # )
        }

        
    def clean_is_water_sensitive(self):
        value = self.cleaned_data.get('is_water_sensitive')
        if value not in [True, False]:  # Проверяем значение
            raise forms.ValidationError('Выберите, является ли коллектор водочувствительным.')
        return value
