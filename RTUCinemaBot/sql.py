import sqlite3


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


async def add_record(full_name, date, time, seat):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    cursor.execute('SELECT MAX(number) FROM records;')
    num = cursor.fetchone()[0] + 1
    m = [num, full_name, date, time, seat]
    cursor.execute('INSERT INTO records (number, full_name, date, time, companions) VALUES (?,?,?,?,?)', m)
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
