from datetime import datetime
from django.db import models


class Devices(models.Model):
    """
    Модель представляет таблицу device
    serial_num_pcb_id: плата без компонентов
    serial_num_board_id: плата
    serial_num_case_id: корпус
    serial_num_package: упаковка
    serial_num_bp: блок питания
    serial_num_pki: ?
    serila_num_router: маршрутизатор
    ethaddr, eth1addr, eth2addr: mac-адреса
    diag: прохождение диагностики (True | False)
    date_time_pci: дата/время прохождения стенда ПсИ
    date_time_package: дата/время упаковки
    """

    serial_num_pcb_id = models.OneToOneField('SerialNumPCB', on_delete=models.CASCADE, unique=True)
    serial_num_board_id = models.OneToOneField('SerialNumBoard', on_delete=models.CASCADE, unique=True)
    serial_num_case_id = models.OneToOneField('SerialNumCase', on_delete=models.CASCADE, unique=True)
    serial_num_package_id = models.OneToOneField('SerialNumPackage', on_delete=models.CASCADE, unique=True)
    serial_num_bp_id = models.OneToOneField('SerialNumBP', on_delete=models.CASCADE, unique=True)
    serial_num_pki_id = models.OneToOneField('SerialNumPKI', on_delete=models.CASCADE, unique=True)
    serial_num_router_id = models.OneToOneField('SerialNumRouter', on_delete=models.CASCADE, unique=True)
    ethaddr_id = models.OneToOneField('Macs', on_delete=models.CASCADE, unique=True, related_name='mac1')
    eth1addr_id = models.OneToOneField('Macs', on_delete=models.CASCADE, unique=True, related_name='mac2')
    eth2addr_id = models.OneToOneField('Macs', on_delete=models.CASCADE, unique=True, related_name='mac3')
    diag = models.BooleanField(default=False)
    date_time_pci = models.CharField(default='No', max_length=150)
    date_time_package = models.CharField(default='No', max_length=150)

    class Meta:
        db_table = 'devices'


class SerialNumPCB(models.Model):
    serial_num_pcb = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'serial_num_pcb'


class SerialNumBoard(models.Model):
    serial_num_board = models.CharField(max_length=14, unique=True)
    visual_inspection = models.BooleanField(default=None)
    visual_inspection_error_code = models.CharField(default=None, max_length=3)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'serial_num_board'

    @classmethod
    def set_defect_visual_inspection(cls, serial_num: str, error_code: str):
        cls.objects.get(serial_num=serial_num).update(visual_inspection='False')
        cls.objects.get(serial_num=serial_num).update(visual_inspection_error_code=error_code)

    @classmethod
    def set_valid_visual_inspection(cls, serial_num: str):
        cls.objects.get(serial_num=serial_num).update(visual_inspection='True')

    @classmethod
    def get_error_code(cls, serial_num: str):
        return cls.objects.get(serial_num=serial_num)

    # @classmethod
    # def is_existence(cls, serial_num):
    #     try:
    #         cls.objects.get(serial_num=serial_num)
    #         return True
    #     except cls.


class SerialNumCase(models.Model):
    serial_num_case = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'serial_num_case'


class SerialNumPackage(models.Model):
    serial_num_package = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'serial_num_package'


class SerialNumBP(models.Model):
    serial_num_BP = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'serial_num_BP'


class SerialNumPKI(models.Model):
    serial_num_pki = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'serial_num_pki'


class SerialNumRouter(models.Model):
    serial_num_router = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'serial_num_router'


class Macs(models.Model):
    mac = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True)

    class Meta:
        db_table = 'macs'


class Statistic(models.Model):
    """
    Модель представляет таблицу Statistic. Ведет сбор статистики об операциях на стендах.

    stand: название стенда, на котором проводилась операция
    date_time: время проведения операции
    """
    stand = models.CharField(max_length=150)
    date_time = models.DateTimeField()

    class Meta:
        db_table = 'statistic'

    @classmethod
    def new_note(cls, stand: str):
        """
        Функция создает новую запись в таблице Statistic

        stand: стенд на котором проходила операция
        date_time: текущее дата и время
        """

        date_time = datetime.now().date()
        note = cls(stand=stand, date_time=date_time)
        note.save()

    @classmethod
    def get_statistic(cls, stand: str, date_time: str) -> list:
        """
        Функция возвращает те записи из таблицы statistic, которые соответсвуют переданным параметрам

        stand: название стенда
        date_time: период времени, за который необходимо вернуть данные (например: 'последние 3 месяца')
        returnable_list: возвращаемый функцией список записей из базы данных
        list_statistic: список записей соответсвующих переданному параметру stand
        """
        returnable_list = list()
        list_statistics = cls.objects.filter(stand=stand)

        if date_time == "all time":
            return cls.objects.filter(stand=stand)

        if date_time == "last 3 mouth":
            now = datetime.now().date()
            for i in list_statistics:
                if int((now - i.date_time.date()).days) <= 91:
                    returnable_list.append(i)

        if date_time == "last 7 days":
            now = datetime.now().date()
            for i in list_statistics:
                if int((now - i.date_time.date()).days) <= 7:
                    returnable_list.append(i)

        if date_time == "last 24 hours":
            now = datetime.now().date()
            for i in list_statistics:
                if int((now - i.date_time.date()).days)*24 <= 24:
                    returnable_list.append(i)

        return returnable_list


class History(models.Model):
    """
    Модель таблицы history, хранит историю операций на стендах каждого устройства

    device_serial_num: серийный номер устройства
    message: результат прохождения стенда
    date_time: дата/время прохождения стенда
    """
    device_serial_num = models.CharField(max_length=14)
    message = models.CharField(max_length=255)
    date_time = models.CharField(max_length=150)

    class Meta:
        db_table = 'history'

    @classmethod
    def get_gistory(cls, serial_num: str) -> list:
        """
        Функция возвращает историю устройства по серийному номеру

        serial_num: серийный номер устройства
        """

        return cls.objects.filter(device_serial_num=serial_num)
