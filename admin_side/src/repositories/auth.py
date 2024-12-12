from pandas import DataFrame
import psycopg2
from settings import DB_CONFIG
from datetime import date
import pandas as pd
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_auth(login, non_hashed_password):
    password=hash_password(non_hashed_password)
    query = """select max(case when login= %(login)s and hashed_password=%(password)s then 1 else 0 end) from admins"""
    with psycopg2.connect(**DB_CONFIG) as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(query, {"login": login, "password": password})
            result = cursor.fetchone()
            print(result)

            if result is None or result[0] == 0 or result[0]== None:
                return False
            else:
                print(result)
                return True
