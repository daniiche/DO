## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.

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
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
      - ./Data:/var/lib/postgresql/data
      - ./Backups:/var/lib/postgresql/backups
    ports:
      - "5432:5432"
```

### Задача 2

В БД из задачи 1:

создайте пользователя test-admin-user и БД test_db
в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
создайте пользователя test-simple-user
предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db
Таблица orders:

id (serial primary key)
наименование (string)
цена (integer)
Таблица clients:

id (serial primary key)
фамилия (string)
страна проживания (string, index)
заказ (foreign key orders)
Приведите:

итоговый список БД после выполнения пунктов выше,
описание таблиц (describe)
SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
список пользователей с правами над таблицами test_db

```
CREATE TABLE "orders" (
    "id" SERIAL PRIMARY KEY,
    "наименование" VARCHAR(128),
    "цена" INTEGER
);

CREATE TABLE "clients" (
    "id" SERIAL PRIMARY KEY,
    "фамилия" VARCHAR(128),
    "страна проживания" VARCHAR(128),
    "заказ" SERIAL,
    CONSTRAINT fk_orders
      FOREIGN KEY("заказ") 
	  REFERENCES orders(id)
);

CREATE INDEX country_idx ON "clients" ("страна проживания");

GRANT ALL PRIVILEGES ON DATABASE test_db TO "test-admin-user";

CREATE USER "test-simple-user";

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "test-simple-user";
```

```console
test_db=# \l
                                             List of databases
   Name    |      Owner      | Encoding |  Collate   |   Ctype    |            Access privileges            
-----------+-----------------+----------+------------+------------+-----------------------------------------
 postgres  | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | =c/"test-admin-user"                   +
           |                 |          |            |            | "test-admin-user"=CTc/"test-admin-user"
 template1 | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | =c/"test-admin-user"                   +
           |                 |          |            |            | "test-admin-user"=CTc/"test-admin-user"
 test_db   | test-admin-user | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/"test-admin-user"                  +
           |                 |          |            |            | "test-admin-user"=CTc/"test-admin-user"
```

```console
test_db-# \d+ public.*
                                                                Table "public.clients"
      Column       |          Type          | Collation | Nullable |                 Default                  | Storage  | Stats target | Description 
-------------------+------------------------+-----------+----------+------------------------------------------+----------+--------------+-------------
 id                | integer                |           | not null | nextval('clients_id_seq'::regclass)      | plain    |              | 
 фамилия           | character varying(128) |           |          |                                          | extended |              | 
 страна проживания | character varying(128) |           |          |                                          | extended |              | 
 заказ             | integer                |           | not null | nextval('"clients_заказ_seq"'::regclass) | plain    |              | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
    "country_idx" btree ("страна проживания")
Foreign-key constraints:
    "fk_orders" FOREIGN KEY ("заказ") REFERENCES orders(id)
Access method: heap

                   Sequence "public.clients_id_seq"
  Type   | Start | Minimum |  Maximum   | Increment | Cycles? | Cache 
---------+-------+---------+------------+-----------+---------+-------
 integer |     1 |       1 | 2147483647 |         1 | no      |     1
Owned by: public.clients.id

                  Index "public.clients_pkey"
 Column |  Type   | Key? | Definition | Storage | Stats target 
--------+---------+------+------------+---------+--------------
 id     | integer | yes  | id         | plain   | 
primary key, btree, for table "public.clients"

                 Sequence "public.clients_заказ_seq"
  Type   | Start | Minimum |  Maximum   | Increment | Cycles? | Cache 
---------+-------+---------+------------+-----------+---------+-------
 integer |     1 |       1 | 2147483647 |         1 | no      |     1
Owned by: public.clients."заказ"

                                    Index "public.country_idx"
      Column       |          Type          | Key? |     Definition      | Storage  | Stats target 
-------------------+------------------------+------+---------------------+----------+--------------
 страна проживания | character varying(128) | yes  | "страна проживания" | extended | 
btree, for table "public.clients"

                                                           Table "public.orders"
    Column    |          Type          | Collation | Nullable |              Default               | Storage  | Stats target | Description 
--------------+------------------------+-----------+----------+------------------------------------+----------+--------------+-------------
 id           | integer                |           | not null | nextval('orders_id_seq'::regclass) | plain    |              | 
 наименование | character varying(128) |           |          |                                    | extended |              | 
 цена         | integer                |           |          |                                    | plain    |              | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "fk_orders" FOREIGN KEY ("заказ") REFERENCES orders(id)
