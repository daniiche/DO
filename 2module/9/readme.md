## Задача 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.

Изучите бэкап БД и восстановитесь из него.

Перейдите в управляющую консоль mysql внутри контейнера.

Используя команду \h получите список управляющих команд.

Найдите команду для выдачи статуса БД и приведите в ответе из ее вывода версию сервера БД.

Подключитесь к восстановленной БД и получите список таблиц из этой БД.

Приведите в ответе количество записей с price > 300.

В следующих заданиях мы будем продолжать работу с данным контейнером.

```
docker-compose up -d

docker-compose exec mysql /bin/bash

mysql -u tuser -ptpass tdb < /var/lib/backup/init.sql

mysql -u tuser -ptpass

status

Server version:		8.0.28 MySQL Community Server - GPL

use tdb;

select * from orders where price > 300;
```

## Задача 2

Создайте пользователя test в БД c паролем test-pass, используя:

плагин авторизации mysql_native_password
срок истечения пароля - 180 дней
количество попыток авторизации - 3
максимальное количество запросов в час - 100
аттрибуты пользователя:
Фамилия "Pretty"
Имя "James"
Предоставьте привелегии пользователю test на операции SELECT базы test_db.

Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю test и приведите в ответе к задаче.

```
CREATE USER 'test'@'localhost'
  IDENTIFIED WITH caching_sha2_password BY 'test-pass'
  REQUIRE X509 WITH MAX_QUERIES_PER_HOUR 100
  PASSWORD EXPIRE INTERVAL 180 DAY
  FAILED_LOGIN_ATTEMPTS 3
  ATTRIBUTE '{"name": "James", "surname": "Pretty"}';
  
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

GRANT SELECT ON dbt.* TO 'test'@'localhost';

select * from INFORMATION_SCHEMA.USER_ATTRIBUTES where user='test';
+------+-----------+----------------------------------------+
| USER | HOST      | ATTRIBUTE                              |
+------+-----------+----------------------------------------+
| test | localhost | {"name": "James", "surname": "Pretty"} |
+------+-----------+----------------------------------------+
1 row in set (0.00 sec)
```

## Задача 3

Установите профилирование SET profiling = 1. Изучите вывод профилирования команд SHOW PROFILES;.

Исследуйте, какой engine используется в таблице БД test_db и приведите в ответе.

Измените engine и приведите время выполнения и запрос на изменения из профайлера в ответе:

на MyISAM
на InnoDB

```
mysql> SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES where TABLE_SCHEMA = 'tdb';
+------------+--------+
| TABLE_NAME | ENGINE |
+------------+--------+
| orders     | InnoDB |
+------------+--------+
1 row in set (0.01 sec)

ALTER TABLE orders ENGINE = MyISAM;
ALTER TABLE orders ENGINE = InnoDB;

mysql> SHOW PROFILES;
+----------+------------+-------------------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                               |
+----------+------------+-------------------------------------------------------------------------------------+
|        1 | 0.00725350 | SELECT @@profiling                                                                  |
|        2 | 0.00007425 | DROP TABLE IF EXISTS t1                                                             |
|        3 | 0.00014650 | SELECT DATABASE()                                                                   |
|        4 | 0.00095350 | show databases                                                                      |
|        5 | 0.00105825 | show tables                                                                         |
|        6 | 0.00276400 | show engines                                                                        |
|        7 | 0.00116450 | SELECT TABLE_NAME, ENGINE FROM information_schema.TABLES where TABLE_SCHEMA = 'tdb' |
|        8 | 0.03131100 | ALTER TABLE orders ENGINE = MyISAM                                                  |
|        9 | 0.04312425 | ALTER TABLE orders ENGINE = InnoDB                                                  |
+----------+------------+-------------------------------------------------------------------------------------+
9 rows in set, 1 warning (0.00 sec)
```

## Задача 4

Изучите файл my.cnf в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):

Скорость IO важнее сохранности данных
Нужна компрессия таблиц для экономии места на диске
Размер буффера с незакомиченными транзакциями 1 Мб
Буффер кеширования 30% от ОЗУ
Размер файла логов операций 100 Мб
Приведите в ответе измененный файл my.cnf.

```
root@87142a190185:/etc/mysql# grep MemTotal /proc/meminfo 
MemTotal:         990392 kB

[mysqld]
pid-file        = /var/run/mysqld/mysqld.pid
socket          = /var/run/mysqld/mysqld.sock
datadir         = /var/lib/mysql
secure-file-priv= NULL

# Custom config should go here
!includedir /etc/mysql/conf.d/

innodb_log_file_size=256M
innodb_file_per_table = 1
innodb_log_buffer_size=1M
innodb_buffer_pool_size=330M
innodb_log_file_size=100M
```
