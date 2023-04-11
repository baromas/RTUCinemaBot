import sqlite3
import datetime


def connect_db():
    return sqlite3.connect('booking.db')


async def add_user(user_id, user_name, full_name, room, phone_number):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(number) FROM users;')
        num = cursor.fetchone()[0] + 1
        m = [num, user_id, user_name, full_name, room, phone_number]
        cursor.execute('INSERT INTO users (number, user_id, user_name, full_name, room, phone_number)'
                       ' VALUES (?,?,?,?,?,?)', m)
        conn.commit()


async def add_record(user_id, full_name, date, time, seat):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(number) FROM records;')
        num = cursor.fetchone()[0] + 1
        m = [user_id, num, full_name, date, time, seat]
        cursor.execute('INSERT INTO records (user_id, number, full_name, date, time, companions) VALUES (?,?,?,?,?,?)',
                       m)
        conn.commit()


async def get_full_name(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT full_name FROM users WHERE user_id = ?", (user_id,))
        name = cursor.fetchone()[0]
        conn.commit()
    return name


async def get_room(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT room FROM users WHERE user_id = ?", (user_id,))
        room = cursor.fetchone()[0]
        conn.commit()
    return room


async def get_phone_number(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT phone_number FROM users WHERE user_id = ?", (user_id,))
        phone_number = cursor.fetchone()[0]
        conn.commit()
    return phone_number


async def check_user(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        exists = cursor.execute("SELECT EXISTS(SELECT user_id FROM users WHERE user_id = ?)", (user_id,)).fetchone()[0]
        conn.commit()
    return exists


async def check_reservation(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        exists = cursor.execute("""SELECT EXISTS(SELECT user_id FROM records WHERE (user_id = ?) \
             AND (date = ? OR date = ? OR date = ?))""",
                                (user_id,
                                 datetime.datetime.today().strftime("%d.%m.%Y"),
                                 (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y"),
                                 (datetime.date.today() + datetime.timedelta(days=2)).strftime("%d.%m.%Y"))).fetchone()[
            0]
        conn.commit()
    return exists


async def get_reservation(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        reservation = {
            "name": cursor.execute("SELECT full_name FROM records WHERE user_id = ?", (user_id,)).fetchone()[0],
            "date": cursor.execute("SELECT date FROM records WHERE user_id = ?", (user_id,)).fetchone()[0],
            "time": cursor.execute("SELECT time FROM records WHERE user_id = ?", (user_id,)).fetchone()[0],
            "companions": cursor.execute("SELECT companions FROM records WHERE user_id = ?", (user_id,)).fetchone()[0]
        }
        conn.commit()
    return reservation


async def get_user_info(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        user = {
            "name": cursor.execute("SELECT full_name FROM users WHERE user_id = ?", (user_id,)).fetchone()[0],
            "room": cursor.execute("SELECT room FROM users WHERE user_id = ?", (user_id,)).fetchone()[0],
            "phone_number": cursor.execute("SELECT phone_number FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        }
        conn.commit()
    return user


async def edit_name(user_id, full_name):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET full_name = ? WHERE user_id = ?", (full_name, user_id))
        if cursor.execute("SELECT EXISTS(SELECT user_id FROM records WHERE user_id = ?)", (user_id,)).fetchone()[0]:
            cursor.execute("UPDATE records SET full_name = ? WHERE user_id = ?", (full_name, user_id))
        conn.commit()


async def edit_room(user_id, room):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET room = ? WHERE user_id = ?", (room, user_id))
        conn.commit()


async def edit_phone(user_id, phone):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET phone = ? WHERE user_id = ?", (phone, user_id))
        conn.commit()


async def check_reservation_day(date):
    with connect_db() as conn:
        cursor = conn.cursor()
        reservation = {
            "16:00": cursor.execute("SELECT EXISTS(SELECT user_id FROM records WHERE date = ? AND time = '16:00')",
                                    (date,)).fetchone()[0],
            "18:00": cursor.execute("SELECT EXISTS(SELECT user_id FROM records WHERE date = ? AND time = '18:00')",
                                    (date,)).fetchone()[0],
            "20:00": cursor.execute("SELECT EXISTS(SELECT user_id FROM records WHERE date = ? AND time = '20:00')",
                                    (date,)).fetchone()[0],
        }
        conn.commit()
    return reservation


async def delete_record(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE from records WHERE user_id = ?", (user_id,))
        conn.commit()
