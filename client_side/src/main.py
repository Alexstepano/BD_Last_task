import streamlit as st
from repositories.auth import get_auth
from repositories.auth import get_courier_auth
from repositories.auth import user_reg_pages
from repositories.auth import courier_reg_pages,deleting_user_update
import pandas as pd
from repositories.user_func import get_orders_statistics,get_titles_list,get_cassette_count,get_title_description,add_title_event, clear_table_event,create_order,see_not_delivered,cancel_order
from repositories.courier_func import cur_orders,renew_order_status,cur_orders_list
# Функция для отображения страницы авторизации
def show_login_page():
    st.title("Авторизация")
    tel = st.text_input("Телефон", key="login_tel")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Пароль", type="password", key="login_password")
    on = st.checkbox("Зайти в качестве курьера", key="login_on")
    if st.button("Войти", key="login_button"):
        if not tel or not email or not password:
            st.error("Все поля обязательны для заполнения.")
        else:
            if not on:
                result = get_auth(tel, email, password)
            else:
                result = get_courier_auth(tel, email, password)
            if result[0] == False:
                st.error("Неверный логин или пароль.")
            else:
                print(result[1])
                st.session_state.client_id = result[1]
                st.session_state.authenticated = True
                st.session_state.is_courier = on
                st.success("Авторизация успешна!")
                st.rerun()  # Перезапуск приложения для обновления состояния

    if st.button("Зарегистрироваться", key="register_button"):
        st.session_state.show_registration = True
        st.rerun()  # Перезапуск приложения для обновления состояния




# Функция для отображения страницы регистрации
def show_user_registration_page():
    st.title("Регистрация")
    first_name = st.text_input("Имя", key="user_first_name")
    second_name = st.text_input("Фамилия", key="user_second_name")
    third_name = st.text_input("Отчество", key="user_third_name")
    email = st.text_input("Email", key="user_email")
    tel = st.text_input("Телефон", key="user_tel")
    street = st.text_input("Улица", key="user_street")
    house_num = st.number_input("Номер дома", min_value=0, step=1, key="user_house_num")
    flat_num = st.number_input("Номер квартиры", min_value=0, step=1, key="user_flat_num")
    password = st.text_input("Пароль", type="password", key="user_password")
    on = st.checkbox("Зайти в качестве курьера", key="user_on")
    if on:
        st.session_state.show_courier_registration = True
        st.rerun()  # Перезапуск приложения для обновления состояния
    if st.button("Зарегистрироваться", key="user_register_button"):
        if not first_name or not second_name or not email or not tel or not street or not house_num or not flat_num or not password:
            st.error("Все поля обязательны для заполнения.")
        else:
            result = user_reg_pages(first_name, second_name, third_name, email, tel, street, house_num, flat_num, password)
            if result == False:
                st.error("Ошибка регистрации. Данный номер или почта уже есть в системе.")
            else:
                st.success("Регистрация успешна! Пожалуйста, войдите в систему.")
                st.session_state.show_registration = False
                st.rerun()  # Перезапуск приложения для обновления состояния
    
    if st.button("Вернуться к авторизации", key="user_back_button"):
        st.session_state.show_registration = False
        st.rerun()  # Перезапуск приложения для обновления состояния
    

# Функция для отображения страницы регистрации курьера
def show_courier_registration_page():
    st.title("Регистрация курьера")
    first_name = st.text_input("Имя", key="courier_first_name")
    second_name = st.text_input("Фамилия", key="courier_second_name")
    third_name = st.text_input("Отчество", key="courier_third_name")
    email = st.text_input("Email", key="courier_email")
    tel = st.text_input("Телефон", key="courier_tel")
    password = st.text_input("Пароль", type="password", key="courier_password")
    on = st.checkbox("Зайти в качестве пользователя", key="user_on")
    if on:
        st.session_state.show_courier_registration = False
        st.rerun()  # Перезапуск приложения для обновления состояния
    if st.button("Зарегистрироваться", key="courier_register_button"):
        if not first_name or not second_name or not email or not tel or not password:
            st.error("Все поля обязательны для заполнения.")
        else:
            result = courier_reg_pages(first_name, second_name, third_name, email, tel, password)
            if result == False:
                st.error("Ошибка регистрации. Данный номер или почта уже есть в системе.")
            else:
                st.success("Регистрация успешна! Пожалуйста, войдите в систему.")
                st.session_state.show_registration = False
                st.rerun()  # Перезапуск приложения для обновления состояния

    if st.button("Вернуться к авторизации", key="courier_back_button"):
        st.session_state.show_registration = False
        st.rerun()  # Перезапуск приложения для обновления состояния

