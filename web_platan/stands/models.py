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
    serial_num_router: маршрутизатор
    ethaddr, eth1addr, eth2addr: mac-адреса
    diag: прохождение диагностики (True | False)
    date_time_pci: дата/время прохождения стенда ПсИ
    date_time_package: дата/время упаковки
    """

    serial_num_pcb_id = models.OneToOneField('SerialNumPCB', on_delete=models.CASCADE,  blank=True, null=True)
    serial_num_board_id = models.OneToOneField('SerialNumBoard', on_delete=models.CASCADE, blank=True, null=True)
    serial_num_case_id = models.OneToOneField('SerialNumCase', on_delete=models.CASCADE, blank=True, null=True)
    serial_num_package_id = models.OneToOneField('SerialNumPackage', on_delete=models.CASCADE, blank=True, null=True)
    serial_num_bp_id = models.OneToOneField('SerialNumBP', on_delete=models.CASCADE, blank=True, null=True)
    serial_num_pki_id = models.OneToOneField('SerialNumPKI', on_delete=models.CASCADE, blank=True, null=True)
    serial_num_router_id = models.OneToOneField('SerialNumRouter', on_delete=models.CASCADE, null=True, blank=True)
    ethaddr_id = models.ForeignKey('Macs', on_delete=models.CASCADE, related_name='mac1', blank=True, null=True)
    eth1addr_id = models.ForeignKey('Macs', on_delete=models.CASCADE, related_name='mac2', blank=True, null=True)
    eth2addr_id = models.ForeignKey('Macs', on_delete=models.CASCADE, related_name='mac3', blank=True, null=True)
    diag = models.BooleanField(default=False)
    date_time_pci = models.CharField(default='No', max_length=150)
    date_time_package = models.CharField(default='No', max_length=150)

    class Meta:
        db_table = 'devices'

    @classmethod
    def create_device(cls, serial_num_board: str) -> list:
        """
        Функция создает новый девайс
        (присваивает ему мак-адреса, плату, возвращает список [serial_num_board, мак-адреса])
        """
        new_device = cls()
        new_device.save()
        new_board = SerialNumBoard(serial_num_board=serial_num_board, device_id=new_device.id)
        new_board.save()
        new_device.serial_num_board_id = new_board.id
        new_device.save()

        snmac_list = [serial_num_board]
        ethaddr_id_list = list()
        macs = Macs.objects.filter(device_id="None")[:3]

        for mac in macs:
            snmac_list.append(mac.mac)
            mac.device_id = new_device.id
            mac.save()
            ethaddr_id_list.append(mac.id)

        new_device.ethaddr_id = ethaddr_id_list[0]
        new_device.eth1addr_id = ethaddr_id_list[1]
        new_device.eth2addr_id = ethaddr_id_list[2]
        new_device.save()

        return snmac_list

    @classmethod
    def update_diag(cls, serial_num):
        """
        Функция меняет значение diag девайса в положение True по серийному номеру платы
        """
        board_id = SerialNumBoard.objects.get(serial_num=serial_num)
        device = cls.objects.get(serial_num_board_id=board_id.id)
        device.diag = True
        device.save()

    @classmethod
    def check_diag(cls, serial_num):
        """
        Функция возвращает реузльтат диагностики девайса по серийному номеру платы
        """
        try:
            board_id = SerialNumBoard.objects.get(serial_num_board=serial_num)
            device = cls.objects.get(serial_num_board_id=board_id.id)
            return device.diag
        except cls.DoesNotExist:
            raise f'Плата с серийным номером {serial_num} отсутствует в базе данных'

    @classmethod
    def write_serial_num_router(cls, serial_num_board, serial_num_router):
        """
        Функция создает новый роутер и записывает информацию в Devices
        """
        board_id = SerialNumBoard.objects.get(serial_num_board=serial_num_board)
        device_id = cls.objects.get(serial_num_board_id=board_id.id)
        new_router = SerialNumRouter(serial_num_router=serial_num_router, device_id=device_id)
        new_router.save()
        router = cls.objects.get(serial_num_board_id=board_id.id)
        router.serial_num_router_id = new_router
        router.save()

    @classmethod
    def get_macs(cls, serial_num):
        """
        Функция возвращает мак-адреса девайса по серийному номеру роутера
        """
        router_id = SerialNumRouter.objects.get(serial_num=serial_num)
        device_id = cls.objects.get(serial_num_router_id=router_id)
        macs = Macs.objects.filter(device_id=device_id)
        mac_list = [mac.mac for mac in macs]
        return mac_list

    @classmethod
    def update_date_time_pci(cls, serial_num):
        """
        Функция обновляет date_time_pci в записи по {serial_num}

        router_id: id роутера, который мы получаем для поиска записи в таблице devices
        """
        router_id = SerialNumRouter.objects.get(serial_num=serial_num)
        device = cls.objects.get(serial_num_router_id=router_id.id)
        device.date_time_pci = str(datetime.now())[:-7].replace(':', '-')
        device.save()

    @classmethod
    def get_date_time_pci(cls, serial_num: str) -> str:
        """
        Функция возвращает время прохождения стенда ПсИ
        """
        router_id = SerialNumRouter.objects.get(serial_num_router=serial_num)
        device = cls.objects.get(serial_num_router_id=router_id.id)
        return str(device.date_time_pci)

    @classmethod
    def update_date_time_package(cls, serial_num: str):
        """
        Функция обновляет date_time_package в записи по {serial_num}

        router_id: id роутера, который мы получаем для поиска записи в таблице devices
        """
        router_id = SerialNumRouter.objects.get(serial_num_router=serial_num)
        device = cls.objects.get(serial_num_router_id=router_id.id)
        device.date_time_package = str(datetime.now())[:-7].replace(':', '-')
        device.save()


class SerialNumPCB(models.Model):
    serial_num_pcb = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True,  blank=True, null=True)

    class Meta:
        db_table = 'serial_num_pcb'


class SerialNumBoard(models.Model):
    """
    Модель таблици serial_num_board

    serial_num_board: серийный номер платы
    visual_inspection: результат прохождения везульного осмотра
    visual_inspection_error_code: код ошибки при условии непрохождения визульного осмотра
    device_id: девайс к котором стоит плата
    """
    serial_num_board = models.CharField(max_length=14, unique=True)
    visual_inspection_author = models.CharField(max_length=150, blank=True, null=True)
    visual_inspection = models.BooleanField(default=False)
    visual_inspection_error_code = models.CharField(max_length=3, blank=True, null=True)
    visual_inspection_datetime = models.CharField(max_length=20, null=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True,  blank=True, null=True)

    class Meta:
        db_table = 'serial_num_board'

    @classmethod
    def check_sn(cls, serial_num_board):
        try:
            cls.objects.get(serial_num_board=serial_num_board)
            return True
        except Exception:
            return False

    @classmethod
    def get_board_count(cls, serial_num):
        return cls.objects.filter(serial_num_board=serial_num).count()

    @classmethod
    def create_board_serial_number(cls, serial_num: str, author: str, valid: bool):
        """
        Функция создает новую запись в таблице serial_num_board

        serial_num: серийный номер новой платы
        author: работник, который провел визульный осмотр
        valid: результат проверки
        """
        new_board = cls(serial_num_board=serial_num,
                        visual_inspection=valid,
                        visual_inspection_author=author,
                        visual_inspection_datetime=datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        new_board.save()


    @classmethod
    def set_visual_inspection(cls, serial_num: str, valid: bool, error_code='None'):
        """
        Функция устанавливает значения:
        visual_inspection={valid}
        visual_inspection_error_code={error_code} записи по serial_num

        serial_num: серийный номер платы
        valid: результат визуального осмотра
        error_code: код ошибки
        """
        board = cls.objects.get(serial_num_board=serial_num)
        board.visual_inspection = valid
        board.visual_inspection_error_code = error_code
        board.save()

    @classmethod
    def get_error_code(cls, serial_num: str) -> str:
        """
        Функция устанавливает значение visual_inspection_error_code='000' записи по serial_num
        serial_num: серийный номер платы, у которой необходимо изменить visual_inspection_error_code
        """
        return cls.objects.get(serial_num_board=serial_num)

    @classmethod
    def update_error_code(cls, serial_num: str):
        """
        Функция устанавливает значение visual_inspection_error_code='000' записи по serial_num

        serial_num: серийный номер платы, у которой необходимо изменить visual_inspection_error_code
        """
        board = cls.objects.get(serial_num_board=serial_num)
        board.visual_inspection_error_code = '000'

    @classmethod
    def is_existence(cls, serial_num: str) -> bool:
        """
        Функция проверяет наличие {serial_num} в базе данных
        """
        try:
            cls.objects.get(serial_num_board=serial_num)
            return True
        except cls.DoesNotExist:
            return False


class SerialNumCase(models.Model):
    serial_num_case = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True,  blank=True, null=True)

    class Meta:
        db_table = 'serial_num_case'


class SerialNumPackage(models.Model):
    serial_num_package = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True,  blank=True, null=True)

    class Meta:
        db_table = 'serial_num_package'


class SerialNumBP(models.Model):
    serial_num_BP = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True,  blank=True, null=True)

    class Meta:
        db_table = 'serial_num_BP'


class SerialNumPKI(models.Model):
    serial_num_pki = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True,  blank=True, null=True)

    class Meta:
        db_table = 'serial_num_pki'


class SerialNumRouter(models.Model):
    serial_num_router = models.CharField(max_length=14, unique=True)
    device_id = models.OneToOneField('Devices', on_delete=models.CASCADE, unique=True, blank=True, null=True)

    class Meta:
        db_table = 'serial_num_router'

    @classmethod
    def check_sn(cls, serial_num_router):
        try:
            cls.objects.get(serial_num_router=serial_num_router)
            return True
        except cls.DoesNotExist:
            return False


class Macs(models.Model):
    mac = models.CharField(max_length=14, unique=True)
    device_id = models.ForeignKey('Devices', on_delete=models.CASCADE, blank=True, null=True, unique=False)

    class Meta:
        db_table = 'macs'


class Statistic(models.Model):
    """
    Модель представляет таблицу Statistic. Ведет сбор статистики об операциях на стендах.

    stand: название стенда, на котором проводилась операция
    date_time: время проведения операции
    """
    manufacturer = models.CharField(max_length=50, default=None)
    stand = models.CharField(max_length=150)
    date_time = models.DateTimeField()

    class Meta:
        db_table = 'statistic'

    @classmethod
    def new_note(cls, serial_num: str, stand: str):
        """
        Функция создает новую запись в таблице Statistic

        stand: стенд на котором проходила операция
        date_time: текущее дата и время
        """
        if serial_num[6:8] == "01":
            manufacturer = "Исток"
        if serial_num[6:8] == "02":
            manufacturer = "EMS Expert"
        if serial_num[6:8] == "03":
            manufacturer = "ТМИ"
        if serial_num[6:8] == "04":
            manufacturer = "Альт Мастер"
        if serial_num[6:8] == "05":
            manufacturer = "ТСИ"
        if serial_num[6:8] == "06":
            manufacturer = "Резанит"

        date_time = datetime.now().date()
        note = cls(manufacturer=manufacturer, stand=stand, date_time=date_time)
        note.save()

    @classmethod
    def get_statistic(cls, date_time: str) -> list:
        """
        Функция возвращает те записи из таблицы statistic, которые соответсвуют переданным параметрам

        stand: название стенда
        date_time: период времени, за который необходимо вернуть данные (например: 'последние 3 месяца')
        returnable_list: возвращаемый функцией список записей из базы данных
        list_statistic: список записей соответсвующих переданному параметру stand
        """
        returnable_list = list()
        list_statistics = cls.objects.all()

        if date_time == 'all time':
            return cls.objects.all()

        if date_time == 'last 3 mouth':
            now = datetime.now().date()
            for i in list_statistics:
                if int((now - i.date_time.date()).days) <= 91:
                    returnable_list.append(i)

        if date_time == 'last week':
            now = datetime.now().date()
            for i in list_statistics:
                if int((now - i.date_time.date()).days) <= 7:
                    returnable_list.append(i)

        if date_time == 'last 24 hour':
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
    def new_note(cls, serial_number, msg):
        new_note = cls(device_serial_num=serial_number, message=msg, date_time=datetime.now().date())
        new_note.save()

    @classmethod
    def check_history(cls, serial_num):
        if cls.objects.filter(device_serial_num=serial_num).exists():
            return True
        else:
            return False

    @classmethod
    def get_history(cls, serial_num: str) -> list:
        """
        Функция возвращает историю устройства по серийному номеру

        serial_num: серийный номер устройства
        """

        return cls.objects.filter(device_serial_num=serial_num)


class GenerateSerialNumbers(models.Model):
    device_type = models.ForeignKey('DeviceType', on_delete=models.CASCADE)
    modification_type = models.ForeignKey('ModificationType', on_delete=models.CASCADE)
    detail_type = models.ForeignKey('DetailType', on_delete=models.CASCADE)
    place_of_production = models.ForeignKey('PlaceOfProduction', on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


class DeviceType(models.Model):
    class Meta:
        verbose_name = 'Тип устройства'
        verbose_name_plural = 'Тип устройства'

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ModificationType(models.Model):
    class Meta:
        verbose_name = 'Тип модификации'
        verbose_name_plural = 'Тип модификации'

    name = models.CharField(max_length=40)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DetailType(models.Model):
    class Meta:
        verbose_name = 'Тип изделия'
        verbose_name_plural = 'Тип изделия'

    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class PlaceOfProduction(models.Model):
    class Meta:
        verbose_name = 'Место производства'
        verbose_name_plural = 'Место производства'

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name