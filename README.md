ТЗ:

```
Приложение представляет собой базу управления книгами в библиотеке. Пользователь может добавить и удалять книгу.
У книг должны быть жанры.
Пользователь должен иметь возможность поиска книги по названию и/или автору. (поиск через один запрос)

Основная функциональность:

Добавление новой книги:
- Пользователь может добавить новую книгу указав название, автора, описание и жанр книги. Пользователю должны быть предложены жанры, которые ранее прописаны в базе данных. Так же пользователь может ввести свой жанр.

Просмотр списка книг:
- Приложение должно отображать список всех книг (название и автор).
- Пользователь может выбрать книгу из списка для просмотра подробной информации.
- Пользователь вывести книги с определенным жанром.

Поиск книги:
- Пользователь может ввести ключевое слово или фразу для поиска.
- Приложение должно отобразить список книг, содержащих данное ключевое слово в полях 'автор' и 'название книги'.

Удаление книги:
- Пользователь может выбрать книгу из списка и удалить её.
- Книга должна быть удалена из базы данных.
```

Для запуска приложения:

1. Установить зависимости
2. Запустить приложение

```bash
 pip install -r req.txt
 uvicorn main:app --reload
```

Для запуска тестов:  
```bash
pytest
```