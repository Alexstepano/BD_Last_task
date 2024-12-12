import streamlit as st
from repositories.auth import get_auth
import repositories.products as f
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
def auth_page():
    st.title("Доступ")
    login = st.text_input("LOGIN", key="login")
    password = st.text_input("Пароль", type="password", key="password")
    if st.button("Войти", key="login_button"):
        if not login or not password:
            st.error("Все поля обязательны для заполнения.")
        else:
            result = get_auth(login, password)
            if result == False:
                st.error("Неверный логин или пароль.")
            else:
                st.session_state.authenticated = True
                st.success("Авторизация успешна!")
                st.rerun()  # Перезапуск приложения для обновления состояния

def show_logout_button():
    if st.sidebar.button("Выйти", key="logout_button"):
        st.session_state.authenticated = False
        st.session_state.checkbox_states['courier_status_checkbox'] = False
        st.session_state.checkbox_states['order_info_checkbox'] = False
        st.session_state.checkbox_states['filmes_pages'] = False
        st.session_state.checkbox_states['cassettes_pages'] = False
        st.rerun()  # Перезапуск приложения для обновления состояния

def main_functional():
    st.title("Добро пожаловать")
    clients = f.get_clients()
    selected_client = st.selectbox("Выберите клиента:", clients)

    if selected_client:
        client_info_list = f.get_client_info(selected_client)

        if client_info_list:
            client_info = client_info_list[0]

            st.write("Информация о клиенте:")
            st.json(client_info)

            st.write("Модифицировать информацию о клиенте:")
            new_first_name = st.text_input("first_name", value=client_info.get('first_name', ''))
            new_second_name = st.text_input("second_name", value=client_info.get('second_name', ''))
            new_third_name = st.text_input("third_name", value=client_info.get('third_name', ''))
            new_email = st.text_input("email", value=client_info.get('email', ''))
            new_telephone = st.text_input("telephone", value=client_info.get('telephone', ''))
            new_street = st.text_input("street", value=client_info.get('street', ''))
            new_house_num = st.text_input("house_num", value=client_info.get('house_num', ''))
            new_flat_num = st.text_input("flat_num", value=client_info.get('flat_num', ''))
            active_flag = st.checkbox("actual_flag",value=client_info.get('actual_flag', ''))
            if st.button("Сохранить изменения"):
                updated_client_info = {
                    'first_name': new_first_name,
                    'second_name': new_second_name,
                    'third_name': new_third_name,
                    'email': new_email,
                    'telephone': new_telephone,
                    'street': new_street,
                    'house_num': new_house_num,
                    'flat_num': new_flat_num,
                    'actual_flag':active_flag
                }
                f.update_client_info(selected_client, updated_client_info)
                st.success("Информация о клиенте успешно обновлена!")
                st.rerun()  # Перезапуск приложения для обновления состояния
        else:
            st.error("Информация о клиенте не найдена.")

def courier_status_page():
    st.title("Изменение статуса курьеров")
    couriers = f.get_couriers()
    selected_courier = st.selectbox("Выберите курьера:", couriers)

    if selected_courier:
        courier_info_list = f.get_courier_info(selected_courier)

        if courier_info_list:
            courier_info = courier_info_list[0]

            st.write("Информация о курьере:")
            st.json(courier_info)

            st.write("Изменить статус курьера:")
            new_first_name = st.text_input("first_name", value=courier_info.get('first_name', ''))
            new_second_name = st.text_input("second_name", value=courier_info.get('second_name', ''))
            new_third_name = st.text_input("third_name", value=courier_info.get('third_name', ''))
            new_email = st.text_input("email", value=courier_info.get('email', ''))
            new_telephone = st.text_input("telephone", value=courier_info.get('telephone', ''))
            active_flag = st.checkbox("actual_flag",value=courier_info.get('actual_flag', ''))
            if st.button("Сохранить изменения"):
                updated_courier_info = {
                    'first_name': new_first_name,
                    'second_name': new_second_name,
                    'third_name': new_third_name,
                    'email': new_email,
                    'telephone': new_telephone,
                    'actual_flag':active_flag
                }
                f.update_courier_status(selected_courier, updated_courier_info)
                st.success("Статус курьера успешно обновлен!")
                st.rerun()  # Перезапуск приложения для обновления состояния
        else:
            st.error("Информация о курьере не найдена.")

