# Bookmarks app 

## Приложение, которое позволяет вам управлять вашими сайтами и создавать закладки на самое интересное

### Для развертывания

Создайте свой .env файла для доступа к вашей базе данных с вашими данными. 

#### Структура файла

SECRET_KEY=
DATABASE_URL=
ALLOWED_HOSTS=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=

#### Запускаем Docker

Запустите Docker.
Из корневой директории соберите и запустите образ приложения:
docker-compose up или docker-compose up -d

Затем создайте базу данных с нужным вам именем и данными:

docker exec -it db psql -U <username> -d postgres -c "CREATE DATABASE your_db;"

Приложение запустится на локальном хосте. 

### Дополнительно

Регистрация юзера делается по email без подтверждения. 

Использована JWT-аутентификация.

Для создания закладок юзер должен быть авторизован (несмотря на отсутствие явно прописанных пермишнов он является частью записи данных!)

Парсинг данных с сайтов делается автоматически при вводе ссылки и записывается в соответствующие поля.