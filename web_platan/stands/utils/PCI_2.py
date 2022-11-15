import logging
import traceback
import re
from django.db import connections
from django.db.utils import OperationalError
import yaml
import concurrent.futures
import time
from telnetlib import Telnet
from netmiko import ConnectHandler

from .docx_to_pdf import *
from ..models import *
from .output_file import *


class CustomError(Exception):
    pass


class CustomErrorExtended(Exception):
    pass


class PCI:
    def __init__(self, board_count, modification, board_serial_number_list, host_ip):
        self.board_count = board_count
        self.modification = modification
        self.board_serial_number_list = board_serial_number_list
        self.host_ip = host_ip
        self.ports_check_cmds = [
            'configure terminal', 'vlan 12,34,56,78',
            'interface switchport 1', 'switchport access vlan 12', 'no shutdown', 'exit',
            'interface switchport 2', 'switchport access vlan 12', 'no shutdown', 'exit',
            'interface switchport 3', 'switchport access vlan 34', 'no shutdown', 'exit',
            'interface switchport 4', 'switchport access vlan 34', 'no shutdown', 'exit',
            'interface switchport 5', 'switchport access vlan 56', 'no shutdown', 'exit',
            'interface switchport 6', 'switchport access vlan 56', 'no shutdown', 'exit',
            'interface switchport 7', 'switchport access vlan 78', 'no shutdown', 'exit',
            'interface switchport 8', 'switchport access vlan 78', 'no shutdown', 'exit',
            'interface br112', 'include eth1', 'include eth2', 'no shutdown', 'end'
        ]
        self.modifications_config = {
            'КРПГ.465614.001': 'devices_sp_hdd.yaml',
            'КРПГ.465614.001-01': 'devices_sp_hdd.yaml',
            'КРПГ.465614.001-02': 'devices_sp_pci_2.yaml',
            'КРПГ.465614.001-03': 'devices_sp_pci_0.yaml',
            'КРПГ.465614.001-04': 'devices_sp_hdd.yaml',
            'КРПГ.465614.001-05': 'devices_sp_hdd.yaml',
            'КРПГ.465614.001-06': 'devices_sp_pci_2.yaml',
            'КРПГ.465614.001-07': 'devices_sp_pci_0.yaml',
            'КРПГ.465614.001-08': 'devices_sp_pci_2.yaml',
            'КРПГ.465614.001-09': 'devices_sp_pci_4.yaml',
            'КРПГ.465614.001-10': 'devices_sp_pci_4.yaml',
            'КРПГ.465614.001-11': 'devices_sp_pci_2.yaml',
            'КРПГ.465614.001-12': 'devices_sp_pci_2.yaml',
            'КРПГ.465614.001-13': 'devices_sp_pci_2.yaml',
            'КРПГ.465614.001-14': 'devices_sp_pci_4.yaml',
            'КРПГ.465614.001-15': 'devices_sp_pci_4.yaml',
            'КРПГ.465614.001-16': 'devices_sp_pci_2.yaml',
            'КРПГ.465614.001-17': 'devices_sp_pci_2.yaml',
        }
        # log_debag
        self.logger_debag_1 = logging.getLogger('debag_1')
        self.log_d_1 = logging.FileHandler('stands/utils/logs/PCI/debag_log_1.log')
        self.logger_debag_1.setLevel(logging.DEBUG)
        self.format_d_script = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(stend)s -  %(sn)s  -  %(place)s  -  %(funcName)s: %(message)s",
            '%Y-%m-%d %H:%M:%S')
        self.log_d_1.setFormatter(self.format_d_script)
        self.logger_debag_1.addHandler(self.log_d_1)
        self.logger_debag_2 = logging.getLogger('debag_2')
        self.log_d_2 = logging.FileHandler('stands/utils/logs/PCI/debag_log_2.log')
        self.logger_debag_2.setLevel(logging.DEBUG)
        self.format_d_script = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(stend)s -  %(sn)s  -  %(place)s  -  %(funcName)s: %(message)s",
            '%Y-%m-%d %H:%M:%S')
        self.log_d_2.setFormatter(self.format_d_script)
        self.logger_debag_2.addHandler(self.log_d_2)
        self.logger_debag_3 = logging.getLogger('debag_3')
        self.log_d_3 = logging.FileHandler('stands/utils/logs/PCI/debag_log_3.log')
        self.logger_debag_3.setLevel(logging.DEBUG)
        self.format_d_script = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(stend)s -  %(sn)s  -  %(place)s  -  %(funcName)s: %(message)s",
            '%Y-%m-%d %H:%M:%S')
        self.log_d_3.setFormatter(self.format_d_script)
        self.logger_debag_3.addHandler(self.log_d_3)
        self.logger_debag_4 = logging.getLogger('debag_4')
        self.log_d_4 = logging.FileHandler('stands/utils/logs/PCI/debag_log_4.log')
        self.logger_debag_4.setLevel(logging.DEBUG)
        self.format_d_script = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(stend)s -  %(sn)s  -  %(place)s  -  %(funcName)s: %(message)s",
            '%Y-%m-%d %H:%M:%S')
        self.log_d_4.setFormatter(self.format_d_script)
        self.logger_debag_4.addHandler(self.log_d_4)
        self.logger_debag_5 = logging.getLogger('debag_5')
        self.log_d_5 = logging.FileHandler('stands/utils/logs/PCI/debag_log_5.log')
        self.logger_debag_5.setLevel(logging.DEBUG)
        self.format_d_script = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(stend)s -  %(sn)s  -  %(place)s  -  %(funcName)s: %(message)s",
            '%Y-%m-%d %H:%M:%S')
        self.log_d_5.setFormatter(self.format_d_script)
        self.logger_debag_5.addHandler(self.log_d_5)
        # log_info stend
        self.logger_stend = logging.getLogger('stend')
        self.log_i_stend = logging.FileHandler('stands/utils/logs/PCI/log_stend.log')
        self.logger_stend.setLevel(logging.INFO)
        self.format_i_stend = logging.Formatter("%(asctime)s - %(levelname)s - %(stend)s - %(message)s",
                                                '%Y-%m-%d %H:%M:%S')
        self.log_i_stend.setFormatter(self.format_i_stend)
        self.logger_stend.addHandler(self.log_i_stend)
        # log_info script
        self.logger_script = logging.getLogger('script')
        self.log_i_script = logging.FileHandler('stands/utils/logs/PCI/log_script.log')
        self.logger_script.setLevel(logging.INFO)
        self.format_i_script = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(stend)s -  %(sn)s  -  %(place)s  -  %(funcName)s: %(message)s",
            '%Y-%m-%d %H:%M:%S')
        self.log_i_script.setFormatter(self.format_i_script)
        self.logger_script.addHandler(self.log_i_script)

        self.hdd_present = None
        self.admin_password = None
        self.serviceuser_password = None
        self.master_password = None
        self.nmc_ports_count = None

        self.install_software_timeout = 900
        self.stend = 'СТЕНД_ПСИ'

    @staticmethod
    def verify_yaml_name(yaml_file):
        """
        Ищет файл с введенным именем в текущем каталоге
        :param yaml_file: имя файла конфигурации
        :return: возвращает также имя файла конфигурации. Может отличаться от изначально введенного пользователем
        """
        os.chdir('stands/utils/yamls')
        while True:
            if yaml_file not in filter(os.path.isfile, os.listdir(os.curdir)):
                write_new_note('Отсутствует конфигурационный файл!\n')
                return False
            else:
                os.chdir('..')
                return yaml_file

    def logger_debag(self, msg, sn, place):
        if place == 1:
            self.logger_debag_1.debug(f'{msg}', extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        elif place == 2:
            self.logger_debag_2.debug(f'{msg}', extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        elif place == 3:
            self.logger_debag_3.debug(f'{msg}', extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        elif place == 4:
            self.logger_debag_4.debug(f'{msg}', extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        elif place == 5:
            self.logger_debag_5.debug(f'{msg}', extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        else:
            self.logger_debag_5.debug(f'{msg}', extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})

    def send_command(self, connect, command, sn, place, timeout=10, expect_string='#', just_wait=False):
        """
        Посылает одну команду на устройство
        :param place:
        :param sn:
        :param just_wait: если True, то просто ждем до появления expect_string или до таймаута.
                        Если False, то проверяем, есть ли expect_string в выводе команды
        :param expect_string: ожидаемый вывод в виде текстовой строки
        :param connect: объект подключения по telnet
        :param command: команда в виде текстовой строки
        :param timeout: таймаут
        :return: возвращает вывод команды
        """
        expect_string_bytes = expect_string.encode('utf-8')
        connect.write(f'{command}\n'.encode('utf-8'))
        self.logger_debag(f'send: {command}', sn, place)
        output = connect.read_until(expect_string_bytes, timeout).decode('utf-8', 'ignore')
        self.logger_debag(f'resend: {output}', sn, place)
        if not just_wait:
            if expect_string not in output:
                self.logger_script.error('Неожиданный вывод команды:' f'ВЫВОД КОМАНДЫ: {output}',
                                         extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                return False
        return output

    def send_commands(self, connect, commands, sn, place, timeout=20, expect_string='#'):
        """
        Посылает несколько команд на устройство
        :param sn:
        :param place:
        :param connect: объект подключения по telnet
        :param commands: список команд
        :param timeout: таймаут
        :param expect_string: ожидаемый вывод в виде текстовой строки
        :return: возвращает вывод всех команд в виде списка
        """
        all_output = []
        expect_string_bytes = expect_string.encode('utf-8')
        for command in commands:
            connect.write(f'{command}\n'.encode('utf-8'))
            self.logger_debag(f'send: {command}', sn, place)
            output = connect.read_until(expect_string_bytes, timeout).decode('utf-8', 'ignore')
            all_output.append(output)
            self.logger_debag(f'resend: {output}', sn, place)
            if 'No link.' in output:
                self.logger_script.error('No link. Проблема с соединением.',
                                         extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                return False

            if expect_string not in output:
                self.logger_script.error('Неожиданный вывод команды:' f'ВЫВОД КОМАНДЫ: {all_output}',
                                         extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                return False

        return all_output

    def get_ip(self):
        try:
            self.logger_stend.info('Получении ip хоста...', extra={'stend': f'{self.stend}'})
            write_new_note('Получении ip хоста..\n')
            netplan_config_name = os.listdir('/etc/netplan')[0]
            netplan_config_file = f'/etc/netplan/{netplan_config_name}'
            with open(netplan_config_file) as f:
                params_netplan = yaml.safe_load(f)
            self.logger_stend.info('Ip хоста успешно получен...', extra={'stend': f'{self.stend}'})
            write_new_note('Ip хоста успешно получен...\n')
            return True
        except CustomError as e:
            self.logger_stend.error(e)
            return False

    def connect_to_db(self):
        write_new_note('Проверка подключения к БД...\n')
        self.logger_stend.info('Проверка подключения к БД...', extra={'stend': f'{self.stend}'})
        try:
            db_conn = connections['default']
            test_connections = db_conn.cursor()
            self.logger_stend.info('Подключение к БД успешно!', extra={'stend': f'{self.stend}'})
            write_new_note('Подключение к БД успешно!\n')

            return True
        except OperationalError:
            write_new_note(f'Не удается подключиться к базе MAC адресов, выполнение программы невозможно\n')
            self.logger_stend.error(f'Не удается подключиться к базе MAC адресов, выполнение программы невозможно')
            return False

    def login_to_router(self, connect, sn, place):
        """
        Функция для залогинивания в маршрутизатор
        :param place:
        :param sn:
        :param connect: объект подключения по telnet
        :return: возвращает prompt
        """
        garbage = connect.read_very_eager().decode('utf-8', 'ignore')  # вычитываем буфер для его очистки, игнорируя
        # байты, которые не декодируются utf-8
        self.logger_debag(garbage, sn, place)
        prompt = self.send_command(connect, '', sn, place, timeout=8, just_wait=True)  # посылаем перевод строки
        time.sleep(10)
        if '#' in prompt:
            connect.write(b'\x03')
            self.send_command(connect, 'end', sn, place)
        elif 'login:' in prompt:
            self.send_command(connect, 'admin', sn, place, expect_string='Password')
            output = self.send_command(connect, f'{self.admin_password}', sn, place, just_wait=True)
            self.logger_debag(output, sn, place)
        elif 'Password:' in prompt:
            self.send_command(connect, '', sn, place, expect_string='login')
            self.send_command(connect, 'admin', sn, place, expect_string='Password')
            self.send_command(connect, f'{self.admin_password}', sn, place)
        else:
            self.logger_script.error('Неожиданное приглашение cli после установки ПО',
                                     extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('Неожиданное приглашение cli после установки ПО\n')
            return False
        return prompt

    def tcp_restart(self):
        try:
            write_new_note('Включение tcp-to-serial мостов...\n')
            self.logger_stend.info('Включение tcp-to-serial мостов...', extra={'stend': f'{self.stend}'})
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                bridge_restart_result = executor.map(self.tcp_to_serial_bridge_restart_ssh,
                                                     list(range(1, int(self.board_count) + 1)))
                if not bridge_restart_result:
                    return False
            return True
        except:
            return False

    def tcp_to_serial_bridge_restart_ssh(self, board_count):
        """
        Функция перезапускает tcp-to-serial мост по ssh
        :param board_count:
        :return: ничего
        """
        try:
            host_config = {
                'device_type': 'linux',
                'host': self.host_ip,
                'username': 'istok',
                'password': 'istok',
                'secret': 'istok',
                'port': '22',
            }
            ssh = ConnectHandler(**host_config)
            ssh.enable()
            ssh.send_command('sudo systemctl restart tcp-to-serial-bridge-router1.service')
            command_status = ssh.send_command('sudo systemctl status tcp-to-serial-bridge-router1.service')
            if 'active (running)' not in command_status:
                self.logger_stend.error(f'Не удается запустить сервис tcp-to-serial-bridge-router{board_count}, \
                            выполнение программы невозможно', extra={'stend': f'{self.stend}'})
                write_new_note(f'Не удается запустить сервис tcp-to-serial-bridge-router_ssh\n')
                return False
            else:
                self.logger_stend.info(f'Cервис tcp-to-serial-bridge-router{board_count} запущен',
                                       extra={'stend': f'{self.stend}'})
                write_new_note(f'Cервис tcp-to-serial-bridge-router{board_count} запущен\n')
            ssh.disconnect()
            return True
        except:
            return False

    def host_service_check_ssh(self, service):
        """
        Проверка состояния сервисов на хосте. Если сервис не запущен, выполнение скрипта заканчивается
        :param service: имя сервиса
        :return: ничего
        """
        write_new_note('Проверка сервиса {}...\n'.format(service))
        try:
            host_config = {
                'device_type': 'linux',
                'host': self.host_ip,
                'username': 'istok',
                'password': 'istok',
                'secret': 'istok',
                'port': '22',
            }
            ssh = ConnectHandler(**host_config)
            ssh.enable()
            command_status = ssh.send_command('sudo systemctl status {service}.service')
            if 'active (running)' not in command_status:
                ssh.send_command(f"sudo systemctl restart {service}.service ")
                command_status = ssh.send_command(f"sudo systemctl status {service}.service")
                if 'active (running)' not in command_status:
                    self.logger_stend.error(f'Сервис {service} не удается запустить, \
                            выполнение программы невозможно', extra={'stend': f'{self.stend}'})
                    write_new_note('Сервис не удается запустить\n'.format(service))
                    return False
                else:
                    self.logger_stend.info(f'Cервис {service} запущен', extra={'stend': f'{self.stend}'})
                    write_new_note('Сервис {} запущен\n'.format(service))
                    ssh.disconnect()
                    return True

            else:
                self.logger_stend.info(f'Cервис {service} запущен', extra={'stend': f'{self.stend}'})
                write_new_note('Сервис {} запущен\n'.format(service))
                ssh.disconnect()
                return True
        except:
            return False

    def enter_uboot(self, connect, phase, sn, place):
        """
        Вход в Uboot маршрутизатора
        :param sn:
        :param place:
        :param connect: объект подключения по telnet
        :param phase: фаза (install или erase)
        :return: приглашение cli после входа в Uboot
        """
        console_output = connect.read_until(b'Hit any key to stop autoboot', timeout=20).decode('utf-8', 'ignore')
        self.logger_debag(console_output, sn, place)
        if phase == 'install' and 'Hit any key to stop autoboot' not in console_output:
            self.logger_script.error('Не удалось войти в U-BOOT...',
                                     extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            return False

        if phase == 'erase' and 'Hit any key to stop autoboot' not in console_output:
            return False

        connect.write(b'a')
        time.sleep(1)
        connect.write(b'\x1b[B\n')
        time.sleep(1)
        connect.write(b'\x1b[B\n')
        time.sleep(1)
        connect.write(b'\r')
        time.sleep(1)
        uboot_prompt = connect.read_very_eager().decode('utf-8')
        self.logger_debag(uboot_prompt, sn, place)
        self.logger_script.info('Вход в U-boot выполнен успешно',
                                extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        return uboot_prompt, console_output

    def init_disk(self, connect, sn, place):
        time.sleep(10)
        sata_list = []
        for _ in range(6):
            time.sleep(3)
            sata_info = self.send_command(connect, 'sata init', sn, place, timeout=30)
            if not sata_info:
                return False
            sata_list.append(sata_info)
        check_list = []
        for i in sata_list:
            if 'Product model number: nanoSSD 3ME3' in i:
                check_list.append(True)

        if len(check_list) >= 5:
            check_status = True
        else:
            check_status = False

        if check_status:
            self.logger_script.info(f'SSD удалось инициализировать!'
                                    f' SSD удалось инициализировать {len(check_list)} раз из 6',
                                    extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('SSD удалось инициализировать!\n')
            return sata_info
        else:
            self.logger_script.error('SSD работает нестабильно!',
                                     extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('SSD работает нестабильно\n')
            return False

    def set_bootmenu(self, connect, phase, sn, place):
        """
        Настройка Bootmenu для автоматической установки ПО
        :param place:
        :param sn:
        :param phase:
        :param master_password: пароль учетки master
        :param serviceuser_password: пароль учетки serviceuser
        :param admin_password: пароль учетки admin
        :param ftp_directory: ftp директория с пакетами ПО
        :param host_ip: адрес tftp/ftp сервера
        :param connect: объект подключения по telnet
        :return:
        """
        if phase == 'install':
            initrd_file_name = 'initrd.gz'
        elif phase == 'erase':
            initrd_file_name = 'initrd_erase.gz'

        if self.modification == 'КРПГ.465614.001-05' or self.modification == 'КРПГ.465614.001-04':
            setenv_commands = [
                f'usb start ; \
                env set phy_sfp 1 ; \
                dhcp ; \
                setenv serverip 192.168.1.2; \
                setenv fdt_addr_n 0x85D00000 ; \
                setenv fdt_file_name baikal.dtb ; \
                setenv initrd_addr_n 0x86000000 ; \
                setenv initrd_file_name {initrd_file_name} ; \
                setenv kernel_addr_n 0x80100000 ; \
                setenv kernel_file_name vmlinux.bin ; \
                setenv ci_installed 1 ; \
                setenv bootargs console=ttyS0,115200n8 usbcore.autosuspend=-1 \
                ei-auto_install=true ei-install_disk=/dev/sda ei-passwd_admin={self.admin_password} \
                ei-passwd_serviceuser={self.serviceuser_password} ei-passwd_master={self.master_password} ; \
                setenv sata_setup_disk "sata init; run sata_common_disk" ; \
                saveenv ; \
                run net_load_all_tftp ; run all_bootnr'
            ]
        else:
            setenv_commands = [
                f'usb start ; \
                dhcp ; \
                setenv serverip 192.168.1.2 ; \
                setenv fdt_addr_n 0x85D00000 ; \
                setenv fdt_file_name baikal.dtb ; \
                setenv initrd_addr_n 0x86000000 ; \
                setenv initrd_file_name {initrd_file_name} ; \
                setenv kernel_addr_n 0x80100000 ; \
                setenv kernel_file_name vmlinux.bin ; \
                setenv bootargs console=ttyS0,115200n8 usbcore.autosuspend=-1 \
                ei-auto_install=true ei-install_disk=/dev/sda ei-passwd_admin={self.admin_password} \
                ei-passwd_serviceuser={self.serviceuser_password} ei-passwd_master={self.master_password} ; \
                saveenv ; \
                run net_load_all_tftp ; run all_bootnr'

            ]
        self.logger_script.info('Начало наcтройки BOOTMENU', extra={'sn': f'{sn}', 'stend': f'{self.stend}',
                                                                    'place': f'{place}'})
        set_bootmenu_output = self.send_commands(connect, setenv_commands, sn, place, timeout=90)
        self.logger_script.info('BOOTMENU натсроено', extra={'sn': f'{sn}', 'stend': f'{self.stend}',
                                                             'place': f'{place}'})
        write_new_note('BOOTMENU натсроено\n')
        if 'Loading' in set_bootmenu_output[0]:
            self.logger_script.info('Началась загрузка файлов по TFTP',
                                    extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        return set_bootmenu_output

    def timer(self):
        write_new_note('0.00%')
        count = self.install_software_timeout
        while count >= 0:
            count = count - 1
            time.sleep(1)
            set_time(f'{(self.install_software_timeout-count)/(self.install_software_timeout/100)}'[:4] + '%')

        set_time('Установка завершена!\n')

    def install_software(self, connect, phase, sn, place):
        """
        Запуск установки ПО
        :param sn:
        :param place:
        :param phase: фаза установки: install или erase
        :param wait_time: время установки в секундах
        :param connect: объект подключения по telnet
        :return: возвращает первые 5 секунд вывода с начала установки софта
        """
        console_output = connect.read_until(b'  No volume groups found', timeout=120).decode('utf-8')
        self.logger_debag(f'Вывод в консоль перед установкой файлов с флешки: {console_output}', sn, place)
        if phase == 'install' and '  No volume groups found' in console_output:
            self.logger_script.info('Загрузка файлов по TFTP прошла успешно. Началась установка файлов с флешки',
                                    extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('Загрузка файлов по TFTP прошла успешно. Началась установка файлов с флешки\n')
        elif phase == 'install' and 'Error: Install disk with label: INSTALLER not found' in console_output:
            self.logger_script.error('Не удалось обнаружить флешку с LABEL: INSTALLER',
                                     extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('Не удалось обнаружить флешку\n')
            return False

        elif phase == 'install' and 'Error while generating lvm2 partitions' in console_output:
            self.logger_script.error('Возникли проблемы с разбиением диска на разделы',
                                     extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('Возникли проблемы с разбиением диска на разделы\n')
            return False

        elif phase == 'install' and 'Disk too small' in console_output:
            self.logger_script.error('Возникли проблемы с определением размера SSD',
                                     extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('Возникли проблемы с определением размера SSD\n')
            return False

        elif phase == 'install' and 'Lvm group vg0 already exists' in console_output:
            self.logger_script.error('На флешке/HDD найдены разделы. Необходимо отформатировать флешку/HDD',
                                     extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('На флешке/HDD найдены разделы. Необходимо отформатировать флешку/HDD\n')
            return False

        else:
            self.logger_script.error('Не удалось начать установку ПО по неизвестным причинам',
                                     extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('Не удалось начать установку ПО по неизвестным причинам\n')
            return False

        start_installing_sw = connect.read_very_eager().decode('utf-8')
        self.timer()
        return start_installing_sw

    def post_install_check(self, connect, sn, place):
        """
        Проверка того, что роутер загрузился после установки ПО. Пробуем логиниться 5 раз с интервалом 15 секунд
        :param sn:
        :param place:
        :param connect: объект подключения по telnet
        :return: результат "show version"
        """
        output_before_check = connect.read_very_eager().decode('utf-8', 'ignore')
        output_before_check_min = output_before_check[-5800::]
        self.logger_debag(f'ВЫВОД ДО ПОПЫТКИ ЗАЛОГИНИВАНИЯ: {output_before_check_min}', sn, place)
        if 'Kernel panic' in output_before_check:
            self.logger_script.error('При загрузке после установки ПО возник Kernel Panic',
                                     extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            return False

        elif 'Waiting for full initialization of mprdaemon' in output_before_check:
            self.logger_script.info('ПО было успешно установленно',
                                    extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        else:
            self.logger_script.warning('Возможно ПО не было установлено, либо было установлено с ошибкой',
                                       extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            return False

        for i in range(3):
            try:
                self.logger_debag(f'Попытка залогиниться №{i + 1}', sn, place)
                self.login_to_router(connect, sn, place)
                break
            except CustomErrorExtended as e:
                self.logger_script.error(e, extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                failed_prompt_result = e
                time.sleep(15)
        if i == 5:
            self.logger_script.error(
                f'Маршрутизатор не загрузился после установки ПО, не найдено приглашение cli {failed_prompt_result}',
                extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            return False

        time.sleep(5)
        version = self.send_command(connect, 'show version', sn, place)
        self.logger_script.info('Вход на устройство выполнен успешно',
                                extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        write_new_note('Вход на устройство выполнен успешно\n')
        return version

    def hdd_check(self, connect, sn, place):
        """
        Проверка наличия hdd
        :param place:
        :param sn:
        :param connect: объект подключения по telnet
        :return: вывод lshw и результат проверки
        """
        self.login_to_router(connect, sn, place)
        self.send_command(connect, 'root-shell', sn, place, timeout=20, expect_string='>')
        self.send_command(connect, self.master_password, sn, place)
        lshw_command = self.send_command(connect, 'lshw -businfo', sn, place, timeout=25)
        self.send_command(connect, 'exit', sn, place)
        if 'scsi@1:0.0.0' not in lshw_command:
            check_result_out = 'Внешний HDD не найден'
            self.logger_script.info(check_result_out, extra={'sn': f'{sn}', 'stend': f'{self.stend}',
                                                             'place': f'{place}'})
            write_new_note('Внешний HDD не найден\n')
        else:
            check_result_out = 'Внешний HDD найден'
            self.logger_script.error(check_result_out, extra={'sn': f'{sn}', 'stend': f'{self.stend}',
                                                              'place': f'{place}'})
            write_new_note('Внешний HDD не найден\n')
        if 'scsi@0:0.0.0' not in lshw_command:
            check_result_in = 'Внутренний HDD не найден'
            self.logger_script.info(check_result_in, extra={'sn': f'{sn}', 'stend': f'{self.stend}',
                                                            'place': f'{place}'})
            write_new_note('Внутренний HDD не найден\n')
        else:
            check_result_in = 'Внутренний HDD найден'
            self.logger_script.error(check_result_in, extra={'sn': f'{sn}', 'stend': f'{self.stend}',
                                                             'place': f'{place}'})
            write_new_note('Внутренний HDD найден\n')

        return lshw_command, check_result_out, check_result_in

    def flash_check(self, connect, hdd_present, hdd_check_result, sn, place):
        """
        Проверка наличия двух флешек
        :param place:
        :param sn:
        :param connect: объект подключения по telnet
        :param hdd_present: признак наличия hdd, указывается в yaml файле
        :param hdd_check_result: результат проверки hdd
        :return: вывод lshw и результат проверки
        """
        if hdd_present:
            if hdd_check_result[1] == 'Внешний HDD найден' and hdd_check_result[2] == 'Внутренний HDD найден':
                flash1 = '/dev/sdc'
                flash2 = '/dev/sdd'
            elif hdd_check_result[1] == 'Внешний HDD не найден' and hdd_check_result[2] == 'Внутренний HDD найден':
                flash1 = '/dev/sdb'
                flash2 = '/dev/sdc'
            elif hdd_check_result[1] == 'Внешний HDD найден' and hdd_check_result[2] == 'Внутренний HDD не найден':
                flash1 = '/dev/sdb'
                flash2 = '/dev/sdc'
        else:
            flash1 = '/dev/sdb'
            flash2 = '/dev/sdc'
        self.login_to_router(connect, sn, place)
        self.send_command(connect, 'root-shell', sn, place, timeout=20, expect_string='>')
        self.send_command(connect, self.master_password, sn, place)
        lshw_command = self.send_command(connect, 'lshw -businfo', sn, place, timeout=25)
        self.send_command(connect, 'exit', sn, place)
        if flash1 not in lshw_command or flash2 not in lshw_command:
            check_result = 'По крайней мере один flash накопитель не определился, возможно, USB порты неисправны'
            self.logger_script.error(check_result, extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        else:
            check_result = 'Flash накопители найдены'
            self.logger_script.info(check_result, extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
        return lshw_command, check_result

    def nmc_check(self, connect):
        self.login_to_router(connect)
        self.send_command(connect, 'root-shell', expect_string='>')
        self.send_command(connect, self.master_password)
        lshw_command = self.send_command(connect, 'lshw -businfo -c network', timeout=25)
        logging.verbose(lshw_command)
        self.send_command(connect, 'exit')
        pci_addr = 'pci@0000:01:00'
        for port_num in range(self.nmc_ports_count):
            if f'{pci_addr}.{port_num}' in lshw_command:
                check_result = 'Все порты NMC модуля найдены'
                write_new_note('Все порты NMC модуля найдены\n')
            else:
                check_result = 'По крайней мере один порт NMC модуля не найден'
                write_new_note('По крайней мере один порт NMC модуля не найден\n')
        logging.verbose(check_result)
        return lshw_command, check_result

    def ports_check(self, connect, commands, dev_num, sn, place):
        """
        Проверка работоспособности портов
        :param place:
        :param sn:
        :param connect: объект подключения по telnet
        :param commands: список с командами для настройки роутера
        :param dev_num: номер проверяемого устройства
        :return: результат пинга
        """
        self.login_to_router(connect, sn, place)
        self.send_commands(connect, commands, sn, place, expect_string='admin@sr-be')
        third_octet = 200 + dev_num
        # отправляем 5 пакетов чтобы заполнились ARP и FDB таблицы на устройствах, потом отправляем тестовые 30 пакетов
        try:
            host_config = {
                'device_type': 'linux',
                'host': self.host_ip,
                'username': 'istok',
                'password': 'istok',
                'secret': 'istok',
                'port': '22',
            }
            ssh = ConnectHandler(**host_config)
            ssh.enable()
            ssh.send_command(f'ping 192.168.{third_octet}.1 -c 5', read_timeout=40.0)
            ping_result = ssh.send_command(f'ping 192.168.{third_octet}.1 -c 30 -i 0,2', read_timeout=40.0)
            self.logger_debag(ping_result, sn, place)
            return ping_result
        except:
            write_new_note("Не удалось подключится!\n")
            return False

    def erase_disk(self, connect, sn, place):
        self.send_command(connect, 'root-shell', sn, place, timeout=20, expect_string='>')
        self.send_command(connect, self.master_password, sn, place)
        self.send_command(connect, 'fdisk /dev/sdb', sn, place, timeout=10, expect_string='Команда (m для справки): ')
        self.send_command(connect, 'd', sn, place, timeout=10, expect_string='Команда (m для справки): ')
        self.send_command(connect, '1', sn, place, timeout=10, expect_string='Команда (m для справки): ')
        self.send_command(connect, 'd', sn, place, timeout=10, expect_string='Команда (m для справки): ')
        fdisk_info = self.send_command(connect, 'w', sn, place, timeout=10)
        if 'Синхронизируются диски' in fdisk_info:
            self.send_command(connect, 'q', sn, place, timeout=5)
            self.send_command(connect, 'exit', sn, place, timeout=5)
            self.logger_script.info(f'Удаление разделов выполнено успешно',
                                    extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('Удаление разделов выполнено успешно\n')
            return fdisk_info
        else:
            self.logger_script.error(f'При удалении разделов возникла ошибка',
                                     extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
            write_new_note('При удалении разделов возникла ошибка\n')

    def create_protocol(self, device_num, serial_num_router, result):
        number = serial_num_router[-5::]
        flash_result = result[f'device_num_{device_num}']['flash_check_result'][1]
        losses = re.findall(r'\d+% packet loss', result[f'device_num_{device_num}']['ping_result'])[0]
        if self.hdd_present:
            ext_slot_result = result[f'device_num_{device_num}']['hdd_check_result'][1]
        elif self.nmc_ports_count != 0:
            ext_slot_result = result[f'device_num_{device_num}']['nmc_check_result'][1]
        if self.hdd_present or self.nmc_ports_count != 0:
            if ext_slot_result in ['HDD найден',
                                   'Все порты NMC модуля найдены'] and flash_result ==\
                                   'Flash накопители найдены' and losses == '0% packet loss':
                control_test_0 = 'Пройдено'
                control_test_1 = 'Пройдено'
            else:
                control_test_0 = 'Не пройдено'
                control_test_1 = 'Пройдено'
        else:
            if flash_result == 'Flash накопители найдены' and losses == '0% packet loss':
                control_test_0 = 'Пройдено'
                control_test_1 = 'Пройдено'
            else:
                control_test_0 = 'Не пройдено'
                control_test_1 = 'Пройдено'
        input_docx = fill_the_doc(number, serial_num_router, self.modification, control_test_0, control_test_1)
        try:
            convert_docx_to_pdf(input_docx)
            return True
        except:
            return False

    def hw_check(self, device):
        """
       Проверка работоспособности АП с установкой и удалением специальной версии ПО
       :param device: список параметров для подключения через tcp-to-serial мост
       :return: словарь со значениями, выдаваемыми в консоль в процессе установки ПО
       """
        device_num = str(device['port'])[2:]
        result = {f'device_num_{device_num}': {}}
        try:
            with Telnet(self.host_ip, device['port'], timeout=30) as connect:
                phase = 'install'

                sn = self.board_serial_number_list[int(device_num) - 1]
                place = self.board_serial_number_list.index(sn) + 1
                result[f'device_num_{device_num}']['sn'] = sn

                # Вход в uboot устройства
                write_new_note(f'Вход в Uboot устройства {device_num}...\n')
                self.logger_script.info(f'Вход в Uboot устройства',
                                        extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                result[f'device_num_{device_num}']['uboot_prompt'] = self.enter_uboot(connect, phase, sn, place)

                # Инициализация SSD
                write_new_note(f'Инициализация SSD устойства {device_num}...\n')
                self.logger_script.info(f'Инициализация SSD устойства',
                                        extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                result[f'device_num_{device_num}']['sata_info'] = self.init_disk(connect, sn, place)

                # Инициализация bootmenu
                write_new_note(f'Настройка BOOTMENU устройства {device_num}...\n')
                self.logger_script.info(f'Настройка Bootmenu устройства',
                                        extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                result[f'device_num_{device_num}']['bootmenu_1_install'] = self.set_bootmenu(connect, phase,
                                                                                             sn, place)

                # Установка ПО на устройство
                write_new_note(f'Установка ПО на устройство {device_num}...\n')
                self.logger_script.info(f'Установка ПО на устройство',
                                        extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                time.sleep(5)
                result[f'device_num_{device_num}']['start_installing_sw'] = self.install_software(connect, phase, sn,
                                                                                                  place)

                # Проверки устройства после установки ПО
                write_new_note(f'Вход для проведения проверок на устройство {device_num}...\n')
                self.logger_script.info(f'Вход для проведения проверок на устройство',
                                        extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                result[f'device_num_{device_num}']['post_install_check_result'] = self.post_install_check(connect, sn,
                                                                                                          place)

                # Проверка наличия HDD на устройстве
                if self.hdd_present:
                    write_new_note(f'Проверка наличия HDD на устройстве {device_num}...\n')
                    self.logger_script.info(f'Проверка наличия HDD на устройстве',
                                            extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                    result[f'device_num_{device_num}']['hdd_check_result'] = self.hdd_check(connect, sn, place)
                else:
                    result[f'device_num_{device_num}']['hdd_check_result'] = 'Исполнение без HDD, ' \
                                                                             'проверка наличия HDD не проводилась'

                # Проверка наличия 2-х Flash накопителей
                write_new_note(f'Проверка наличия 2-х Flash накопителей на устройстве {device_num}...\n')
                self.logger_script.info(f'Проверка наличия 2-х Flash накопителей на устройстве',
                                        extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                result[f'device_num_{device_num}']['flash_check_result'] =\
                    self.flash_check(connect, self.hdd_present, result[f'device_num_{device_num}']['hdd_check_result'],
                                     sn, place)

                # Проверка NMC модуля на устройстве
                if self.nmc_ports_count != 0:
                    write_new_note(f'Проверка NMC модуля на устройстве {device_num}...\n')
                    result[f'device_num_{device_num}']['nmc_check_result'] = self.nmc_check(connect)
                else:
                    result[f'device_num_{device_num}']['nmc_check_result'] = 'Исполнение без NMC модуля, проверка ' \
                                                                             'наличия NMC модуля не проводилась '

                # Проверка работоспособности портов на устройстве
                write_new_note(f'Проверка работоспособности портов на устройстве {device_num}...\n')
                self.logger_script.info(f'Проверка работоспособности портов на устройстве',
                                        extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                result[f'device_num_{device_num}']['ping_result'] = self.ports_check(connect, self.ports_check_cmds,
                                                                                     device['port'] - 230, sn, place)

                # Удаление разделов на диске
                if self.nmc_ports_count == 0:
                    write_new_note(f'Удаление разделов на диске {device_num}...\n')
                    self.logger_script.info(f'Удаление разделов на диске',
                                            extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                    result[f'device_num_{device_num}']['erase_disk'] = self.erase_disk(connect, sn, place)
                else:
                    result[f'device_num_{device_num}'][
                        'erase_disk'] = 'Удаление разделов не проводилось, так как исполнение с NMC модулем'

                # Создание протокола проверки изделия
                write_new_note_pci(f'Создание протокола проверки изделия для устройства {device_num}...')
                self.logger_script.info(f'Создание протокола проверки изделия для устройства',
                                        extra={'sn': f'{sn}', 'stend': f'{self.stend}', 'place': f'{place}'})
                self.create_protocol(device_num, sn, result)

                result[f'device_num_{device_num}']['error'] = 'False'  # признак не сработавшего исключения
                return result

        except CustomErrorExtended as e:
            result[f'device_num_{device_num}']['error'] = f'Ошибка c устройством {device_num}'  # признак сработавшего
            # исключения
            result[f'device_num_{device_num}']['error_details'] = e.args
            return result
        except:
            self.logger_debag(traceback.format_exc(), sn, place)
            result[f'device_num_{device_num}']['error'] = f'Ошибка c устройством {device_num}: неизвестная ошибка'
            result[f'device_num_{device_num}']['error_details'] = traceback.format_exc()
            return result

    def start_pci(self):
        # Проверка yaml файлов
        y_f = self.modifications_config.get(self.modification)
        yaml_file = self.verify_yaml_name(y_f)
        if not yaml_file:
            return False

        # Запись конфигураций
        with open(f'yamls/{yaml_file}') as f:
            params = yaml.safe_load(f)
        self.hdd_present = params['hdd_present']
        self.admin_password, self.serviceuser_password, self.master_password = list(params['passwords'].values())
        self.nmc_ports_count = params['nmc_ports_count']
        devices = {}
        for i in range(int(self.board_count)):
            devices[f'device{i}'] = params['router_template'].copy()
        i = 0
        for item in devices.items():
            item[1]['port'] = 231 + i
            i += 1
        device_list = []
        for i in range(len(devices)):
            device_list.append(devices[f'device{i}'])

        # Получение ip хоста
        check_ip = self.get_ip()
        if not check_ip:
            return False

        # Подключение к базе данных
        check_db = self.connect_to_db()
        if not check_db:
            return False

        # Включение tcp мостов
        check_tcp = self.tcp_restart()
        if not check_tcp:
            return False

        # Проверка tftp сервиса
        ssh_tftpd_check = self.host_service_check_ssh('tftpd-hpa')
        if not ssh_tftpd_check:
            return False

        # Проверка ftp сервиса
        ssh_vsftpd_check = self.host_service_check_ssh('vsftpd')
        if not ssh_vsftpd_check:
            return False

        # запуск инсталляции ПО и проверок
        result = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
            hw_check_result = executor.map(self.hw_check, device_list)

        result_list = list(hw_check_result)
        for i in range(len(result_list)):
            result.update(result_list[i])

        # вывод результатов теста на экран
        for dev_num in range(1, len(result) + 1):
            serial_num_board = self.board_serial_number_list[int(dev_num) - 1]
            place = self.board_serial_number_list.index(serial_num_board) + 1
            write_new_note(f'\nРезультат для устройства {dev_num}:\n')
            if 'неизвестная ошибка' in result[f'device_num_{dev_num}']['error']:
                write_new_note('>>>Неуспех. Возникла неизвестная ошибка<<<\n')

                self.logger_script.error('Устройство закончило работу с неизвестной ошибкой',
                                         extra={'sn': f'{serial_num_board}', 'stend': f'{self.stend}',
                                                'place': f'{place}'})
                SerialNumBoard.set_visual_inspection(serial_num_board, valid=True, error_code='666')
                History.new_note(serial_num_board, 'СТЕНД_ДИАГНОСТИКИ, плата закончиала работу с неизвестной ошибкой!')
                Repair.new_note(serial_num_board, 'Плата закончиала работу с неизвестной ошибкой!')
                return False
            elif 'Ошибка c устройством' in result[f'device_num_{dev_num}']['error']:
                error_string = result[f'device_num_{dev_num}']['error_details'][0][0]
                write_new_note(f'>>>Неуспех. ПО не было установлено/удалено: {error_string}<<<\n')
                error_code = result[f'device_num_{dev_num}']['error_details'][0][2]
                self.logger_script.error(f'Устройство закончило работу с ошибкой: {error_string}',
                                         extra={'sn': f'{serial_num_board}', 'stend': f'{self.stend}',
                                                'place': f'{place}'})
                SerialNumBoard.set_visual_inspection(serial_num_board, valid=True, error_code=error_code)
                History.new_note(serial_num_board,
                                 f'СТЕНД_ДИАГНОСТИКИ, плата закончиала работу с ошибкой {error_code}!')
                Repair.new_note(serial_num_board, error_code)
                return False
            else:
                flash_result = result[f'device_num_{dev_num}']['flash_check_result'][1]
                losses = re.findall(r'\d+% packet loss', result[f'device_num_{dev_num}']['ping_result'])[0]
                if self.hdd_present:
                    ext_slot_out_result = result[f'device_num_{dev_num}']['hdd_check_result'][1]
                    ext_slot_in_result = result[f'device_num_{dev_num}']['hdd_check_result'][2]
                elif self.nmc_ports_count != 0:
                    ext_slot_out_result = result[f'device_num_{dev_num}']['nmc_check_result'][1]
                if ext_slot_out_result in ['Внешний HDD найден', 'Все порты NMC модуля найдены'] and \
                        flash_result == 'Flash накопители найдены' and \
                        ext_slot_in_result == 'Внутренний HDD найден' and \
                        losses == '0% packet loss':
                    write_new_note(f'Создание карточки изделия для устройства {dev_num}...\n')
                    Devices.create_device(serial_num_board)
                    write_new_note('\n>>>Карточка изделия создана!<<<\n')
                    Devices.update_diag(serial_num_board)
                    SerialNumBoard.set_visual_inspection(serial_num_board, valid=True)
                    History.new_note(serial_num_board, f'СТЕНД_ДИАГНОСТИКИ, плата закончиала работу без ошибок!')
                    write_new_note('\n>>>Диагностика успешно пройдена!<<<\n')
                    self.logger_script.info('Устройство закончило работу без ошибок!',
                                            extra={'sn': f'{serial_num_board}', 'stend': f'{self.stend}',
                                                   'place': f'{place}'})
                    Statistic.new_note(serial_num_board, 'Стенд диагностики')
                    return True
                else:
                    write_new_note('>>>Неуспех. ПО было установлено, но при проверке АП возникли ошибки<<<\n')
                    serial_num_board = self.board_serial_number_list[dev_num - 1]
                    if ext_slot_out_result in ['Внешний HDD не найден',
                                               'По крайней мере один порт NMC модуля не найден']:
                        error_code = '009'
                    elif flash_result == 'По крайней мере один flash накопитель не определился, возможно,' \
                                         ' USB порты неисправны':
                        error_code = '090'
                    elif losses == '100% packet loss':
                        error_code = '900'
                    elif ext_slot_out_result in ['Внешний HDD не найден',
                                                 'По крайней мере один порт NMC модуля не найден'] and flash_result ==\
                            'По крайней мере один flash накопитель не определился, возможно, USB порты неисправны':
                        error_code = '099'
                    elif ext_slot_out_result in ['Внешний HDD не найден',
                                                 'По крайней мере один порт NMC модуля не найден'] and losses == \
                            '100% packet loss':
                        error_code = '909'
                    elif flash_result == 'По крайней мере один flash накопитель не определился, возможно,' \
                                         ' USB порты неисправны' and losses == '100% packet loss':
                        error_code = '990'
                    elif ext_slot_out_result in ['Внешний HDD не найден',
                                                 'По крайней мере один порт NMC модуля не найден'] and flash_result ==\
                            'По крайней мере один flash накопитель не определился, возможно, USB порты неисправны'\
                            and losses == '100% packet loss':
                        error_code = '999'
                    SerialNumBoard.set_visual_inspection(serial_num_board, valid=True, error_code=error_code)
                    History.new_note(serial_num_board,
                                     f'СТЕНД_ДИАГНОСТИКИ, плата закончиала работу с ошибкой {error_code}!')
                    Repair.new_note(serial_num_board, error_code)
                    write_new_note(
                        f'Результат проверки слота расширения: {ext_slot_out_result}, {ext_slot_in_result}\n')
                    write_new_note(f'Результат проверки USB портов: {flash_result}\n')
                    write_new_note(f'Результат проверки Ethernet портов: {losses}\n')
                    self.logger_script.error(
                        f'Устройство закончило работу с ошибками АП: {ext_slot_out_result}, {ext_slot_in_result},'
                        f' {flash_result}, {losses}',
                        extra={'sn': f'{serial_num_board}', 'stend': f'{self.stend}', 'place': f'{place}'})
                    return False

        # запись сырых результатов в файл
        current_time = str(datetime.now())[:-7].replace(':', '-')
        with open(f'logs/PCI/raw_results/raw_results-{current_time}.yaml', 'w') as f:
            f.write(yaml.dump(result, allow_unicode=True))

        self.logger_stend.removeHandler(self.log_i_stend)
        self.logger_script.removeHandler(self.log_i_script)
        self.logger_debag_1.removeHandler(self.log_d_1)
        self.logger_debag_2.removeHandler(self.log_d_2)
        self.logger_debag_3.removeHandler(self.log_d_3)
        self.logger_debag_4.removeHandler(self.log_d_4)
        self.logger_debag_5.removeHandler(self.log_d_5)
        return True
