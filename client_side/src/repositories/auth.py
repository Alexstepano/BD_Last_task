from pandas import DataFrame
import psycopg2
from settings import DB_CONFIG
from datetime import date
import pandas as pd
import hashlib
import streamlit as st
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_auth(tel, email, non_hased_password):
    password=hash_password(non_hased_password)
    query = """
    WITH t1 AS (
        SELECT user_id
        FROM users
        WHERE telephone = %(tel)s AND email = %(email)s AND actual_flag = true
    ),
    max_times AS (
        SELECT client_id, MAX(time) AS max_time
        FROM client_password_history
        WHERE client_type = true
        GROUP BY client_id
    )
    SELECT
        MAX(
            CASE
                WHEN cph.hashed_password = %(password)s
                THEN 1
                ELSE 0
            END
        ) AS answer
    FROM client_password_history AS cph
    JOIN t1 ON cph.client_id = t1.user_id
    JOIN max_times ON cph.client_id = max_times.client_id AND cph.time = max_times.max_time
    WHERE client_type = true
    """
    query_2 = """SELECT user_id
        FROM users
        WHERE telephone = %(tel)s AND email = %(email)s AND actual_flag = true"""
    with psycopg2.connect(**DB_CONFIG) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(query, {"tel": tel, "email": email, "password": password})
            result = cursor.fetchone()
            print(result)

            if result is None or result[0] == 0 or result[0]== None:
                return (False,"")
            else:
                cursor.execute(query_2, {"tel": tel, "email": email})
                result = cursor.fetchone()
                print(result)
                return (True,result[0])


def get_courier_auth(tel, email, non_hased_password):
    password=hash_password(non_hased_password)
    query = """
    WITH t1 AS (
        SELECT courier_id
        FROM couriers
        WHERE telephone = %(tel)s AND email = %(email)s AND actual_flag = True
    ),
    max_times AS (
        SELECT client_id, MAX(time) AS max_time
        FROM client_password_history
        WHERE client_type = false
        GROUP BY client_id
    )
    SELECT
        MAX(
            CASE
                WHEN cph.hashed_password = %(password)s
                THEN 1
                ELSE 0
            END
        ) AS answer
    FROM client_password_history AS cph
    JOIN t1 ON cph.client_id = t1.courier_id
    JOIN max_times ON cph.client_id = max_times.client_id AND cph.time = max_times.max_time
    WHERE client_type = false
    """
    query_2="""SELECT courier_id
        FROM couriers
        WHERE telephone = %(tel)s AND email = %(email)s AND actual_flag = True"""
    with psycopg2.connect(**DB_CONFIG) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(query, {"tel": tel, "email": email, "password": password})
            result = cursor.fetchone()
            print(result)

            if result is None or result[0] == 0 or result[0]== None:
                return (False,"")
            else:
                cursor.execute(query_2, {"tel": tel, "email": email})
                result = cursor.fetchone()
                print(1)
                print(result)
                return (True,result[0])


def user_reg_pages(first_name, second_name, third_name, email, tel, street, house_num, flat_num,non_hased_password):
    password=hash_password(non_hased_password)
    query_1 = """
    select min(case when telephone = %(tel)s or  %(email)s = email then 0
    else 1
    end) as booleaninclude from users;
    """
    query_2="""INSERT INTO users(
	 first_name, second_name, third_name, email, telephone, street, house_num, flat_num,actual_flag)
	VALUES ( %(first_name)s, %(second_name)s, %(third_name)s, %(email)s, %(tel)s, %(street)s, %(house_num)s,%(flat_num)s,TRUE);
     with t1 as(select user_id from users where telephone=%(tel)s and email =%(email)s)

    INSERT INTO public.client_password_history(
	 client_type, client_id, hashed_password, time)
	VALUES ( true, (select user_id from t1), %(password)s, NOW());
	select 'complite';"""

    with psycopg2.connect(**DB_CONFIG) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(query_1, {"tel": tel, "email": email})
            result = cursor.fetchone()
            print(result)

            if result is None or result[0] == 0 or result[0]== None:
                return False
            else:
                cursor.execute(query_2, {
                    "first_name": first_name,
                    "second_name": second_name,
                    "third_name": third_name,
                    "email": email,
                    "tel": tel,
                    "street": street,
                    "house_num": house_num,
                    "flat_num": flat_num,
                    "password": password
                })
                result = cursor.fetchall()
                print(result)
                if result is None or result[0][0]!='complite':
                    print(['complite',result[0]])
                    return False
                else:
                    return True


def courier_reg_pages(first_name, second_name, third_name, email, tel,non_hased_password):
    password=hash_password(non_hased_password)
    query_1 = """
    select min(case when telephone = %(tel)s or  %(email)s = email then 0
    else 1
    end) as booleaninclude from couriers;
    """
    query_2="""INSERT INTO couriers(
	 first_name, second_name, third_name, email, telephone,actual_flag)
	VALUES ( %(first_name)s, %(second_name)s, %(third_name)s, %(email)s, %(tel)s,TRUE);
     with t1 as(select courier_id from couriers where telephone=%(tel)s and email =%(email)s)

    INSERT INTO public.client_password_history(
	 client_type, client_id, hashed_password, time)
	VALUES ( false, (select courier_id from t1), %(password)s, NOW());
	select 'complite';"""

    with psycopg2.connect(**DB_CONFIG) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(query_1, {"tel": tel, "email": email})
            result = cursor.fetchone()
            print(result)

            if result is None or result[0] == 0 or result[0]== None:
                return False
            else:
                cursor.execute(query_2, {
                    "first_name": first_name,
                    "second_name": second_name,
                    "third_name": third_name,
                    "email": email,
                    "tel": tel,
                    "password": password
                })
                result = cursor.fetchall()
                print(result)
                if result is None or result[0][0]!='complite':
                    print(['complite',result[0][0]])
                    return False
                else:
                    return True
    
def deleting_user_update():
    user_id = st.session_state.client_id
    q_1="""with t1 as (select order_id from orders_history where status='Доставлено' or status='Отменен')
select count(order_id) from orders where user_id=%(user_id)s and order_id not in (select * from t1);"""
    query = """
        UPDATE users
        SET actual_flag = False
        WHERE user_id = %(user_id)s;
        SELECT 'complete'
    """

    params = {
        'user_id': user_id
    }

    with psycopg2.connect(**DB_CONFIG) as conn:
      with conn.cursor() as cur:
        cur.execute(q_1,params)
        result = cur.fetchone()
        if result is not None and result[0] == 0:
                cur.execute(query, params)
                result = cur.fetchall()
                return True
        else:
            st.error("Вы не можете удалить аккаунт, т.к. У вас есть ещё неотмененные и недоставленные заказы.")
            return False