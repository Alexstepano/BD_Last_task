import psycopg2
import psycopg2.extras
from settings import DB_CONFIG
from pandas import DataFrame
import streamlit as st
from datetime import datetime
def get_clients():
    query = "SELECT user_id FROM users"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            clients=cur.fetchall()
            print(clients)
            return [cl['user_id'] for cl in clients]

def get_client_info(client_id):
    query ="""SELECT user_id, first_name, second_name, third_name, email, telephone, street, house_num, flat_num,actual_flag
	FROM public.users where user_id = %s"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query,(client_id,))
            return cur.fetchall()


def update_client_info(selected_client, updated_client_info):
    query ="""
        UPDATE users
        SET first_name = %(first_name)s,
            second_name = %(second_name)s,
            third_name = %(third_name)s,
            email = %(email)s,
            telephone = %(telephone)s,
            street = %(street)s,
            house_num = %(house_num)s,
            flat_num = %(flat_num)s,
            actual_flag = %(actual_flag)s
        WHERE user_id = %(user_id)s;
        select 'complite'
    """

    params = {
        'first_name': updated_client_info.get('first_name'),
        'second_name': updated_client_info.get('second_name'),
        'third_name': updated_client_info.get('third_name'),
        'email': updated_client_info.get('email'),
        'telephone': updated_client_info.get('telephone'),
        'street': updated_client_info.get('street'),
        'house_num': updated_client_info.get('house_num'),
        'flat_num': updated_client_info.get('flat_num'),
        'actual_flag':updated_client_info.get('actual_flag'),
        'user_id': selected_client
    }

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            result = cur.fetchall()
            print(result)

def get_couriers():
    query = "SELECT courier_id FROM couriers"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            clients=cur.fetchall()
            print(clients)
            return [cl['courier_id'] for cl in clients]

def get_courier_info(client_id):
    query ="""SELECT courier_id, first_name, second_name, third_name, email, telephone,actual_flag
	FROM public.couriers where courier_id = %s"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query,(client_id,))
            return cur.fetchall()

def update_courier_status(selected_courier, updated_client_info):
    query ="""
        UPDATE couriers
        SET first_name = %(first_name)s,
            second_name = %(second_name)s,
            third_name = %(third_name)s,
            email = %(email)s,
            telephone = %(telephone)s,
            actual_flag =%(actual_flag)s
        WHERE courier_id = %(user_id)s;
        select 'complite'
    """

    params = {
        'first_name': updated_client_info.get('first_name'),
        'second_name': updated_client_info.get('second_name'),
        'third_name': updated_client_info.get('third_name'),
        'email': updated_client_info.get('email'),
        'telephone': updated_client_info.get('telephone'),
        'actual_flag':updated_client_info.get('actual_flag'),
        'user_id': selected_courier
    }

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            result = cur.fetchall()
            print(result)


def get_orders():
    query = "SELECT order_id FROM public.orders"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            orders = cur.fetchall()
            return [order['order_id'] for order in orders]

def get_order_info(order_id):
    query = """
        SELECT order_id, courier_id, user_id, street, house_num, flat_num
        FROM public.orders
        WHERE order_id = %s
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (order_id,))
            return cur.fetchall()

def update_order_info(selected_order, updated_order_info):
    query = """
        UPDATE public.orders
        SET courier_id = %(courier_id)s,
            user_id = %(user_id)s,
            street = %(street)s,
            house_num = %(house_num)s,
            flat_num = %(flat_num)s
        WHERE order_id = %(order_id)s;
    """

    params = {
        'courier_id': updated_order_info.get('courier_id'),
        'user_id': updated_order_info.get('user_id'),
        'street': updated_order_info.get('street'),
        'house_num': updated_order_info.get('house_num'),
        'flat_num': updated_order_info.get('flat_num'),
        'order_id': selected_order
    }

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()  # Сохраняем изменения в базе данных
            return cur.rowcount 

def get_actual_status(order_id):
    query=""" with t3 as (select max(time) as time,order_id from orders_history group by order_id)
select status,time from orders_history join t3 using(order_id,time) where order_id=%s"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (order_id,))
            result = cur.fetchone()['status']
            return result

