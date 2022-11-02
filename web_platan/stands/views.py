from django.shortcuts import render, redirect
from django.http import FileResponse
from datetime import datetime

from .forms import *
from .models import *
from .utils.generate_serial_number import *
from .utils.package import *
from .utils import diagnostic
from .utils import PCI
from .utils.get_host_ip import *
from .utils.group_required import group_required


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
        returnable_statistic_istok = {'stand_visual_inspection': 0,
                                      'stand_diagnostic': 0,
                                      'stand_board_case': 0,
                                      'stand_PCI': 0,
                                      'stand_package': 0}
        returnable_statistic_tsi = {'stand_visual_inspection': 0,
                                    'stand_diagnostic': 0,
                                    'stand_board_case': 0,
                                    'stand_PCI': 0,
                                    'stand_package': 0}

        for stat in statistic:
            if stat.manufacturer == "Исток":
                if stat.stand == "Стенд визуального осмотра":
                    returnable_statistic_istok['stand_visual_inspection'] = returnable_statistic_istok['stand_visual_inspection'] + 1
                if stat.stand == "Стенд диагностики":
                    returnable_statistic_istok['stand_diagnostic'] = returnable_statistic_istok['stand_diagnostic'] + 1
                if stat.stand == "Стенд сборки":
                    returnable_statistic_istok['stand_board_case'] = returnable_statistic_istok['stand_board_case'] + 1
                if stat.stand == "Стенд ПСИ":
                    returnable_statistic_istok['stand_PCI'] = returnable_statistic_istok['stand_PCI'] + 1
                if stat.stand == "Стенд упаковки":
                    returnable_statistic_istok['stand_package'] = returnable_statistic_istok['stand_package'] + 1
            if stat.manufacturer == "ТСИ":
                if stat.stand == "Стенд визуального осмотра":
                    returnable_statistic_tsi['stand_visual_inspection'] = returnable_statistic_tsi['stand_visual_inspection'] + 1
                if stat.stand == "Стенд диагностики":
                    returnable_statistic_tsi['stand_diagnostic'] = returnable_statistic_tsi['stand_diagnostic'] + 1
                if stat.stand == "Стенд сборки":
                    returnable_statistic_tsi['stand_board_case'] = returnable_statistic_tsi['stand_board_case'] + 1
                if stat.stand == "Стенд ПСИ":
                    returnable_statistic_tsi['stand_PCI'] = returnable_statistic_tsi['stand_PCI'] + 1
                if stat.stand == "Стенд упаковки":
                    returnable_statistic_tsi['stand_package'] = returnable_statistic_tsi['stand_package'] + 1

        return render(request, 'statistic.html', context={'statistic_istok': returnable_statistic_istok,
                                                          'statistic_tsi': returnable_statistic_tsi,
                                                          'form': form})

    return render(request, 'statistic.html', context={'form': form})


@group_required('Техническое бюро')
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
            current_time = str(datetime.now())[:-7].replace(' ', '_').replace(':', '-')
            generate_serial_number(device_type, modification_type,
                                   detail_type, place_of_production, count, current_time)
            filename1 = f'stands/storage/userfiles/SerialNumbers/{device_type}/{modification_type}/{detail_type}' \
                        f'/serial_number_for_{modification_type}/{detail_type}({current_time}).txt'
            return FileResponse(open(filename1, 'rb'), as_attachment=True)
    return render(
        request, 'generate_serial_numbers.html', context={'form': form})


@group_required('Стенд сборки')
def stand_board_case_page(request):
    form = ChainBoardCase(request.POST)

    if request.method == 'POST':

        if form.is_valid():
            Devices.write_serial_num_router(
                                            form.cleaned_data['board_serial_number'],
                                            form.cleaned_data['case_serial_number'])

            Statistic.new_note(form.cleaned_data['board_serial_number'], 'Стенд сборки')
            History.new_note(form.cleaned_data['board_serial_number'], msg="СТЕНД СБОРКИ, стенд пройден успешно")
            return redirect('stand-board-case')

    return render(request, 'stand_board_case.html', context={'form': ChainBoardCase()})


@group_required('Стенд упаковки')
def stand_package_page(request):
    form = StandPackage()
    if request.method == 'POST':
        form = StandPackage(request.POST)

        if form.is_valid():
            stickers = start_package_process(form.cleaned_data['device_serial_number'])
            Statistic.new_note(form.cleaned_data['device_serial_number'], 'Стенд упаковки')
            History.new_note(form.cleaned_data['device_serial_number'], msg="СТЕНД УПАКОВКИ, стенд пройден успешно")

            return render(request, 'stand_package.html', context={'form': form, 'stickers': stickers})
    return render(request, 'stand_package.html', context={'form': form})


