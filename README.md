# Это тестовое задание для Татнефть
Проект представляет собой апи на DRF

## Как запустить проект?

Создать .env файл и добавить переменные окружение

```bash

cat > .env <<EOF
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=securepassword123
DB_NAME=metric_db
POSTGRES_USER=super
POSTGRES_PASSWORD =pass
DB_HOST=db
DB_PORT=5432
REDIS_URL=redis://redis:6379/1
POSTGRES_DB=metric_db
EOF
```

Выполнить build через docker-compose 

```bash
docker-compose up -d
```

Админка будет доступна по адрес: http://localhost/admin
Api будет достпна по адрес: http://localhost/api

Данные для входа в админку
Имя пользователя: admin
Пароль: securepassword123