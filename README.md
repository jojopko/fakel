# Описание

Бот для отправки постов из ВК в телеграм.

# Установка

1. Клонируем репозиторий
2. Собираем докер-образ `make build`
3. Создаем `.env` файл: `cp .env.example .env` и устанавливаем нужные значения переменных (см. ниже)
4. Запускаем `make deploy` или `docker compose up -d`
5. Теперь он открыт на порту 8000 (можно изменить в `docker-compose.yml`)
6. Желательно сервис вынести в отдельный эндпоинт или subdomain. Вот так это делается через Nginx:

```
server {
    # ...

    # Обрати внимание! http://localhost:8000/ должен быть с закрывающим слешем!
    location /fakel_bot {
            proxy_pass http://localhost:8000/;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
            proxy_redirect off;
    }

    # ...
}
```

Проверить установку можно через curl: `curl http://example.com/fakel_bot`. Если все хорошо, поприветсвует тебя.

## Переменные

- `ACCESS_TOKEN` - ключ доступа с правами на стену и управление группой (только получить ключ при подтверждении сервера)
- `APP_SECRET` - любая секретная строка
- `VK_GROUP_ID` - ID группы ВК
- `TG_CHANNEL_NAME` - ID или название группы без '@', также там должен быть добавлен бот с правами на отправку сообщений
- `TG_BOT_TOKEN` - Токен бота в телеграме, получить у [BotFather](https://t.me/BotFather)
- `TELEGRAM_SEND_BLOCK` - Блокировка отправки сообщений (нужно для разработки, оставить `False`)
- `DEBUG_MODE` - Режим разработчика, больше логов и др. Можно оставить `True`, но возможно будет медленее работать
- `BOT_ADMIN_TELEGRAM_IDS` - ID пользователей, которые имеют админские привелегии через запяткую слитно.