def order_status_page():
    st.title("Изменение статуса курьеров")
    couriers = f.get_couriers()
    selected_courier = st.selectbox("Выберите курьера:", couriers)

    if selected_courier:
        courier_info_list = f.get_courier_info(selected_courier)

        if courier_info_list:
            courier_info = courier_info_list[0]

            st.write("Информация о курьере:")
            st.json(courier_info)

            st.write("Изменить статус курьера:")
            new_status = st.selectbox("Новый статус:", ["Активный", "Неактивный", "В пути", "Доставлено"])

            if st.button("Сохранить изменения"):
                updated_courier_info = {
                    'status': new_status
                }
                f.update_courier_status(selected_courier, updated_courier_info)
                st.success("Статус курьера успешно обновлен!")
                st.rerun()  # Перезапуск приложения для обновления состояния
        else:
            st.error("Информация о курьере не найдена.")

def order_info_page():
    st.title("Информация о заказах")
    orders = f.get_orders()
    selected_order = st.selectbox("Выберите заказ:", orders)
    status=f.get_actual_status(selected_order)
    if selected_order:
        order_info_list = f.get_order_info(selected_order)

        if order_info_list:
            order_info = order_info_list[0]

            st.write("Информация о заказе:")
            st.json(order_info)

            st.write("Модифицировать информацию о заказе:")
            new_courier_id = st.text_input("courier_id", value=order_info.get('courier_id', ''))
            new_user_id = st.text_input("user_id", value=order_info.get('user_id', ''))
            new_street = st.text_input("street", value=order_info.get('street', ''))
            new_house_num = st.text_input("house_num", value=order_info.get('house_num', ''))
            new_flat_num = st.text_input("flat_num", value=order_info.get('flat_num', ''))
            new_status=st.text_input("status", value=status)
            if st.button("Сохранить изменения"):
                updated_order_info = {
                    'courier_id': new_courier_id,
                    'user_id': new_user_id,
                    'street': new_street,
                    'house_num': new_house_num,
                    'flat_num': new_flat_num
                }
                f.update_order_info(selected_order, updated_order_info)
                st.success("Информация о заказе успешно обновлена!")
                f.set_new_status(selected_order,new_status)
                st.rerun()  # Перезапуск приложения для обновления состояния
        else:
            st.error("Информация о заказе не найдена.")

def filmes_pages():
    st.title("Информация о фильмах")
    if st.button("Узнать информацию о фильмах"):
        df=f.see_films_statistics();
        st.write(df)
    st.write("Модифицировать информацию о фильме:")
    new_title_name = st.text_input("title_name")
    new_title_description = st.text_input("title_description")
    new_title_rating = st.number_input("title_rating", min_value=1, step=1,max_value=10)
    if st.button("Сохранить изменения"):
        ans=f.add_new_title(new_title_name,new_title_description,new_title_rating)
        
        

def cassettes_page():
    st.title("Информация о кассетах")
    df = f.see_cassettes_statistics()
    st.write(df)
    st.write("Добавть информацию о кассете:")
    new_cassette_status = st.text_input("cassette_status_New")
    if st.button("Добавить новую кассету"):
        f.add_new_cassette(new_cassette_status)
        st.rerun()
    st.write("Изменить информацию о кассете")
    cassettes = f.get_cassettes()
    selected_cassette = st.selectbox("Выберите кассету:", cassettes)
    if selected_cassette:
        cassette_info_list = f.get_cassette_info(selected_cassette)

        if cassette_info_list:
            cassette_info = cassette_info_list[0]

            st.write("Информация о кассете:")
            st.json(cassette_info)

            st.write("Модифицировать статус кассеты:")
            new_cassette_status = st.text_input("cassette_status", value=cassette_info.get('cassette_status', ''))

            if st.button("Сохранить изменения"):
                updated_cassette_info = {
                    'cassette_status': new_cassette_status
                }
                f.update_cassette_info(selected_cassette, updated_cassette_info)
                st.success("Информация о кассете успешно обновлена!")
                st.rerun()  # Перезапуск приложения для обновления состояния
        else:
            st.error("Информация о кассете не найдена.")
        films = f.get_film_list()
        selected_film = st.selectbox("Выберите фильм:", films)
        if st.button("Добавить фильм на кассету"):
            f.add_film_to_cassette(selected_cassette, selected_film)
            st.success("Фильм успешно добавлен на кассету!")
            st.rerun()  # Перезапуск приложения для обновления состояния