def set_new_status(order_id,status):
    query_update_order_status="""INSERT INTO public.orders_history(
	 order_id, status, "time")
	VALUES (%(order_id)s, %(status)s, NOW());"""
    if order_id:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                try:
                    # Начало транзакции
                    conn.autocommit = False

                    # Вставка записи об отмене заказа в таблицу Orders_History
                    
                    cur.execute( query_update_order_status, {'order_id':order_id,'status':status})

                    # Коммит транзакции
                    conn.commit()
                except Exception as e:
                    # Откат транзакции в случае ошибки
                    conn.rollback()
                    raise e
    else:
        st.error('У вас нет заказа для возможного изменения статуса')
    return order_id

def see_films_statistics():
    query="""with t as (select cassette_id from cassettes where cassette_status='Доступно' ) ,t1 as(select title_id,count(*) as cassete_count from cassette_titles where cassette_id not in (select * from t) group by title_id)
SELECT title_id, title_name, title_description, title_rating,COALESCE(cassete_count,0) as cassete_count
	FROM public.titles left join t1 using(title_id) order by title_id;"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query,)
            return DataFrame(cur.fetchall())





def add_new_title(titlename,desc,rat):

    query_1 = """
    select min(case when title_name = %s then 0
    else 1
    end) as booleaninclude from titles;
    """
    query_2="""INSERT INTO public.titles(
	 title_name, title_description, title_rating)
	VALUES ( %(nam)s, %(des)s, %(rat)s);
	select 'complite';"""
    if titlename  is not  None and desc is not None:
        with psycopg2.connect(**DB_CONFIG) as connection:
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute(query_1, (titlename,))
                result = cursor.fetchone()
                print(result)
                print("FFFF")

                if result is None or result[0] == 0 or result[0]== None:
                    st.error("Фильму уже есть")
                    print()
                    return False
                else:
                    cursor.execute(query_2, {
                        "nam": titlename,
                        "des": desc,
                        "rat": rat
                    })
                    result = cursor.fetchall()
                    print(result)
                    if result is None or result[0][0]!='complite':
                        print(['complite',result[0]])
                        st.error("Фильму уже есть")
                        return False
                    else:
                        st.success("Добавление удачно")
                        return True
    else:
        return True

def see_cassettes_statistics():
    query="""with t1 as (select cassette_id,count(title_id) over (partition by cassette_id) as film_count,title_id  from cassette_titles),
 t2 as (select cassette_id,film_count,title_id,title_name from t1 join titles using(title_id))
select cassette_id,cassette_status,film_count,title_id,title_name from t2 right join cassettes using(cassette_id) order by cassette_id"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query,)
            return DataFrame(cur.fetchall())


def get_cassete():
    query = "SELECT cassette_id FROM public.cassettes"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            orders = cur.fetchall()
            return [order['cassette_id'] for order in orders]


def add_new_cassette(status):
    query_update_cassete_status ="""INSERT INTO public.cassettes(
	 cassette_status)
	VALUES (%s);"""
    with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                try:
                    # Начало транзакции
                    conn.autocommit = False

                    # Вставка записи об отмене заказа в таблицу Orders_History
                    
                    cur.execute( query_update_cassete_status, (status,))

                    # Коммит транзакции
                    conn.commit()
                except Exception as e:
                    # Откат транзакции в случае ошибки
                    conn.rollback()
                    raise e
    return True


def get_cassettes():
    query = "SELECT cassette_id FROM cassettes"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            cassettes = cur.fetchall()
            print(cassettes)
            return [cass['cassette_id'] for cass in cassettes]

