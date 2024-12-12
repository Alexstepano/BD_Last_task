import streamlit as st
from pandas import DataFrame
import psycopg2
from settings import DB_CONFIG
from datetime import date
import pandas as pd

def get_orders_statistics() -> DataFrame:
    query = """with
 t2 as (select order_id  from orders where user_id=%(user_id)s ),

t3 as (select order_id,title_id from t2 left join order_titles using(order_id)),
t1 as (select *,COUNT(title_id) OVER (PARTITION BY order_id, title_id)  AS title_count from t3 left join titles using(title_id)),
t as (select order_id,max(time) over (partition by order_id) as time  from orders_history ),
t4 as (select order_id,status,time,title_name,title_description,title_rating,title_count from t1 left join orders_history using(order_id))
select Distinct order_id,status,time,title_name,title_description,title_rating,title_count from t4 join t using(order_id,time)"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, {"user_id": st.session_state.client_id})
            return DataFrame(cur.fetchall())

def get_titles_list():
    query = "SELECT title_name FROM titles"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            title_list = cur.fetchall()
    return [title[0] for title in title_list]

def get_cassette_count(title_name):
    query = """
    with t1 as (select cassette_id from cassettes where cassette_status='Доступно' )
SELECT count(*)
    FROM Cassette_Titles as ct
    JOIN Titles as t ON ct.title_id = t.title_id
    WHERE t.title_name = %s and cassette_id in (select * from t1)
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (title_name,))
            count = cur.fetchone()[0]
    return count

def get_title_description(title_name):
    query = "SELECT title_description FROM titles WHERE title_name = %s"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (title_name,))
            description = cur.fetchone()[0]
    return description

def get_title_id(title_name):
    query = "SELECT title_id FROM titles WHERE title_name = %s"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (title_name,))
            title_id = cur.fetchone()[0]
    return title_id

def add_title_event(title_name):
    new_row = pd.DataFrame(
        {
            "Название фильма": [title_name],
            "title_id": [get_title_id(title_name)],
        }
    )
    st.session_state.order_table = pd.concat(
        [st.session_state.order_table, new_row], ignore_index=True
    )

def clear_table_event():
    st.session_state.order_table = pd.DataFrame(
        columns=["Название фильма", "title_id"]
    )

def create_order(street, house_num, flat_num, title_ids):
    user_id = st.session_state.client_id
    query="select street, house_num, flat_num from users where user_id=%(user_id)s;"
    query_insert_order = """
    insert into orders(courier_id, user_id, street, house_num, flat_num) VALUES 
(null,%(user_id)s, %(street)s, %(house_num)s, %(flat_num)s) RETURNING order_id;
    """
    query_insert_order_titles = """
    INSERT INTO Order_Titles (title_id, order_id)
    VALUES (%(title_id)s,%(order_id)s)
    """
    query_insert_order_history = """
    insert into Orders_History (order_id, status, time) VALUES 
 (%(order_id)s, 'Принят', NOW())
    """
    
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            try:
                # Начало транзакции
                conn.autocommit = False
                cur.execute(query,{'user_id': user_id})
                user_address=cur.fetchone()

                if not street or  house_num == 0 or  flat_num == 0:
                    db_street, db_house_num, db_flat_num = user_address
                    final_street = db_street
                    final_house_num = db_house_num
                    final_flat_num = db_flat_num
                else:
                    final_street = street
                    final_house_num = house_num
                    final_flat_num = flat_num
                
                # Вставка нового заказа
                cur.execute(query_insert_order, {'user_id': user_id, 'street': final_street, 'house_num': final_house_num, 'flat_num': final_flat_num})
                order_id = cur.fetchone()[0]

                # Вставка связей между заказом и фильмами
                for title_id in title_ids:
                    cur.execute(query_insert_order_titles, {'title_id': title_id, 'order_id': order_id})

                # Вставка записей в таблицу Orders_History
                
                cur.execute(query_insert_order_history, {'order_id': order_id })

                # Коммит транзакции
                conn.commit()
            except Exception as e:
                # Откат транзакции в случае ошибки
                conn.rollback()
                raise e
    return order_id

def see_not_delivered():
    query="""with t1 as (select order_id from orders where user_id=%s),
 t2 as (select order_id from orders_history where status='Доставлено' or status='Отменен')
select Distinct order_id from orders_history where order_id  not in (select * from t2) and order_id in (select * from t1)"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (st.session_state.client_id,))
            orders = cur.fetchall()
    return [order[0] for order in  orders]


def cancel_order(order_id):
    query_update_order_history = """
    INSERT INTO Orders_History (order_id, status, time)
    VALUES (%s, 'Отменен', NOW());
    """

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            try:
                # Начало транзакции
                conn.autocommit = False

                # Вставка записи об отмене заказа в таблицу Orders_History
                
                cur.execute(query_update_order_history, (order_id,))

                # Коммит транзакции
                conn.commit()
            except Exception as e:
                # Откат транзакции в случае ошибки
                conn.rollback()
                raise e

    return order_id