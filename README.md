# Cервис терминологий

Независимый сервис терминологии, который хранит коды данных и их контекст. База данных справочников, с
кодами и значениями

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/iurinmikhail/medical_service.git
```


2. Создайте виртуальное окружение:
   
   ```bash
   python -m venv venv
   ```
3. Активируйте виртуальное окружение:
   
   ```bash
   .\venv\Scripts\activate
   ```

4. Установите зависимости:
   
   ```bash
   pip install -r requirements.txt
   ```

5. Перейдите в директорию проекта:
   
   ```bash
   cd medical_site
   ```
6. Создать файл миграции:
   
   ```bash
   python manage.py makemigrations
   ```

7. Примените миграции:
   
   ```bash
   python manage.py migrate
   ```

8. Запустите сервер:
   
   ```bash
   python manage.py runserver
   ```

## Проект доступен по адресу 
http://127.0.0.1:8000/

## Документация API 
http://127.0.0.1:8000/swagger/

## Тестирование

   ```bash
   python manage.py test
   ```