def get_cassette_info(cassette_id):
    query = """
        SELECT cassette_id, cassette_status
        FROM public.cassettes
        WHERE cassette_id = %s
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (cassette_id,))
            return cur.fetchall()

def update_cassette_info(selected_cassette, updated_cassette_info):
    query = """
        UPDATE cassettes
        SET cassette_status = %(cassette_status)s
        WHERE cassette_id = %(cassette_id)s;
        SELECT 'complete'
    """

    params = {
        'cassette_status': updated_cassette_info.get('cassette_status'),
        'cassette_id': selected_cassette
    }

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            result = cur.fetchall()
            print(result)
def get_film_list():
    query = "SELECT title_id FROM titles"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            clients=cur.fetchall()
            print(clients)
            return [cl['title_id'] for cl in clients]


def add_film_to_cassette(selected_cassette, selected_film):
    query="""INSERT INTO public.cassette_titles(
	 title_id, cassette_id)
	VALUES (%(title_id)s, %(order_id)s);"""
    if selected_cassette and selected_film:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                try:
                    # Начало транзакции
                    conn.autocommit = False

                    # Вставка записи об отмене заказа в таблицу Orders_History
                    
                    cur.execute( query, {'title_id':selected_film,'order_id':selected_cassette})

                    # Коммит транзакции
                    conn.commit()
                except Exception as e:
                    # Откат транзакции в случае ошибки
                    conn.rollback()
                    raise e
    else:
        st.error('У вас нет касеты для возможного добавления фильма')
    return True


#АНАЛИТИКА

def get_month_users():


    query="""with t1 as (SELECT  client_type, client_id, min("time") as time
            FROM public.client_password_history group by client_id,client_type order by client_id,client_type)

        SELECT
            DATE_TRUNC('month', time) AS month,
            COUNT(*) AS new_users
        FROM
            t1
        WHERE
            client_type = true
        GROUP BY
            month
        ORDER BY
            month;
        """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query,)
            return DataFrame(cur.fetchall())



def get_month_cur():


    query="""with t1 as (SELECT  client_type, client_id, min("time") as time
            FROM public.client_password_history group by client_id,client_type order by client_id,client_type)

        SELECT
            DATE_TRUNC('month', time) AS month,
            COUNT(*) AS new_users
        FROM
            t1
        WHERE
            client_type = false
        GROUP BY
            month
        ORDER BY
            month;
        """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query,)
            return DataFrame(cur.fetchall())



def get_popular_films_report():
    query="""select title_id,count(Distinct order_id) from order_titles group by title_id order by title_id
        """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query,)
            return DataFrame(cur.fetchall())

def get_avg_delivery_time_report():
    query="""with t1 as (select order_id from orders_history where status='Доставлено'),

t2 as (select max(time),min(time) from orders_history where order_id in (select * from t1) group by order_id)
select (avg(max-min)::varchar) from t2
     """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query,)
            return cur.fetchone()[0]
    
def get_order_statuses_report():
    query="""with t1 as (select max(time) as time,order_id from orders_history group by order_id)

select status, count(*) from orders_history join t1 using(order_id,time) group by status"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query,)
            return DataFrame(cur.fetchall())

def get_casstets_statuses_report():
    query="""select cassette_status, count(*) from  cassettes group by cassette_status"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query,)
            return DataFrame(cur.fetchall())



def get_back_up():
    time=datetime.now()
    queries = [
        """CREATE TABLE IF NOT EXISTS backup_table_users AS
        SELECT %s AS backup_timestamp ,*
        FROM users WHERE 1=0;
        INSERT INTO public.backup_table_users
        SELECT %s AS backup_timestamp ,*
        FROM users;""",

        """CREATE TABLE IF NOT EXISTS backup_table_couriers AS
        SELECT %s AS backup_timestamp ,*
        FROM couriers WHERE 1=0;
        INSERT INTO public.backup_table_couriers
        SELECT %s AS backup_timestamp ,*
        FROM couriers;""",

        """CREATE TABLE IF NOT EXISTS backup_table_admins AS
        SELECT %s AS backup_timestamp ,*
        FROM admins WHERE 1=0;
        INSERT INTO public.backup_table_admins
        SELECT %s AS backup_timestamp ,*
        FROM admins;""",

        """CREATE TABLE IF NOT EXISTS backup_table_cassette_titles AS
        SELECT %s AS backup_timestamp ,*
        FROM cassette_titles WHERE 1=0;
        INSERT INTO public.backup_table_cassette_titles
        SELECT %s AS backup_timestamp ,*
        FROM cassette_titles;""",

        """CREATE TABLE IF NOT EXISTS backup_table_cassettes AS
        SELECT %s AS backup_timestamp ,*
        FROM cassettes WHERE 1=0;
        INSERT INTO public.backup_table_cassettes
        SELECT %s AS backup_timestamp ,*
        FROM cassettes;""",

        """CREATE TABLE IF NOT EXISTS backup_table_client_password_history AS
        SELECT %s AS backup_timestamp ,*
        FROM client_password_history WHERE 1=0;
        INSERT INTO public.backup_table_client_password_history
        SELECT %s AS backup_timestamp ,*
        FROM client_password_history;""",

        """CREATE TABLE IF NOT EXISTS backup_table_order_titles AS
        SELECT %s AS backup_timestamp ,*
        FROM order_titles WHERE 1=0;
        INSERT INTO public.backup_table_order_titles
        SELECT %s AS backup_timestamp ,*
        FROM order_titles;""",

        """CREATE TABLE IF NOT EXISTS backup_table_orders AS
        SELECT %s AS backup_timestamp ,*
        FROM orders WHERE 1=0;
        INSERT INTO public.backup_table_orders
        SELECT %s AS backup_timestamp ,*
        FROM orders;""",

        """CREATE TABLE IF NOT EXISTS backup_table_titles AS
        SELECT %s AS backup_timestamp ,*
        FROM titles WHERE 1=0;
        INSERT INTO public.backup_table_titles
        SELECT %s AS backup_timestamp ,*
        FROM titles;""",

        """CREATE TABLE IF NOT EXISTS backup_table_orders_history AS
        SELECT %s AS backup_timestamp ,*
        FROM orders_history WHERE 1=0;
        INSERT INTO public.backup_table_orders_history
        SELECT %s AS backup_timestamp ,*
        FROM orders_history;"""
    ]

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for query in queries:
                cur.execute(query,(time,time))
            conn.commit()



def load_backup(backup_timestamp):
    queries = [
       """BEGIN;

