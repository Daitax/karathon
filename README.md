Чтобы запустить тесты:
1. в файле settings.py включить переключатель IS_TESTING = True
2. в терминале выполнить ```docker exec -it python bash -c "cd karathon && python3 manage.py test apps"```
3. не забыть выключить IS_TESTING = False