@group_required('Стенд визуального осмотра')
def stand_visual_inspection_page(request):
    form = StandVisualInspection()

    if 'submit_btn_valid' in request.POST and request.method == 'POST':
        form = StandVisualInspection(request.POST)

        if form.is_valid():
            SerialNumBoard.create_board_serial_number(
                form.cleaned_data['board_serial_number'],
                request.user, valid=True)
            Statistic.new_note(form.cleaned_data['board_serial_number'], 'Стенд визуального осмотра')
            History.new_note(form.cleaned_data['board_serial_number'],
                             msg="СТЕНД ВИЗУАЛЬНОГО ОСМОТРА, стенд пройден успешно")

            return redirect('stand-visual-inspection')

    if 'submit_btn_defect' in request.POST and request.method == 'POST':
        form = StandVisualInspection(request.POST)

        if form.is_valid():
            SerialNumBoard.create_board_serial_number(
                form.cleaned_data['board_serial_number'],
                request.user, valid=False)
            History.new_note(form.cleaned_data['board_serial_number'],
                             msg="СТЕНД ВИЗУАЛЬНОГО ОСМОТРА, стенд не пройден")

            return redirect('stand-visual-inspection')

    return render(request, 'stand_visual_inspection.html', context={'form': form})


@group_required('Стенд диагностики')
def stand_diagnostic_page(request):
    form = StandDiagnostic()
    if request.method == 'POST':
        form = StandDiagnostic(request.POST)
        if form.is_valid():
            board_count = form.cleaned_data['board_count']
            board_serial_number = form.cleaned_data['board_serial_number_1']
            os_modification = 'SP'
            modification_split = board_serial_number[2:4]
            modification_serial_number_os = modification_split + os_modification
            modification_dictionary = {
                '20SP': 'КРПГ.465614.001',
                '31SP': 'КРПГ.465614.001-02',
                '30SP': 'КРПГ.465614.001-03',
                '10SP': 'КРПГ.465614.001-05',
                '41SP': 'КРПГ.465614.001-06',
                '40SP': 'КРПГ.465614.001-07',
                '32SP': 'КРПГ.465614.001-09',
                '33SP': 'КРПГ.465614.001-10',
                '34SP': 'КРПГ.465614.001-11',
                '35SP': 'КРПГ.465614.001-12',
                '42SP': 'КРПГ.465614.001-14',
                '43SP': 'КРПГ.465614.001-15',
                '44SP': 'КРПГ.465614.001-16',
                '45SP': 'КРПГ.465614.001-17',
            }
            modification = modification_dictionary.get(modification_serial_number_os)
            board_serial_number_list = [form.cleaned_data['board_serial_number_1'],
                                        form.cleaned_data['board_serial_number_2'],
                                        form.cleaned_data['board_serial_number_3'],
                                        form.cleaned_data['board_serial_number_4'],
                                        form.cleaned_data['board_serial_number_5']]

            ip = get_ip(request)
            diagnostic.run(board_count, modification, board_serial_number_list, ip)
            return redirect('stand-diagnostic')
    return render(request, 'stand-diagnostic.html', context={'form': form})


@group_required('Стенд ПСИ')
def stand_pci_page(request):
    form = StandPCI()
    if 'pci_start' in request.POST and request.method == 'POST':
        form = StandPCI(request.POST)

        if form.is_valid():
            router_count = form.cleaned_data['router_count']
            router_serial_number = form.cleaned_data['router_serial_number_1']
            os_modification = 'SP'
            modification_split = router_serial_number[2:4]
            modification_serial_number_os = modification_split + os_modification

            modification_dictionary = {
                '20SP': 'КРПГ.465614.001',
                '31SP': 'КРПГ.465614.001-02',
                '30SP': 'КРПГ.465614.001-03',
                '10SP': 'КРПГ.465614.001-05',
                '41SP': 'КРПГ.465614.001-06',
                '40SP': 'КРПГ.465614.001-07',
                '32SP': 'КРПГ.465614.001-09',
                '33SP': 'КРПГ.465614.001-10',
                '34SP': 'КРПГ.465614.001-11',
                '35SP': 'КРПГ.465614.001-12',
                '42SP': 'КРПГ.465614.001-14',
                '43SP': 'КРПГ.465614.001-15',
                '44SP': 'КРПГ.465614.001-16',
                '45SP': 'КРПГ.465614.001-17',
            }
            modification = modification_dictionary.get(modification_serial_number_os)

            router_serial_number_list = [form.cleaned_data['router_serial_number_1'],
                                        form.cleaned_data['router_serial_number_2'],
                                        form.cleaned_data['router_serial_number_3'],
                                        form.cleaned_data['router_serial_number_4'],
                                        form.cleaned_data['router_serial_number_5']]
            ip = get_ip(request)
            PCI.run(router_count, modification, router_serial_number_list, ip)
            return redirect('stand-pci')

    return render(request, 'stand-pci.html', context={'form': form})


def pci_load_output(request):
    return render(request, 'ajax/pci_output.html', context={})


def diagnostic_load_output(request):
    return render(request, 'ajax/diagnostic_output.html', context={})


def load_modifications(request):
    device_type_id = request.GET.get('device_type_id')
    modification_type = ModificationType.objects.filter(device_type_id=device_type_id).all()
    return render(request, 'ajax/modification_dropdown_list_options.html', context={'modifications': modification_type})
