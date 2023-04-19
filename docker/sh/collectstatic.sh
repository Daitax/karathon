#!/bin/bash

printf "\033[46mСобираем статику\033[0m\n"

if docker exec -it python bash -c "cd karathon && python manage.py collectstatic -l"

then
printf "\033[32mСтатика собрана\033[0m\n"

else
printf "\033[31mСтатика не собрана. Исправьте ошибки.\033[0m\n"

fi