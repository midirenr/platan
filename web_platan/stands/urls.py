from django.urls import path
from .views import *
urlpatterns = [
    path('', index, name='index'),
    path('generate-serial-numbers/', generate_serial_numbers_page, name='generate-serial-numbers'),
    path('stand-board-case/', stand_board_case_page, name='stand-board-case'),
    path('stand-package/', stand_package_page, name='stand-package'),
    path('stand-visual-inspection/', stand_visual_inspection_page, name='stand-visual-inspection'),
    path('stand-diagnostic/', stand_diagnostic_page, name='stand-diagnostic'),
    path('stand-pci/', stand_pci_page, name='stand-pci'),
    path('history/', history_page, name='history'),
    path('statistic/', statistic_page, name='statistic'),
    # ajax
    path('ajax/load-modifications/', load_modifications, name='ajax_load_modifications'),
    path('ajax/diagnostic-output/', diagnostic_load_output, name='ajax_diag_output'),
    path('ajax/pci-output/', pci_load_output, name='ajax_pci_output')
]
