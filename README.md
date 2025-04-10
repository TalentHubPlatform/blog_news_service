## Деплой
1. `sudo docker-compose -f docker-compose.yml up --build`

## Запуск тестов
`sudo docker compose run --rm user_and_teams_service pytest tests/testfile.py -v -s`

Сами тесты находятся в директории tests