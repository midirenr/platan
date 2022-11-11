from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class RepairForm(forms.Form):
    serial_number = forms.CharField(min_length=14, max_length=14)

    def clean(self):
        super(RepairForm, self).clean()
        serial_number = self.cleaned_data['serial_number']
        if not Repair.check_note(serial_number):
            self.errors['serial_number'] = self.error_class([f'Серийный номер устройства {serial_number}'
                                                             f' отсутствует в списке плат подлежащих ремонту'
                                                             f' или уже была отремонтирована'])
            print("not valid")
            return self.cleaned_data
        return self.cleaned_data


class HistoryForm(forms.Form):
    serial_number = forms.CharField(min_length=14, max_length=14)

    def clean(self):
        super(HistoryForm, self).clean()
        serial_number = self.cleaned_data['serial_number']

        if not History.check_history(serial_number):
            self.errors['serial_number'] = self.error_class([f'Серийный номер устройства {serial_number}'
                                                             f'отсутствует в базе данных'])
            return self.cleaned_data

        return self.cleaned_data


class StatisticForm(forms.Form):
    date_time = forms.ChoiceField(
        choices=(('all time', 'За все время'), ('last 3 mouth', 'Последние 3 месяца'),
                 ('last week', 'Последние 7 дней'), ('last 24 hour', 'Последние 24 часа')))

    def clean(self):
        super(StatisticForm, self).clean()
        return self.cleaned_data


class GenerateSerialNumbersForm(forms.ModelForm):

    class Meta:
        model = GenerateSerialNumbers
        fields = '__all__'

        labels = {
            'device_type': 'Тип устройства',
            'modification_type': 'Тип модификации',
            'detail_type': 'Тип детали',
            'place_of_production': 'Место производства',
            'count': 'Количество',
        }


class ChainBoardCase(forms.Form):
    board_serial_number = forms.CharField(min_length=14, max_length=14)
    case_serial_number = forms.CharField(min_length=14, max_length=14)

    def clean(self):
        super(ChainBoardCase, self).clean()

        board_serial_number = self.cleaned_data.get('board_serial_number')
        case_serial_number = self.cleaned_data.get('case_serial_number')

        board_list = []
        case_list = []
        cut_board = board_serial_number[4:6]
        cut_case = case_serial_number[4:6]

        if cut_board != '20':
            self.errors['board_serial_number'] = self.error_class([f'Серийный номер платы {board_serial_number}'
                                                                   f' не соответствует серийному номеру платы!'])
            return self.cleaned_data

        if cut_case != '10':
            self.errors['case_serial_number'] = self.error_class([f'Серийный номер корпуса {case_serial_number}'
                                                                  f' не соответствует серийному номеру корпуса!'])
            return self.cleaned_data

        if board_serial_number == case_serial_number:
            self.errors['case_serial_number'] = self.error_class([f'Серийные номера платы и корпуса одинаковые!'
                                                                  f'\nОтсканируйте заново'])
            return self.cleaned_data

        if not SerialNumBoard.check_sn(board_serial_number):
            self._errors['board_serial_number'] = self.error_class([f'Серийного номера {board_serial_number}'
                                                                    f' нет в Базе Данных.\nОтсканируйте заново,'
                                                                    f' в проивном случае верните плату на стенд'
                                                                    f' диагностики.'])
            return self.cleaned_data

        if not Devices.check_diag(board_serial_number):
            self._errors['board_serial_number'] = self.error_class([f'Плата с серийным номером {board_serial_number}'
                                                                    f' не прошла дигностику!'
                                                                    f'\nВерните плату на стенд диагностики!'])
            return self.cleaned_data
        else:
            board_list.append(board_serial_number)

        if SerialNumRouter.check_sn(case_serial_number):
            self.errors['case_serial_number'] = self.error_class([f'Серийный номер корпуса {case_serial_number}'
                                                                  f' уже есть в БД!\nОтсканируйте заново!'])
        else:
            case_list.append(case_serial_number)

        return self.cleaned_data


class StandPackage(forms.Form):
    device_serial_number = forms.CharField(min_length=14, max_length=14)

    def clean(self):
        super(StandPackage, self).clean()
        device_serial_number = self.cleaned_data['device_serial_number']
        cut_device = device_serial_number[4:6]

        if cut_device != '10':
            self.errors['device_serial_number'] = self.error_class([f'Серийный номер устройства {device_serial_number}'
                                                                    f' не соответствует серийному номеру устройства!'
                                                                    f'\nОтсканируйте повторно!'])
            return self.cleaned_data

        if not SerialNumRouter.check_sn(device_serial_number):
            self.errors['device_serial_number'] = self.error_class([f'Серийный номер устройства {device_serial_number}'
                                                                    f' отсутствует в Базе Данных"'
                                                                    f'\nОтсканируйте заново.'])
            return self.cleaned_data

        if str(Devices.get_date_time_pci(device_serial_number)) == 'No':
            self.errors['device_serial_number'] = self.error_class([f'Устройство с серийным номером'
                                                                    f' {device_serial_number} не прошло ПСИ!'
                                                                    f'\nПередайте устройство на стенд ПСИ!'])
            return self.cleaned_data

        return self.cleaned_data

