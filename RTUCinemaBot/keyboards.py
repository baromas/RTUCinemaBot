from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime

# Клавиши отменить и назад
inline_btn_cancel = InlineKeyboardButton('❌ Отменить', callback_data='Отменить')
inline_btn_back_str = InlineKeyboardButton('↩ Назад', callback_data='back_start')
inline_kb_cancel = InlineKeyboardMarkup().add(inline_btn_cancel)
inline_kb_back = InlineKeyboardMarkup().add(inline_btn_back_str)

# Клавиша продолжить после /start
inline_btn_continue = InlineKeyboardButton('Продолжить', callback_data='Продолжить')
inline_kb_continue = InlineKeyboardMarkup().add(inline_btn_continue)

# Клавиши начального интерфейса
inline_btn_check_res = InlineKeyboardButton('Мои бронирования', callback_data='Мои бронирования')
inline_btn_book = InlineKeyboardButton('Забронировать место в кинозале', callback_data='Забронировать место в кинозале')
inline_btn_edit = InlineKeyboardButton('Редактировать профиль', callback_data='Редактировать профиль')
inline_kb_start = InlineKeyboardMarkup(row_width=1).add(inline_btn_check_res, inline_btn_book, inline_btn_edit)

# Клавиши, если "Мои бронирования" ==
inline_btn_delete = InlineKeyboardButton('❌ Удалить запись', callback_data='delete_record')
inline_kb_res = InlineKeyboardMarkup(row_width=1).add(inline_btn_delete, inline_btn_back_str)

# Клавиша, если "Мои бронирования" == Null
inline_kb_no_res = InlineKeyboardMarkup(row_width=1).add(inline_btn_book, inline_btn_back_str)

# Проверить намерения пользователя
inline_btn_yes = InlineKeyboardButton('🔥 Да', callback_data='Да')
inline_btn_no = InlineKeyboardButton('↩ Отмена', callback_data='Мои бронирования')
inline_kb_assure = InlineKeyboardMarkup(row_width=2).add(inline_btn_yes, inline_btn_no)

# Клавиши FSM date
date0 = datetime.date.today().strftime("%d.%m.%Y")
date1 = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
date2 = (datetime.date.today() + datetime.timedelta(days=2)).strftime("%d.%m.%Y")
inline_btn_back_book_date = InlineKeyboardButton('↩ Назад', callback_data='back_book_date')
inline_btn_date0 = InlineKeyboardButton(date0, callback_data=f'date_{date0}')
inline_btn_date1 = InlineKeyboardButton(date1, callback_data=f'date_{date1}')
inline_btn_date2 = InlineKeyboardButton(f'{date2}', callback_data=f'date_{date2}')
inline_kb_date = InlineKeyboardMarkup(row_width=3).add(inline_btn_date0, inline_btn_date1,
                                                       inline_btn_date2, inline_btn_back_book_date)

# Клавиши FSM time
inline_btn_time0 = InlineKeyboardButton('16:00', callback_data='time_16:00')
inline_btn_time1 = InlineKeyboardButton('18:00', callback_data='time_18:00')
inline_btn_time2 = InlineKeyboardButton('20:00', callback_data='time_20:00')
inline_btn_back_book_time = InlineKeyboardButton('↩ Назад', callback_data='back_book_time')

# Клавиша FSM list
inline_btn_back_book_list = InlineKeyboardButton('↩ Назад', callback_data='back_book_list')
inline_kb_list = InlineKeyboardMarkup().add(inline_btn_back_book_list)

# Клавиши "Редактировать профиль"
inline_btn_edit_name = InlineKeyboardButton('ФИО', callback_data='edit_name')
inline_btn_edit_room = InlineKeyboardButton('Номер комнаты', callback_data='edit_room')
inline_btn_edit_phone = InlineKeyboardButton('Номер телефона', callback_data='edit_phone')
inline_kb_edit = InlineKeyboardMarkup(row_width=1).add(inline_btn_edit_name, inline_btn_edit_room,
                                                       inline_btn_edit_phone, inline_btn_back_str)
inline_btn_back_edit = InlineKeyboardButton('↩ Назад', callback_data='back_edit')
inline_kb_back_edit = InlineKeyboardMarkup(row_width=1).add(inline_btn_back_edit)
