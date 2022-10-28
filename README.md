# Web

1. Разработка СПО для производства Сервисных и Граничных маршрутизаторов. 
2. Каждый разработчик работает со своей веткой.
3. Изменения в git вносим каждый день (в свою ветку).
4. В main вносим существенные изменения минимум раз в неделю.

Отвественные - 

fronend - Максим Мукоедов

backend - Никита Таракановский

скрипты (DUT) - Сергей Рубцов

*** В readme описываем внесенные изменения (существенные). ***

# Процесс установки и запуска

Установка проходит путем клонирования проекта из репозитория:
- открываем CMD;
- переходим в папку, в которую хотим сохранить проект командой: cd "yourfolder";
- выполняем команду: git clone https://git.istok.ad/devel-platan/web.git;
- выполняем команду: git chekout dev;
- выполняем команду: git pull;
- переходим в корневую папку проекта командой: cd web/web-platan .

Запуск осуществляется через файл manage.py, который автоматический генерируется фреймворком Django:
- для запуска проекта на локальном сервере выполняем команду: python manage.py runserver (проект запустится на localhost с портом 8000)

# Changelog v0.0.1

Frontend:
- Перенес весь Frontend, за исключением AJAX.

Backend:
- Полностью перенесена база данных под управление ORM Django, миграции выполнены, ошибок нет,
- Разработаны формы, за исключением валидации,
- Частично разработаны функции-представления,
- Составлены пути (urls).

Общее:
- Настроен файл конфигурации,
- Настроена файловая структура проекта(см. doc).

# Changelog v0.1.0

Frontend:
- Добавлено автообновление полей вывода на стендах ПСИ и диагностики AJAX

Backend:
- Добавлена авторизация
- Созданны группы пользователей
- Добавлена валидация форм ко всем стендам
- Добавлены все модели в админку
- Добавлена логика работы функций-представлений:
    1) Генерация серийных номеров
    2) История девайса
    3) Статистика

# Changelog v0.1.1
Backend:
- Реализована логика работы стенда диагностики
- Реализована логика работы стенда сборки
- Реализована логика работы стенда ПСИ
- Для пользователя-администратора добавлена ссылка в меню а админ-панель
- Сгенерированные стикеры в процессе работы стенда упаковки теперь открываются в новых вкладках
