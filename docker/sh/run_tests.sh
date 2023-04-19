#!/bin/bash

printf "\033[46mВыполнение тестов запущено\033[0m\n"

if docker exec -it python bash -c "cd karathon && python3 manage.py test apps"

then
printf "\033[32mВыполнение тестов успешно завершено\033[0m\n"

else
printf "\033[31mТесты не выполнены. Исправьте ошибки.\033[0m\n"

fi