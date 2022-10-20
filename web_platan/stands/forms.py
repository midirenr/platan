from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .utils.device_configurations.config import Device


class HistoryForm(forms.Form):
    serial_number = forms.CharField(min_length=14, max_length=14)

    def clean(self):
        super(HistoryForm, self).clean()

        return self.cleaned_data


class StatisticForm(forms.Form):
    stand = forms.ChoiceField(
        choices=(('All', 'Все'), ('stand_visual_inspection', 'Стэнд визуального осмотра'),
                 ('stand_diagnostic', 'Стенд диагностики'), ('stand_pci', 'Стэнд ПСИ'),
                 ('stand_package', 'Стэнд упаковки'), ('stand_board_case', 'Стэнд сборки')))
    date_time = forms.ChoiceField(
        choices=(('all time', 'За все время'), ('last 3 mouth', 'Последние 3 месяца'),
                 ('last week', 'Последние 7 дней'), ('last 24 hour', 'Последние 24 часа')))

    def clean(self):
        super(StatisticForm, self).clean()
        return self.cleaned_data


class GenerateSerialNumbersForm(forms.Form):
    device_type_choices = ((j, i) for i, j in Device.device_dictionary.items())
    device_type = forms.ChoiceField(choices=device_type_choices)
    modification_type_choices = ((j, i) for i, j in Device.modification_dictionary.items())
    modification_type = forms.ChoiceField(choices=modification_type_choices)
    detail_type_choices = ((j, i) for i, j in Device.detail_dictionary.items())
    detail_type = forms.ChoiceField(choices=detail_type_choices)
    place_of_production_choices = ((j, i) for i, j in Device.place_dictionary.items())
    place_of_production = forms.ChoiceField(choices=place_of_production_choices)
    count = forms.CharField(max_length=14)

    def clean(self):
        super(GenerateSerialNumbersForm, self).clean()
        return self.cleaned_data


class ChainBoardCase(forms.Form):
    board_serial_number = forms.CharField(min_length=14, max_length=14)
    case_serial_number = forms.CharField(min_length=14, max_length=14)

    def clean(self):
        super(ChainBoardCase, self).clean()

        return self.cleaned_data


class StandPackage(forms.Form):
    device_serial_number = forms.CharField(min_length=14, max_length=14)

    def clean(self):
        super(StandPackage, self).clean()

        return self.cleaned_data


class StandVisualInspection(forms.Form):
    board_serial_number = forms.CharField(min_length=14, max_length=14)

    def clean(self):
        super(StandVisualInspection, self).clean()

        return self.cleaned_data


class StandDiagnostic(forms.Form):
    CHOICES_COUNT = zip(range(1, 6), range(1, 6))
    CHOICES_TYPE = (
        ('RS', 'Сервисный маршрутизатор'),
        ('RB', 'Граничный маршрутизатор'),
    )

    diagnostic_device_type = forms.ChoiceField(choices=CHOICES_TYPE)
    board_count = forms.ChoiceField(choices=CHOICES_COUNT)
    board_serial_number_1 = forms.CharField(widget=forms.TextInput(), min_length=14, max_length=14)
    board_serial_number_2 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14',
        }), required=False)
    board_serial_number_3 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14',
        }), required=False)
    board_serial_number_4 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14',
        }), required=False)
    board_serial_number_5 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14',
        }), required=False)

    output = forms.CharField(widget=forms.Textarea(attrs={
        'style': 'resize:none;',
        'readonly': True,
    }), required=False)

    def clean(self):
        super(StandDiagnostic, self).clean()
        return self.cleaned_data


class StandPCI(forms.Form):
    CHOICES_COUNT = zip(range(1, 6), range(1, 6))
    CHOICES_TYPE = (
        ('RS', 'Сервисный маршрутизатор'),
        ('RB', 'Граничный маршрутизатор'),
    )

    pci_device_type = forms.ChoiceField(choices=CHOICES_TYPE)
    router_count = forms.ChoiceField(choices=CHOICES_COUNT)
    router_serial_number_1 = forms.CharField(widget=forms.TextInput(), max_length=14)
    router_serial_number_2 = forms.CharField(widget=forms.TextInput(
        attrs={
            'maxlength': '14',
        }), required=False)
    router_serial_number_3 = forms.CharField(widget=forms.TextInput(
        attrs={
            'maxlength': '14',
        }), required=False)
    router_serial_number_4 = forms.CharField(widget=forms.TextInput(
        attrs={
            'maxlength': '14',
        }), required=False)
    router_serial_number_5 = forms.CharField(widget=forms.TextInput(
        attrs={
            'maxlength': '14',
        }), required=False)

    output = forms.CharField(widget=forms.Textarea(attrs={
        'style': 'resize:none;',
        'readonly': True,
    }), required=False)

    def clean(self):
        super(StandPCI, self).clean()
        return self.cleaned_data
