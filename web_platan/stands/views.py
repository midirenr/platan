from django.shortcuts import render
from .forms import *


def index(request):
    return render(
        request,
        'index.html',
        context=
        {

        },
    )


def history_page(request):
    form = HistoryForm()
    return render(request, 'history.html', context={'form': form})


def statistic_page(request):
    form = StatisticForm()
    return render(request, 'statistic.html', context={'form': form})


def generate_serial_numbers_page(request):
    form = GenerateSerialNumbersForm()
    return render(request, 'generate_serial_numbers.html', context={'form': form})


def stand_board_case_page(request):
    form = ChainBoardCase()
    return render(request, 'stand_board_case.html', context={'form': form})


def stand_package_page(request):
    form = StandPackage()
    return render(request, 'stand_package.html', context={'form': form})


def stand_visual_inspection_page(request):
    form = StandVisualInspection()
    return render(request, 'stand_visual_inspection.html', context={'form': form})


def stand_diagnostic_page(request):
    form = StandDiagnostic()
    return render(request, 'stand-diagnostic.html', context={'form': form})


def stand_pci_page(request):
    form = StandPCI()
    return render(request, 'stand-pci.html', context={'form': form})


def pci_load_output(request):
    pass


def diagnostic_load_output(request):
    pass


def load_modifications(request):
    pass