Access method: heap

                   Sequence "public.orders_id_seq"
  Type   | Start | Minimum |  Maximum   | Increment | Cycles? | Cache 
---------+-------+---------+------------+-----------+---------+-------
 integer |     1 |       1 | 2147483647 |         1 | no      |     1
Owned by: public.orders.id

                  Index "public.orders_pkey"
 Column |  Type   | Key? | Definition | Storage | Stats target 
--------+---------+------+------------+---------+--------------
 id     | integer | yes  | id         | plain   | 
primary key, btree, for table "public.orders"

```

```sql
SELECT * FROM information_schema.table_privileges where table_schema = 'public';
```

```console
test_db=# SELECT distinct grantee FROM information_schema.table_privileges where table_schema='public';
     grantee      
------------------
 test-admin-user
 test-simple-user
(2 rows)
```


## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

Наименование	цена
Шоколад	10
Принтер	3000
Книга	500
Монитор	7000
Гитара	4000
Таблица clients

ФИО	Страна проживания
Иванов Иван Иванович	USA
Петров Петр Петрович	Canada
Иоганн Себастьян Бах	Japan
Ронни Джеймс Дио	Russia
Ritchie Blackmore	Russia
Используя SQL синтаксис:

вычислите количество записей для каждой таблицы
приведите в ответе:
запросы
результаты их выполнения.

```sql
INSERT INTO orders("наименование","цена") VALUES
('Шоколад',10),
('Принтер',3000),
('Книга',500),
('Монитор',7000),
('Гитара',4000);

INSERT INTO clients("фамилия","страна проживания") VALUES
('Иванов Иван Иванович','USA'),
('Петров Петр Петрович','Canada'),
('Иоганн Себастьян Бах','Japan'),
('Ронни Джеймс Дио','Russia'),
('Ritchie Blackmore','Russia');

SELECT COUNT(*) FROM orders
union all
SELECT COUNT(*) FROM clients;

```

```
count
5
5
```

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

ФИО	Заказ
Иванов Иван Иванович	Книга
Петров Петр Петрович	Монитор
Иоганн Себастьян Бах	Гитара
Приведите SQL-запросы для выполнения данных операций.

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.

Подсказк - используйте директиву UPDATE.

```sql
delete from clients c
where c.фамилия in ('Ронни Джеймс Дио','Ritchie Blackmore');

update orders
set наименование='гитара'
where id = (select заказ from clients where фамилия='Иоганн Себастьян Бах');

update orders
set наименование='монитор'
where id = (select заказ from clients where фамилия='Петров Петр Петрович');

update orders
set наименование='книга'
where id = (select заказ from clients where фамилия='Иванов Иван Иванович');

select "фамилия" as ФИО,"наименование" as заказ
from clients
inner join orders o
on clients.заказ = o.id;
```

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 (используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.

```
EXPLAIN ANALYSE SELECT COUNT(*) FROM clients;

Aggregate  (cost=11.62..11.63 rows=1 width=8) (actual time=0.026..0.027 rows=1 loops=1)
  ->  Seq Scan on clients  (cost=0.00..11.30 rows=130 width=0) (actual time=0.007..0.008 rows=5 loops=1)
Planning Time: 0.052 ms
Execution Time: 0.054 ms

Здесь в виде древовидной структуре представленны выполняющиеся операции.
В корневом уровне есть функция агрегации подсчета, выдающая одну строку и занимающая около 0.025 мс
Для ее реализации нужно внутри нее проводить последовательный перебор значений, занимающий 0.007 мс.
Сost - это число условных единиц сложности которые потребуются движку для начала операции.
Rows - это предположительное число строк, которые будут возвращены
Width - это примерный размер в байтах возвращенных строк

```

## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.


Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления.

```console
docker exec -i postgres_docker_postgres_1 /bin/bash -c "POSTGRES_PASSWORD=admin pg_dump --username test-admin-user test_db > /var/lib/postgresql/backups/dump.sql"

docker exec -i postgres_docker_postgres_1 /bin/bash -c "POSTGRES_PASSWORD=admin psql -U test-admin-user -d test_db -c 'drop database test_db'"

docker exec -i postgres_docker_postgres_1 /bin/bash -c "POSTGRES_PASSWORD=admin psql -U test-admin-user -d postgres -c 'create database test_db'"

docker exec -i postgres_docker_postgres_1 /bin/bash -c "POSTGRES_PASSWORD=admin psql --username test-admin-user test_db < /var/lib/postgresql/backups/dump.sql"

```

