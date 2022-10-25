from django.shortcuts import render, redirect
from django.http import FileResponse
import datetime


from .forms import *
from .models import *
from .utils.generate_serial_number import *


def index(request):
    return render(request, 'index.html', context={})


def history_page(request):
    form = HistoryForm()
    if request.method == "POST":
        form = HistoryForm(data=request.POST)

        if form.is_valid():
            serial_number = request.POST.get('serial_number')
            history = History.get_history(serial_number)
            return render(request, 'history.html', context={'history': history, 'form': form})

    return render(request, 'history.html', context={'form': form})


def statistic_page(request):
    form = StatisticForm()
    if request.method == "POST":
        form = StatisticForm(data=request.POST)
        date_time = request.POST.get('date_time')
        statistic = Statistic.get_statistic(date_time)
        returnable_statistic = {'All': 0,
                                'stand_visual_inspection': 0,
                                'stand_diagnostic': 0,
                                'stand_board_case': 0,
                                'stand_PCI': 0,
                                'stand_package': 0}
        for stat in statistic:
            returnable_statistic['All'] = returnable_statistic['All'] + 1
            if stat.stand == "Стенд визуального осмотра":
                returnable_statistic['stand_visual_inspection'] = returnable_statistic['stand_visual_inspection'] + 1
            if stat.stand == "Стенд диагностики":
                returnable_statistic['stand_diagnostic'] = returnable_statistic['stand_diagnostic'] + 1
            if stat.stand == "Стенд сборки":
                returnable_statistic['stand_board_case'] = returnable_statistic['stand_board_case'] + 1
            if stat.stand == "Стенд ПСИ":
                returnable_statistic['stand_PCI'] = returnable_statistic['stand_PCI'] + 1
            if stat.stand == "Стенд упаковки":
                returnable_statistic['stand_package'] = returnable_statistic['stand_package'] + 1

        return render(request, 'statistic.html', context={'statistic': returnable_statistic, 'form': form})

    return render(request, 'statistic.html', context={'form': form})


def generate_serial_numbers_page(request):
    form = GenerateSerialNumbersForm()

    if request.method == 'POST':
        form = GenerateSerialNumbersForm(data=request.POST)

        if form.is_valid():
            device_type = form.cleaned_data['device_type']
            modification_type = form.cleaned_data['modification_type']
            detail_type = form.cleaned_data['detail_type']
            place_of_production = form.cleaned_data['place_of_production']
            count = form.cleaned_data['count']
            current_time = str(datetime.datetime.now())[:-7].replace(' ', '_').replace(':', '-')
            generate_serial_number(device_type, modification_type,
                                   detail_type, place_of_production, count, current_time)
            filename1 = f'stands/storage/userfiles/SerialNumbers/{device_type}/{modification_type}/{detail_type}' \
                        f'/serial_number_for_{modification_type}/{detail_type}({current_time}).txt'
            return FileResponse(open(filename1, 'rb'), as_attachment=True)
    return render(
        request, 'generate_serial_numbers.html', context={'form': form})


def stand_board_case_page(request):
    form = ChainBoardCase()
    return render(request, 'stand_board_case.html', context={'form': form})


def stand_package_page(request):
    form = StandPackage()
    return render(request, 'stand_package.html', context={'form': form})


def stand_visual_inspection_page(request):
    form = StandVisualInspection()

    if 'submit_btn_valid' in request.POST and request.method == 'POST':
        form = StandVisualInspection(request.POST)

        if form.is_valid():
            SerialNumBoard.create_board_serial_number(
                form.cleaned_data['board_serial_number'],
                request.user, valid=True)
            Statistic.new_note('Стенд визульного осмотра')

            return redirect('stand-visual-inspection')

    if 'submit_btn_defect' in request.POST and request.method == 'POST':
        form = StandVisualInspection(request.POST)

        if form.is_valid():
            SerialNumBoard.create_board_serial_number(
                form.cleaned_data['board_serial_number'],
                request.user, valid=True)

            return redirect('stand-visual-inspection')

    return render(request, 'stand_visual_inspection.html', context={'form': form})


def stand_diagnostic_page(request):
    form = StandDiagnostic()
    return render(request, 'stand-diagnostic.html', context={'form': form})


def stand_pci_page(request):
    form = StandPCI()
    return render(request, 'stand-pci.html', context={'form': form})


def pci_load_output(request):
    return render(request, 'ajax/pci_output.html', context={})


def diagnostic_load_output(request):
    return render(request, 'ajax/diagnostic_output.html', context={})


def load_modifications(request):
    device_type_id = request.GET.get('device_type_id')
    modification_type = ModificationType.objects.filter(device_type_id=device_type_id).all()
    return render(request, 'ajax/modification_dropdown_list_options.html', context={'modifications': modification_type})
