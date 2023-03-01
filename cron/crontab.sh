#!/bin/bash

#  создание файла для логов, если его не существует
touch /logs/crontab.log

# обеспечение прав на выполнение файла
chmod a+x /src/collect.py

# добавление правила периодического задания для cron
# * * * * * – выполнение задания один раз в каждую минуту
echo "* * * * * /usr/local/bin/python /src/collect.py >> /logs/crontab.log 2>&1" > /etc/crontab

# сохранение текущих значений переменных окружения в файле для cron
printenv >> /etc/environment

# регистрация созданного правила
crontab /etc/crontab

# запуск cron
/usr/sbin/service cron start

# вывод логов
tail -f /logs/crontab.log