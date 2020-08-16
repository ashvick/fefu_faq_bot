### Используемые инструменты:
- Для взаимодействия с Telegram использовалась библиотека https://github.com/eternnoir/pyTelegramBotAPI 
- Для сравнения запроса пользователя с вопросом из списка типа "Вопрос-Ответ" использовалась pre-trained модель "distiluse-base-multilingual-cased" из репозитория 
https://github.com/UKPLab/sentence-transformers

### Установка
1. Установить виртуальное окружение:
```
python -m venv env
```
Активировать виртуальное окружение:
* Linux:
```
source ./env/bin/activate
```
* Windows:
```
.\env\Scripts\activate.bat
```
2. Затем в терминале:
```
pip3 install -r requirements.txt
```
3. Запуск бота:
```
  python main.py
```

### Использование

В data.csv содержится список вопросов. Чтобы бот понимал другие вопросы, нужно изменить этот файл и перезапустить бота (шаг 3 из раздела "Установка")

