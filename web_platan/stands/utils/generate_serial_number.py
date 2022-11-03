import os
from datetime import date
from ..models import *
from collections import deque



def generate_serial_number(device_type, modification_type, detail_type, place_of_production, count, current_time):
    type_of_device = DeviceType.objects.get(name=str(device_type))
    type_of_device = type_of_device.serial_number_modify
    modification = ModificationType.objects.get(name=str(modification_type))
    modification = modification.serial_number_modify
    detail = DetailType.objects.get(name=str(detail_type))
    detail = detail.serial_number_modify
    place = PlaceOfProduction.objects.get(name=str(place_of_production))
    place = place.serial_number_modify

    year_now = date.today().year
    if year_now == 2022:
        _year = 1
    else:
        _year = year_now - 2022 + 1
    _y = str(hex(_year)).split('x')[-1].capitalize()
    _month = date.today().month
    _m = str(hex(_month)).split('x')[-1].capitalize()
    with open(f'stands/storage/userfiles/SerialNumbers/{device_type}/{modification_type}/{detail_type}/log/how_much', 'r') as f1:
        how_much = list(deque(f1, 1))
    last = int(how_much[0])
    with open(f'stands/storage/userfiles/SerialNumbers/{device_type}/{modification_type}/{detail_type}/log/how_much', 'w') as f2:
        new_last = last + count
        f2.write(str(new_last))
    delta = last + count
    serial_number = type_of_device + modification + detail + place + _y + _m
    serial_number_list = []
    number = ''
    for i in range(last + 1, delta + 1):
        if 1 <= i < 10:
            number = '000' + str(i)
        elif 10 <= i < 100:
            number = '00' + str(i)
        elif 100 <= i < 1000:
            number = '0' + str(i)
        elif 1000 <= i < 10000:
            number = '' + str(i)
        _serial_number = serial_number + number
        serial_number_list.append(_serial_number)

    fullname = f'serial_number_for_{modification_type}/{detail_type}({current_time})'

    if os.path.exists(f'stands/storage/userfiles/SerialNumbers/{device_type}/{modification_type}/{detail_type}'
                      f'/serial_number_for_{modification_type}'):
        pass
    else:
        os.mkdir(f'stands/storage/userfiles/SerialNumbers/{device_type}/{modification_type}/{detail_type}/serial_number_for_{modification_type}')

    with open(f'stands/storage/userfiles/SerialNumbers/{device_type}/{modification_type}/{detail_type}/{fullname}.txt', 'w') as file:
        for i in serial_number_list:
            print(i, file=file)
