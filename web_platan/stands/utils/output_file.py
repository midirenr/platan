def write_new_note (message: str):
    output_file = open('/home/nikita/Рабочий стол/web/web_platan/stands/templates/ajax/diagnostic_output.html', 'a', encoding='utf-8')
    output_file.write(message)
    output_file.flush()
    output_file.close()


def clear_file():
    output_file = open('/home/nikita/Рабочий стол/web/web_platan/stands/templates/ajax/diagnostic_output.html', 'w', encoding='utf-8')
    output_file.close()


def write_new_note_pci (message: str):
    output_file = open('/home/nikita/Рабочий стол/web/web_platan/stands/templates/ajax/pci_output.html', 'a', encoding='utf-8')
    output_file.write(message)
    output_file.flush()
    output_file.close()


def clear_file_pci():
    output_file = open('/home/nikita/Рабочий стол/web/web_platan/stands/templates/ajax/pci_output.html', 'w', encoding='utf-8')
    output_file.close()


def set_time(time):
    output_file = open('/home/nikita/Рабочий стол/web/web_platan/stands/templates/ajax/diagnostic_output.html',
                       'r', encoding='utf-8')
    lines = output_file.readlines()
    lines = lines[:-1]
    lines.append(time)
    output_file.close()

    output_file = open('/home/nikita/Рабочий стол/web/web_platan/stands/templates/ajax/diagnostic_output.html',
                       'w', encoding='utf-8')
    for line in lines:
        output_file.write(line)
    output_file.close()