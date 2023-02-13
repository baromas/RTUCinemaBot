import pathlib
from pathlib import Path
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.markdown import bold

from main import dp
from keyboards import inline_kb_continue, inline_kb_start, inline_btn_back_edit, inline_kb_back_edit, \
    inline_kb_date, inline_kb_time, inline_kb_cancel, inline_kb_back, inline_kb_no_res, inline_kb_edit
from sql import *

logo_path = Path(pathlib.Path.home(), 'RTUCinemaBot', 'RTUCinemaBot', 'CinemaBotLogo.png')


# FSM
class FSMUserInfo(StatesGroup):
    full_name = State()
    room = State()
    phone_number = State()


class FSMBooking(StatesGroup):
    date = State()
    time = State()
    list = State()


class FSMEdit(StatesGroup):
    name = State()
    room = State()
    phone = State()


# Start of programme
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    if await check_user(message.from_user.id):
        user_info = await get_user_info(message.from_user.id)
        await message.answer_photo(photo=types.InputFile(logo_path),
                                   caption=f"👤 Пользователь: <b>{(user_info['name'])}</b>\n"
                                           f"🏠 Комната: <b>{(user_info['room'])}</b>\n"
                                           f"☎ Номер телефона: <b>{(user_info['phone_number'])}</b>",
                                   parse_mode=types.ParseMode.HTML,
                                   reply_markup=inline_kb_start)
    else:
        greetings = f"""Привет, {message.from_user.first_name}!
        
На территории кинозала установлены следующие правила:
1. Запрещено мусорить 
2. Запрещено курить и употреблять алкоголь 
3. Запрещено превышать допустимый уровень шума
4. После завершения сеанса (при необходимости) передвинуть мебель обратно согласно штатной расстановке
5. Выключить всю аппаратуру и свет после завершения сеанса
6. Перед уходом убедитесь, что зал закрыт

Внимание! В кинозале ведется видеонаблюдение!
Спасибо, что соблюдаете правила

Перед тем как приступить к работе, Вам необходимо внести короткую информацию о себе.
Пожалуйста, нажмите кнопку "Продолжить" """
        await message.answer(text=greetings, reply_markup=inline_kb_continue)


# Reverse button
@dp.callback_query_handler(text='back_start')
async def go_back(callback: types.CallbackQuery, state: FSMContext):
    user_info = await get_user_info(callback.from_user.id)
    await callback.message.edit_caption(caption=f"👤 Пользователь: <b>{(user_info['name'])}</b>\n"
                                                f"🏠 Комната: <b>{(user_info['room'])}</b>\n"
                                                f"☎ Номер телефона: <b>{(user_info['phone_number'])}</b>",
                                        parse_mode=types.ParseMode.HTML,
                                        reply_markup=inline_kb_start)
    await callback.answer()


@dp.callback_query_handler(Text("Мои бронирования"))
async def cmd_check_res(callback: types.CallbackQuery):
    if await check_reservation(callback.from_user.id):
        reservations = await get_reservation(callback.from_user.id)
        await callback.message.edit_caption(caption=f"👤 Пользователь: <b>{(reservations['name'])}</b>\n"
                                                    f"📅 Дата: <b>{(reservations['date'])}</b>\n"
                                                    f"🕒 Время: <b>{(reservations['time'])}</b>\n"
                                                    f"👯 Список людей: <b>{(reservations['companions'])}</b>",
                                            parse_mode=types.ParseMode.HTML,
                                            reply_markup=inline_kb_back)
    else:
        await callback.message.edit_caption(caption="У Вас сейчас отсутствуют бронирования",
                                            reply_markup=inline_kb_no_res)
    await callback.answer()


@dp.callback_query_handler(Text("Редактировать профиль"))
async def cmd_edit_user(callback: types.CallbackQuery):
    user_info = await get_user_info(callback.from_user.id)
    await callback.message.edit_caption(caption=f"👤 Пользователь: <b>{(user_info['name'])}</b>\n"
                                                f"🏠 Комната: <b>{(user_info['room'])}</b>\n"
                                                f"☎ Номер телефона: <b>{(user_info['phone_number'])}</b>\n\n"
                                                "Выберите пункт, который хотите редактировать 👇",
                                        parse_mode=types.ParseMode.HTML,
                                        reply_markup=inline_kb_edit)
    await callback.answer()


