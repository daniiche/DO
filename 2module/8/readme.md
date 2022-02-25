## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя psql.

Воспользуйтесь командой \? для вывода подсказки по имеющимся в psql управляющим командам.

Найдите и приведите управляющие команды для:

вывода списка БД
подключения к БД
вывода списка таблиц
вывода описания содержимого таблиц
выхода из psql

```
version: '3'
services:
  postgres:
    image: postgres:13.0
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test-admin-user
      POSTGRES_PASSWORD: admin
      PGDATA: "/var/lib/postgresql/data/pgdata"
    volumes:
      - ./Data:/var/lib/postgresql/data
      - ./Backups:/var/lib/postgresql/backups
    ports:
      - "5432:5432"
```

```
DanBookDair:~ danche$ psql -h 130.162.41.72 -U test-admin-user -d test_db
Password for user test-admin-user: 
psql (14.0, server 13.0 (Debian 13.0-1.pgdg100+1))
Type "help" for help.

test_db=# 
```

```
\l
\conninfo
\db
\dt[S+]
\d[S+]  NAME
\q
```

## Задача 2

Используя psql создайте БД test_database.

Изучите бэкап БД.

Восстановите бэкап БД в test_database.

Перейдите в управляющую консоль psql внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

Используя таблицу pg_stats, найдите столбец таблицы orders с наибольшим средним значением размера элементов в байтах.

Приведите в ответе команду, которую вы использовали для вычисления и полученный результат.

```
docker exec -i postgres_docker_postgres_1 /bin/bash -c "POSTGRES_PASSWORD=admin psql --username test-admin-user test_db < /var/lib/postgresql/backups/dump.sql"
```

```
test_db=# select tablename,attname, avg_width from pg_stats where tablename ='orders' order by avg_width desc limit 5;
 tablename | attname | avg_width 
-----------+---------+-----------
 orders    | title   |        16
 orders    | id      |         4
 orders    | price   |         4
```



## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и поиск по ней занимает долгое время. 
Вам, как успешному выпускнику курсов DevOps в нетологии предложили провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

```
CREATE TABLE orders_1 (CHECK (price >499)) INHERITS (orders);
INSERT INTO orders_1 SELECT * from orders where price >499;
CREATE TABLE orders_2 (CHECK (price <=499)) INHERITS (orders);
INSERT INTO orders_1 SELECT * from orders where price <=499;
```

```
да, сразу задав правила партиционирования для таблицы
```

## Задача 4

Используя утилиту pg_dump создайте бекап БД test_database.

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца title для таблиц test_database?

```
docker exec -i postgres_docker_postgres_1 /bin/bash -c "POSTGRES_PASSWORD=admin psql --username test-admin-user test_db > /var/lib/postgresql/backups/dump.sql"
```

```
CREATE TABLE public.orders (
    id integer NOT NULL,
    title character varying(80) UNIQUE NOT NULL,
    price integer DEFAULT 0
);

OR

CREATE TABLE public.orders (
    id integer NOT NULL,
    title character varying(80) PRIMARY KEY,
    price integer DEFAULT 0
);
```
