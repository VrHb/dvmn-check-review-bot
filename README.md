# Получаем уведомления о проверке работ Devman.org с помощью бота 

С помощью API dvmn получаем уведомления о проверке работ на [devman.org](https://dvmn.org/)

## Как установить

### C помощью docker:

1. Скачать образ python:
```bash
docker pull python:3.10
```
2. Упаковать контейнер:
```bash
docker build -t dvmn-lesson-checker . 
```
3. Запустить контейнер:
```bash
docker run -d -t dvmn-lesson_checker
```
4. Проверить что контейнер запустился:
```bash
docker ps
```

### Обычным путем:

* Необходимо установить интерпретатор python версии 3.10
* Cкопировать содержимое проекта к себе в рабочую директорию
* Активировать внутри рабочей директории виртуальное окружение:

```
python -m venv [название окружения]
```

* Установить зависимости(необходимые библиотеки):

```
pip install -r requirements.txt
```

### Настройка переменных окружения:

* Для хранения переменных окружения создаем файл .env:
```
touch .env
```

#### Для работы будут необходимы три переменные:
1. Токен API devman, получаем по [ссылке](https://dvmn.org/api/docs/)
```
echo "DVNM_TOKEN"=<токен API devman>" >> .env 
```
2. Токен бота, получаем после регистрации [бота](https://habr.com/ru/post/262247/) 
```
echo "TG_TOKEN"=<токен бота>" >> .env 
```
3. ID вашего чата, можно получить в коде с помощью `print(bot.get_me())`
```
echo "TG_CHAT_ID"=<ID телеграм чата>" >> .env 
```

### Как пользоваться:

Запускаем файл:
```
python main.py
```