@dp.callback_query_handler(text_startswith="edit_")
async def cmd_edit(callback: types.CallbackQuery):
    if callback.data.replace('edit_', '') == "name":
        await FSMEdit.name.set()
        await callback.message.edit_caption(caption="Введите своё ФИО", reply_markup=inline_kb_back_edit)
    if callback.data.replace('edit_', '') == "room":
        await FSMEdit.room.set()
        await callback.message.edit_caption(caption="Введите номер Вашей комнаты", reply_markup=inline_kb_back_edit)
    if callback.data.replace('edit_', '') == "phone":
        await FSMEdit.phone.set()
        await callback.message.edit_caption(caption="Введите Ваш контактный номер телефона",
                                            reply_markup=inline_kb_back_edit)
    await callback.answer()


@dp.callback_query_handler(text='back_edit', state="*")
async def edit_finish(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await cmd_edit_user(callback)
    await callback.answer()


# @dp.callback_query_handler(text='back_book', state="*")
# async def back_book(callback: types.CallbackQuery, state: FSMContext):
#     await FSMBooking.previous()
#     await callback.answer()


@dp.message_handler(state=FSMEdit.name)
async def edit_full_name(message: Message, state: FSMContext):
    await edit_name(message.from_user.id, message.text.strip())
    await message.answer(text="Данные обновлены ✅")
    await cmd_start(message)
    await state.finish()


@dp.message_handler(state=FSMEdit.room)
async def edit_room(message: Message, state: FSMContext):
    await edit_room(message.from_user.id, message.text.strip())
    await message.answer(text="Данные обновлены ✅")
    await cmd_start(message)
    await state.finish()


@dp.message_handler(state=FSMEdit.phone)
async def edit_phone_num(message: Message, state: FSMContext):
    await edit_phone(message.from_user.id, message.text.strip())
    await message.answer(text="Данные обновлены ✅")
    await cmd_start(message)
    await state.finish()



# Add user to db
@dp.callback_query_handler(Text("Продолжить"))
async def cmd_add_user(callback: types.CallbackQuery):
    await FSMUserInfo.full_name.set()
    await callback.message.answer(text="Введите своё ФИО")
    await callback.answer()


@dp.message_handler(state=FSMUserInfo.full_name)
async def set_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer(text="Введите номер блока и комнаты")
    await FSMUserInfo.next()


@dp.message_handler(state=FSMUserInfo.room)
async def set_room(message: Message, state: FSMContext):
    await state.update_data(room=message.text.strip().replace(' ', '/').replace('\\', '/'))
    await message.answer("Введите контактный номер телефона")
    await FSMUserInfo.next()


@dp.message_handler(state=FSMUserInfo.phone_number)
async def set_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text.strip())
    data = await state.get_data()
    await add_user(message.from_user.id, message.from_user.username, data['full_name'], data['room'],
                   data['phone_number'])
    await message.answer("Регистрация прошла успешно ✅")
    await cmd_start(message)
    await state.finish()


# Add record to db
@dp.callback_query_handler(Text("Забронировать место в кинозале"))
async def cmd_book(callback: types.CallbackQuery):
    if await check_reservation(callback.from_user.id):
        reservations = await get_reservation(callback.from_user.id)
        await callback.message.edit_caption(caption="У Вас уже есть одно бронирование:\n\n"
                                                    f"👤 Пользователь: <b>{(reservations['name'])}</b>\n"
                                                    f"📅 Дата: <b>{(reservations['date'])}</b>\n"
                                                    f"🕒 Время: <b>{(reservations['time'])}</b>\n"
                                                    f"👯 Список людей: <b>{(reservations['companions'])}</b>",
                                            parse_mode=types.ParseMode.HTML,
                                            reply_markup=inline_kb_back)
    else:
        await FSMBooking.date.set()
        await callback.message.edit_caption(
            caption="📅 Выберите желаемую дату 👇", reply_markup=inline_kb_date)
        await callback.answer()


@dp.callback_query_handler(text_startswith='date_', state=FSMBooking.date)
async def set_date(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(date=callback.data)
    await callback.message.edit_caption(
        caption="🕒 Выберите время 👇", reply_markup=inline_kb_time)
    await FSMBooking.next()
    await callback.answer()


@dp.callback_query_handler(text_startswith='time_', state=FSMBooking.time)
async def set_time(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(time=callback.data)
    await callback.message.edit_caption("👯 Пожалуйста, напишите через запятую список всех людей,"
                                        " которые идут с Вами в кинозал")
    await FSMBooking.next()
    await callback.answer()


@dp.message_handler(state=FSMBooking.list)
async def set_list(message: Message, state: FSMContext):
    await state.update_data(list=message.text)
    data = await state.get_data()
    await add_record(message.from_user.id, await get_full_name(message.from_user.id), data['date'].replace('date_', ''),
                     data['time'].replace('time_', ''), data['list'])
    await message.answer("Бронирование успешно завершено ✅")
    await cmd_start(message)
    await state.finish()
