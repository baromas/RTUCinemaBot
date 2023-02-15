import sqlite3
import datetime


async def add_user(user_id, user_name, full_name, room, phone_number):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    cursor.execute('SELECT MAX(number) FROM users;')
    num = cursor.fetchone()[0] + 1
    m = [num, user_id, user_name, full_name, room, phone_number]
    cursor.execute('INSERT INTO users (number, user_id, user_name, full_name, room, phone_number)'
                   ' VALUES (?,?,?,?,?,?)', m)
    connect.commit()
    cursor.close()


async def add_record(user_id, full_name, date, time, seat):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    cursor.execute('SELECT MAX(number) FROM records;')
    num = cursor.fetchone()[0] + 1
    m = [user_id, num, full_name, date, time, seat]
    cursor.execute('INSERT INTO records (user_id, number, full_name, date, time, companions) VALUES (?,?,?,?,?,?)', m)
    connect.commit()
    cursor.close()


async def get_full_name(user_id):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    name = cursor.execute(f"SELECT full_name FROM users WHERE user_id = '{user_id}'").fetchone()[0]
    connect.commit()
    cursor.close()
    return name


async def get_room(user_id):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    room = cursor.execute(f"SELECT room FROM users WHERE user_id = '{user_id}'").fetchone()[0]
    connect.commit()
    cursor.close()
    return room


async def get_phone_number(user_id):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    phone_number = cursor.execute(f"SELECT phone_number FROM users WHERE user_id = '{user_id}'").fetchone()[0]
    connect.commit()
    cursor.close()
    return phone_number


async def check_user(user_id):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    exists = cursor.execute(f"SELECT EXISTS(SELECT user_id FROM users WHERE user_id ='{user_id}')").fetchone()[0]
    connect.commit()
    cursor.close()
    return exists


async def check_reservation(user_id):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    exists = \
        cursor.execute(f"""SELECT EXISTS(SELECT user_id FROM records WHERE (user_id ='{user_id}') \
             AND (date = '{datetime.datetime.today().strftime("%d.%m.%Y")}' OR date = 
             '{(datetime.date.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")}' OR 
             date = '{(datetime.date.today() + datetime.timedelta(days=2)).strftime("%d.%m.%Y")}'))""").fetchone()[0]
    connect.commit()
    cursor.close()
    return exists


async def get_reservation(user_id):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    reservation = {
        "name": cursor.execute(f"SELECT full_name FROM records WHERE user_id = '{user_id}'").fetchone()[0],
        "date": cursor.execute(f"SELECT date FROM records WHERE user_id = '{user_id}'").fetchone()[0],
        "time": cursor.execute(f"SELECT time FROM records WHERE user_id = '{user_id}'").fetchone()[0],
        "companions": cursor.execute(f"SELECT companions FROM records WHERE user_id = '{user_id}'").fetchone()[0]
    }
    connect.commit()
    cursor.close()
    return reservation


async def get_user_info(user_id):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    user = {
        "name": cursor.execute(f"SELECT full_name FROM users WHERE user_id = '{user_id}'").fetchone()[0],
        "room": cursor.execute(f"SELECT room FROM users WHERE user_id = '{user_id}'").fetchone()[0],
        "phone_number": cursor.execute(f"SELECT phone_number FROM users WHERE user_id = '{user_id}'").fetchone()[0]
    }
    connect.commit()
    cursor.close()
    return user


async def edit_name(user_id, full_name):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET full_name = '{full_name}' WHERE user_id ='{user_id}'")
    if cursor.execute(f"SELECT EXISTS(SELECT user_id FROM records WHERE user_id ='{user_id}')").fetchone()[0]:
        cursor.execute(f"UPDATE records SET full_name = '{full_name}' WHERE user_id ='{user_id}'")
    connect.commit()
    cursor.close()


async def edit_room(user_id, room):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET room = '{room}' WHERE user_id ='{user_id}'")
    connect.commit()
    cursor.close()


async def edit_phone(user_id, phone):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    cursor.execute(f"UPDATE users SET phone = '{phone}' WHERE user_id ='{user_id}'")
    connect.commit()
    cursor.close()


async def check_reservation_day(date):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    reservation = {
        "16:00": cursor.execute(f"SELECT EXISTS(SELECT user_id "
                                f"FROM records WHERE date ='{date}' AND time = '16:00')").fetchone()[0],
        "18:00": cursor.execute(f"SELECT EXISTS(SELECT user_id "
                                f"FROM records WHERE date ='{date}' AND time = '18:00')").fetchone()[0],
        "20:00": cursor.execute(f"SELECT EXISTS(SELECT user_id "
                                f"FROM records WHERE date ='{date}' AND time = '20:00')").fetchone()[0],
    }
    connect.commit()
    cursor.close()
    return reservation


async def delete_record(user_id):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    cursor.execute(f"DELETE from records WHERE user_id ='{user_id}'")
    connect.commit()
    cursor.close()