-- Delete from tables that do not have foreign key dependencies first
DELETE FROM order_titles;
DELETE FROM orders_history;
DELETE FROM orders;


-- Delete from tables that do not have foreign key dependencies
DELETE FROM client_password_history;
DELETE FROM cassette_titles;
DELETE FROM titles;
DELETE FROM cassettes;
DELETE FROM admins;
DELETE FROM couriers;
DELETE FROM users;

-- Insert data from backup tables


INSERT INTO titles
SELECT  title_id, title_name, title_description, title_rating FROM backup_table_titles
WHERE backup_timestamp = %(t)s::timestamp;

INSERT INTO cassettes
SELECT cassette_id, cassette_status FROM backup_table_cassettes
WHERE backup_timestamp = %(t)s::timestamp;

INSERT INTO cassette_titles
SELECT id, title_id, cassette_id FROM backup_table_cassette_titles
WHERE backup_timestamp = %(t)s::timestamp;



INSERT INTO admins
SELECT admin_id, login, hashed_password FROM backup_table_admins
WHERE backup_timestamp = %(t)s::timestamp;

INSERT INTO couriers
SELECT courier_id, first_name, second_name, third_name, email, telephone, actual_flag FROM backup_table_couriers
WHERE backup_timestamp = %(t)s::timestamp;

INSERT INTO users
SELECT user_id, first_name, second_name, third_name, email, telephone, street, house_num, flat_num, actual_flag FROM backup_table_users
WHERE backup_timestamp = %(t)s::timestamp;

INSERT INTO orders
SELECT order_id, courier_id, user_id, street, house_num, flat_num FROM backup_table_orders
WHERE backup_timestamp = %(t)s::timestamp;

INSERT INTO orders_history
SELECT history_id, order_id, status, time FROM backup_table_orders_history
WHERE backup_timestamp = %(t)s::timestamp;

INSERT INTO order_titles
SELECT  id, title_id, order_id FROM backup_table_order_titles
WHERE backup_timestamp = %(t)s::timestamp;



INSERT INTO client_password_history
SELECT id, client_type, client_id, hashed_password, time FROM backup_table_client_password_history
WHERE backup_timestamp = %(t)s::timestamp;
COMMIT;"""
    ]

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for query in queries:
                cur.execute(query,{'t':backup_timestamp})
            conn.commit()

# Функция для получения доступных резервных копий
def get_available_backups():
    query = """
    SELECT DISTINCT backup_timestamp
    FROM backup_table_users"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            backups = cur.fetchall()
    return [backup[0] for backup in backups]