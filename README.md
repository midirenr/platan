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
