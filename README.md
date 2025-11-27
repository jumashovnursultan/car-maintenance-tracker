# Car Maintenance Tracker

Веб-приложение для учёта ремонтов автомобилей с напоминаниями о техническом обслуживании.

## Технологии

**Backend:**
- Python 3.11
- Django 5.2
- Django REST Framework
- SQLite

**Frontend:**
- HTML5
- JavaScript (Vanilla JS)
- Bootstrap 5
- Axios

## Функционал

- ✅ Регистрация и авторизация пользователей
- ✅ Управление списком автомобилей (добавление, удаление)
- ✅ Учёт ремонтных работ (тип, дата, стоимость, пробег)
- ✅ История обслуживания с фильтрацией
- ✅ Автоматические напоминания о необходимости ТО
- ✅ REST API для всех операций
- ✅ Админ-панель Django

## Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/jumashovnursultan/car-maintenance-tracker.git
cd car-maintenance-tracker
```

### 2. Создать виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Применить миграции
```bash
python manage.py migrate
```

### 5. Создать суперпользователя (для доступа в админку)
```bash
python manage.py createsuperuser
```

Введите:
- Username: admin
- Email: (можно пропустить)
- Password: admin123

### 6. Запустить сервер
```bash
python manage.py runserver
```

Приложение доступно по адресу: http://127.0.0.1:8000/

## Использование

### Для пользователей

1. **Регистрация:** http://127.0.0.1:8000/register/
2. **Вход:** http://127.0.0.1:8000/login/
3. **Добавление машины:** Мои машины → Добавить машину
4. **Добавление ремонта:** Ремонты → Добавить ремонт
5. **Просмотр уведомлений о ТО:** автоматически на странице "Мои машины"

### Для администраторов

Админ-панель: http://127.0.0.1:8000/admin/

Логин: admin / admin123

## API Endpoints

### Автомобили
- `GET /api/cars/` - список машин текущего пользователя
- `POST /api/cars/` - добавить машину
- `GET /api/cars/{id}/` - детали машины
- `PUT /api/cars/{id}/` - обновить машину
- `DELETE /api/cars/{id}/` - удалить машину
- `GET /api/cars/{id}/repairs/` - все ремонты машины

### Ремонты
- `GET /api/repairs/` - список ремонтов
- `POST /api/repairs/` - добавить ремонт
- `GET /api/repairs/{id}/` - детали ремонта
- `PUT /api/repairs/{id}/` - обновить ремонт
- `DELETE /api/repairs/{id}/` - удалить ремонт
- `GET /api/repairs/needs_maintenance/` - список ремонтов, требующих ТО

### Сервисы
- `GET /api/services/` - список сервисов
- `POST /api/services/` - добавить сервис

## Структура проекта
```
car-maintenance-tracker/
├── config/              # Настройки Django
│   ├── settings.py
│   └── urls.py
├── cars/                # Основное приложение
│   ├── models.py        # Модели (Car, Service, Repair)
│   ├── views.py         # API Views + Frontend views
│   ├── serializers.py   # DRF сериализаторы
│   ├── admin.py         # Настройки админки
│   └── urls.py          # URL маршруты
├── templates/           # HTML шаблоны
│   ├── base.html
│   └── cars/
│       ├── home.html
│       ├── cars_list.html
│       └── repairs_list.html
├── static/              # CSS, JS файлы
├── db.sqlite3           # База данных
├── manage.py
└── README.md
```

## Логика уведомлений о ТО

При добавлении ремонта автоматически рассчитывается дата следующего ТО:
- **По времени:** +6 месяцев от даты ремонта
- **По пробегу:** +10,000 км от текущего пробега

Уведомление показывается, если:
- Текущая дата >= дата следующего ТО, ИЛИ
- Текущий пробег >= пробег следующего ТО

## Автор

Nursultan Jumashov  
GitHub: [@jumashovnursultan](https://github.com/jumashovnursultan)

## Лицензия

MIT License