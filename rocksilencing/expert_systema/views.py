import json
from django.shortcuts import render
from expert_systema.forms import ReservoirCharacteristicsForm
from expert_systema.utils import filter_technologies

def reservoir_characteristics_view(request):
    technologies = None
    if request.method == 'POST':
        form = ReservoirCharacteristicsForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            rock_type = cleaned_data.get('rock_type')
            pressure_coefficient = cleaned_data.get('pressure_coefficient')
            temperature = cleaned_data.get('temperature')
            is_water_sensitive = cleaned_data.get('is_water_sensitive')

            technologies = filter_technologies(
                rock_type,
                pressure_coefficient,
                temperature,
                is_water_sensitive
            )
    else:
        form = ReservoirCharacteristicsForm()

    # Сериализуем словарь в JSON
    technologies_json = json.dumps(technologies) if technologies else ''

    return render(request, 'reservoir_characteristics_form.html', {
        'form': form,
        'technologies': technologies,
        'technologies_json': technologies_json
    })