# Функция для отображения кнопки выхода
def show_logout_button():
    if st.sidebar.button("Выйти", key="logout_button"):
        st.session_state.authenticated = False
        st.rerun()  # Перезапуск приложения для обновления состояния
def show_main_page():
    st.title("Главная страница")
    delete_button=st.sidebar.button("Удалить аккаунт", key="delete_button")
    if 'client_id' in st.session_state:
        st.write(f"Ваш user_id: {st.session_state.client_id}")
    else:
        st.write("user_id не найден.")
    
    if st.button("Показать историю заказов"):
        df = get_orders_statistics()
        st.write(df)
    st.title("Заказ видеокассеты")
    
    title_list=get_titles_list()
    selected_title = st.selectbox("Выберите фильм:", title_list)
    orders_listik = see_not_delivered()
    if selected_title:
        cassette_count = get_cassette_count(selected_title)
        title_description = get_title_description(selected_title)
        st.write(f"Число кассет: {cassette_count}")
        st.write(f"Описание фильма: {title_description}")

    if 'order_table' not in st.session_state:
        st.session_state.order_table = pd.DataFrame(columns=["Название фильма", "title_id"])
    st.write('Aдрес доставки')
    street = st.text_input("Улица:")
    house_num = st.number_input("Номер дома:", min_value=0,step=1)
    flat_num = st.number_input("Номер квартиры:", min_value=0,step=1)

    add_title_btn = st.button("Добавить фильм")
    clear_table_btn = st.button("Очистить список для заказов")
    apply_btn = st.button("Подтвердить заказ")
    if delete_button:
        a=deleting_user_update()
        if a:
            st.session_state.authenticated = False
            st.rerun()
        
    if add_title_btn:
        add_title_event(selected_title)
    if clear_table_btn:
        clear_table_event()
    if apply_btn and len(st.session_state.order_table) > 0:
        title_ids = st.session_state.order_table["title_id"].tolist()
        order_id=create_order(street, house_num, flat_num, title_ids)
        st.success(f"Заказ создан успешно! ID заказа: {order_id}")
        clear_table_event()
        st.rerun()
    elif apply_btn and len(st.session_state.order_table) <=0:
        st.write("Ошибка.Ваш будущий заказ пуст.Добавьте фильмы")
    st.write("Ваш будущий заказ")
    st.dataframe(st.session_state.order_table)
    st.title("Отменить заказ ")
    add_title_btn = st.button("Отменить заказ ниже")
    not_del_order = st.selectbox("Выберите заказ:", orders_listik)
    if add_title_btn:
        cancel_order(not_del_order)
        st.rerun()
    
   
        
def show_courier_main_page():
    st.title("Главная страница курьера")
    st.write("Добро пожаловать, курьер!")
    if st.button("Показать текущие заказы"):
        df = cur_orders()
        st.write(df)
    st.title("Обновить  статус заказа")
    selected_order = st.selectbox("Выберите заказ:",  cur_orders_list())
    stat_order = st.selectbox("Выберите новый статус заказа:", ['Доставляется','Доставлено','Не смог доставить'])
    update_btn = st.button("Передать статус заказа")
    if update_btn:
        renew_order_status(selected_order,stat_order)

    

# Главная логика приложения с навигацией
def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'show_registration' not in st.session_state:
        st.session_state.show_registration = False
    if 'show_courier_registration' not in st.session_state:
        st.session_state.show_courier_registration = False
    if 'is_courier' not in st.session_state:
        st.session_state.is_courier = False

    if not st.session_state.authenticated:
        if st.session_state.show_registration:
            if st.session_state.show_courier_registration:
                show_courier_registration_page()
            else:
                show_user_registration_page()
        else:
            show_login_page()
    else:
        st.sidebar.title("Навигация")
        show_logout_button()
        if st.session_state.is_courier:
            show_courier_main_page()
        else:
            show_main_page()

if __name__ == "__main__":
    main()