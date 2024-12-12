CREATE TABLE Admins (
    admin_id SERIAL PRIMARY KEY,
    login VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(4000) NOT NULL
);

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    second_name VARCHAR(255) NOT NULL,
    third_name VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    telephone VARCHAR(15) NOT NULL,
    street VARCHAR(255) NOT NULL,
    house_num INTEGER NOT NULL,
    flat_num INTEGER NOT NULL,
    actual_flag BOOLEAN NOT NULL
);

CREATE TABLE Couriers (
    courier_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    second_name VARCHAR(255) NOT NULL,
    third_name VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    telephone VARCHAR(15) NOT NULL,
    actual_flag BOOLEAN NOT NULL
);

CREATE TABLE Titles (
    title_id SERIAL PRIMARY KEY,
    title_name VARCHAR(60) NOT NULL,
    title_description VARCHAR(600) NOT NULL,
    title_rating INTEGER NOT NULL
);

CREATE TABLE Cassettes (
    cassette_id SERIAL PRIMARY KEY,
    cassette_status VARCHAR(15) NOT NULL
);

CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    courier_id INTEGER ,
    user_id INTEGER NOT NULL,
    street VARCHAR(255) NOT NULL,
    house_num INTEGER NOT NULL,
    flat_num INTEGER NOT NULL,
    FOREIGN KEY (courier_id) REFERENCES Couriers(courier_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Order_Titles (
    id SERIAL PRIMARY KEY,
    title_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    FOREIGN KEY (title_id) REFERENCES Titles(title_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

CREATE TABLE Cassette_Titles (
    id SERIAL PRIMARY KEY,
    title_id INTEGER NOT NULL,
    cassette_id INTEGER NOT NULL,
    FOREIGN KEY (title_id) REFERENCES Titles(title_id),
    FOREIGN KEY (cassette_id) REFERENCES Cassettes(cassette_id)
);

CREATE TABLE Orders_History (
    history_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    status VARCHAR(60) NOT NULL,
    time TIMESTAMP NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

CREATE TABLE Client_Password_History (
    id SERIAL PRIMARY KEY,
    client_type BOOLEAN NOT NULL,
    client_id INTEGER NOT NULL,
    hashed_password VARCHAR(4000) NOT NULL,
    time TIMESTAMP NOT NULL
);

-- Триггер для проверки целостности составного ключа.--
CREATE OR REPLACE FUNCTION check_client_id() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.client_type = TRUE THEN
        IF NOT EXISTS (SELECT user_id FROM Users WHERE user_id = NEW.client_id) THEN
            RAISE EXCEPTION 'Invalid client_id for client_type = TRUE';
        END IF;
    ELSE
        IF NOT EXISTS (SELECT courier_id FROM Couriers WHERE courier_id = NEW.client_id) THEN
            RAISE EXCEPTION 'Invalid client_id for client_type = FALSE';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_client_id_trigger
BEFORE INSERT OR UPDATE ON Client_Password_History
FOR EACH ROW EXECUTE FUNCTION check_client_id();