class StandVisualInspection(forms.Form):
    board_serial_number = forms.CharField(min_length=14, max_length=14)

    def clean(self):
        super(StandVisualInspection, self).clean()

        board_serial_number = self.cleaned_data['board_serial_number']

        if board_serial_number[4:6] != '20':
            self.errors['board_serial_number'] = self.error_class([f'Серийный номер указан неправильно!'
                                                                   f' Отсканируйте повторно.'])
            return self.cleaned_data

        if SerialNumBoard.get_board_count(board_serial_number) > 0:
            self.errors['board_serial_number'] = self.error_class([f'Плата с серийным номером {board_serial_number}'
                                                                   f' уже есть в Базе Данных!'])
            return self.cleaned_data

        return self.cleaned_data

class StandDiagnostic(forms.Form):
    CHOICES_COUNT = zip(range(1, 6), range(1, 6))
    CHOICES_TYPE = (
        ('RS', 'Сервисный маршрутизатор'),
        ('RB', 'Граничный маршрутизатор'),
    )

    diagnostic_device_type = forms.ChoiceField(choices=CHOICES_TYPE)
    board_count = forms.ChoiceField(choices=CHOICES_COUNT)
    board_serial_number_1 = forms.CharField(widget=forms.TextInput(), max_length=14)
    board_serial_number_2 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14', }),
        required=False)
    board_serial_number_3 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14', }),
        required=False)
    board_serial_number_4 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14', }),
        required=False)
    board_serial_number_5 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14', }),
        required=False)

    output = forms.CharField(widget=forms.Textarea(attrs={
        'style': 'resize:none;',
        'readonly': True, }),
        required=False)

    def clean(self):
        super(StandDiagnostic, self).clean()

        board_count = self.cleaned_data['board_count']

        serial_numbers = [
            self.cleaned_data['board_serial_number_1'],
            self.cleaned_data['board_serial_number_2'],
            self.cleaned_data['board_serial_number_3'],
            self.cleaned_data['board_serial_number_4'],
            self.cleaned_data['board_serial_number_5']]

        for i in range(int(board_count)):
            if serial_numbers[i][4:6] != '20':
                self.errors['board_serial_number_1'] = self.error_class([f'Серийный номер указан неправильно!'
                                                                         f'\nОтсканируйте повторно.'])
                return self.cleaned_data

            if not SerialNumBoard.is_existence(serial_numbers[i]):
                self.errors['board_serial_number_1'] = self.error_class([f'Плата с серийным номером {serial_numbers[i]}'
                                                                         f' отсутствует в Базе Данных!\n'
                                                                         f'Передайте плату на стенд'
                                                                         f' визуального осмотра.'])
                return self.cleaned_data

            if not SerialNumBoard.get_visual_inspection_result(serial_numbers[i]):
                self.errors['board_serial_number_1'] = self.error_class([f'Плата с серийным номером {serial_numbers[i]}'
                                                                         f' была помечена как бракованная!\n'
                                                                         f'Передайте плату на стенд'
                                                                         f' визуального осмотра.'])
                return self.cleaned_data

            if Macs.get_free_mac_count() < 3:
                self.errors['board_serial_number_1'] = self.error_class([f'В базе данных отсутствуют свободные'
                                                                        f' MAC-адреса, обратитесь к разработчику'])
                return self.cleaned_data
        return self.cleaned_data


class StandPCI(forms.Form):
    CHOICES_COUNT = zip(range(1, 6), range(1, 6))
    CHOICES_TYPE = (
        ('RS', 'Сервисный маршрутизатор'),
        ('RB', 'Граничный маршрутизатор'),
    )

    pci_device_type = forms.ChoiceField(choices=CHOICES_TYPE)
    router_count = forms.ChoiceField(choices=CHOICES_COUNT)
    router_serial_number_1 = forms.CharField(widget=forms.TextInput(), min_length=14, max_length=14)
    router_serial_number_2 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14',
        }), required=False)
    router_serial_number_3 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14',
        }), required=False)
    router_serial_number_4 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14',
        }), required=False)
    router_serial_number_5 = forms.CharField(widget=forms.TextInput(
        attrs={
            'minlength': '14',
            'maxlength': '14',
        }), required=False)

    output = forms.CharField(widget=forms.Textarea(attrs={
        'style': 'resize:none;',
        'readonly': True,
    }), required=False)

    def clean(self):
        super(StandPCI, self).clean()

        router_count = self.cleaned_data['router_count']
        serial_numbers = [
            self.cleaned_data['router_serial_number_1'],
            self.cleaned_data['router_serial_number_2'],
            self.cleaned_data['router_serial_number_3'],
            self.cleaned_data['router_serial_number_4'],
            self.cleaned_data['router_serial_number_5']]

        for number in range(0, int(router_count)):
            if serial_numbers[number][4:6] != '10':
                self.errors[f'router_serial_number_{number+1}'] = self.error_class([f'Серийный номер'
                                                                                    f' указан неправильно!'
                                                                                    f'\nОтсканируйте повторно.'])
                return self.cleaned_data

            if not SerialNumRouter.check_sn(serial_numbers[number]):
                self.errors[f'router_serial_number_{number+1}'] = self.error_class([f'Плата с серийным номером '
                                                                                    f'{serial_numbers[number]}'
                                                                                    f' отсутствует в Базе Данных!\n'
                                                                                    f'Передайте плату на стенд'
                                                                                    f' визуального осмотра.'])
                return self.cleaned_data

        return self.cleaned_data