def reports_page():
    st.title("Отчеты")

    st.subheader("Количество новых пользователей по месяцам")
    new_users_df = f.get_month_users()
    st.write(new_users_df)
    st.line_chart(new_users_df.set_index(0))

    st.subheader("Количество новых курьеров по месяцам")
    new_couriers_df = f.get_month_cur()
    st.write(new_couriers_df)
    st.line_chart(new_couriers_df.set_index(0))
    
    st.subheader("Популярность фильмов")
    st.write("Количество заказов, включающие n-ый фильм")
    popular_films_df = f.get_popular_films_report()
    st.bar_chart(popular_films_df.set_index(0))

    st.subheader("Среднее время выполнения заказов")
    avg_delivery_time = f.get_avg_delivery_time_report()
    st.write(f"Среднее время выполнения заказов: {avg_delivery_time} минут")
    st.subheader("Статусы заказов")
    order_statuses_df = f.get_order_statuses_report()
    fig, ax = plt.subplots()
    ax.pie(order_statuses_df[1], labels=order_statuses_df[0], autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)
    st.subheader("Статусы кассет")
    сassetes_statuses_df = f.get_casstets_statuses_report()
    fig1, ax1 = plt.subplots()
    ax1.pie(сassetes_statuses_df[1], labels=сassetes_statuses_df[0], autopct='%1.1f%%', startangle=140)
    ax1.axis('equal')
    st.pyplot(fig1)
def backup_page():
    st.title("Создание резервных копий таблиц")
    if st.button("Создать резервные копии"):
        try:
            f.get_back_up()
            st.success("Резервные копии таблиц успешно созданы.")
        except Exception as e:
            st.error(f"Ошибка: {e}")
def load_backup_page():
    st.title("Загрузка данных из резервных копий")
    available_backups = f.get_available_backups()
    selected_backup = st.selectbox("Выберите резервную копию для загрузки:", available_backups)

    if st.button("Загрузить данные"):
        try:
            f.load_backup(selected_backup)
            st.success("Данные успешно загружены из резервных копий.")
        except Exception as e:
            st.error(f"Ошибка: {e}")
# Главная логика приложения с навигацией
def main():
    st.sidebar.title("Навигация")
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'checkbox_states' not in st.session_state:
        st.session_state.checkbox_states = {
            'courier_status_checkbox': False,
            'order_info_checkbox': False,
            'filmes_pages': False,
            'cassettes_pages': False,
            'reports_page': False,
            'backup_page': False,
            'load_backup_page': False  
        }
    if not st.session_state.authenticated:
        auth_page()
    else:
        courier_status_checkbox = st.sidebar.checkbox("Изменить статус курьеров", key="courier_status_checkbox", value=st.session_state.checkbox_states['courier_status_checkbox'])
        order_info_checkbox = st.sidebar.checkbox("Информация о заказах", key="order_info_checkbox", value=st.session_state.checkbox_states['order_info_checkbox'])
        filme_checkbox = st.sidebar.checkbox("Информация о фильмах", key="filmo_info_checkbox", value=st.session_state.checkbox_states['filmes_pages'])
        cassette_checkbox = st.sidebar.checkbox("Информация о кассетах", key="cassette_info_checkbox", value=st.session_state.checkbox_states['cassettes_pages'])
        reports_checkbox = st.sidebar.checkbox("Отчеты", key="reports_page", value=st.session_state.checkbox_states['reports_page'])
        backup_checkbox = st.sidebar.checkbox("Создать резервные копии", key="backup_page", value=st.session_state.checkbox_states['backup_page'])  
        load_backup_checkbox = st.sidebar.checkbox("Загрузить резервные копии", key="load_backup_page", value=st.session_state.checkbox_states['backup_page'])
        if courier_status_checkbox:
            courier_status_page()
        elif order_info_checkbox:
            order_info_page()
        elif filme_checkbox:
            filmes_pages()
        elif cassette_checkbox:
            cassettes_page()
        elif reports_checkbox:
            reports_page()
        elif backup_checkbox:
            backup_page() 
        elif load_backup_checkbox:
            load_backup_page()
        else:
            st.session_state.checkbox_states['courier_status_checkbox'] = False
            st.session_state.checkbox_states['order_info_checkbox'] = False
            st.session_state.checkbox_states['filmes_pages'] = False
            st.session_state.checkbox_states['cassettes_pages'] = False
            st.session_state.checkbox_states['reports_page'] = False
            st.session_state.checkbox_states['backup_page'] = False
            st.session_state.checkbox_states['load_backup_page'] = False 
            main_functional()

        show_logout_button()

if __name__ == "__main__":
    main()
