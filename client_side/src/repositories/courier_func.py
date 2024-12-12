import streamlit as st
from pandas import DataFrame
import psycopg2
from settings import DB_CONFIG
from datetime import date
import pandas as pd


def cur_orders():
    query="""with t1 as (select order_id from orders_history where status='Доставлено' or status='Отменен'),
 t2 as (select order_id from orders where courier_id=%s and order_id not in (select * from t1)),
 t3 as (select max(time) as time,order_id from orders_history group by order_id)
select order_id,status,time from orders_history join t3 using(order_id,time) where order_id in (select * from t2)"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (st.session_state.client_id,))
            return DataFrame(cur.fetchall())

def renew_order_status(order_id,status):
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


def cur_orders_list():
    query="""with t1 as (select order_id from orders_history where status='Доставлено' or status='Отменен'),
 t2 as (select order_id from orders where courier_id=%s and order_id not in (select * from t1)),
 t3 as (select max(time) as time,order_id from orders_history group by order_id)
select order_id,status,time from orders_history join t3 using(order_id,time) where order_id in (select * from t2)"""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (st.session_state.client_id,))
            orders = cur.fetchall()
            return[order[0] for order in  orders]