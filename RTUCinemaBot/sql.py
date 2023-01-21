import sqlite3


async def add(full_name, date, time, seat):
    connect = sqlite3.connect('booking.db')
    cursor = connect.cursor()
    cursor.execute('SELECT MAX(number) FROM records;')
    num = cursor.fetchone()[0] + 1
    m = [num, full_name, date, time, seat]
    cursor.execute('INSERT INTO records (number, full_name, date, time, seat) VALUES (?,?,?,?,?)', m)
    connect.commit()
    cursor.close()
