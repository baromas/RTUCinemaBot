import pathlib
from pathlib import Path
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from main import dp
from keyboards import inline_kb_continue
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sql import add_record, add_user, get_full_name, get_room, check_user, get_phone_number, get_user_info

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


# Start of programme
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    if await check_user(message.from_user.id):
        await message.answer_photo(photo=types.InputFile(logo_path),
                                   caption=f"Пользователь: {await get_full_name(message.from_user.id)}\n"
                                           f"Комната: {await get_room(message.from_user.id)}"
                                           f"Номер телефона: {await get_phone_number(message.from_user.id)}")
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


# Add user to db
@dp.callback_query_handler(Text("Продолжить"))
async def cmd_add_user(callback: types.CallbackQuery):
    await FSMUserInfo.full_name.set()
    await callback.answer()
    await callback.message.answer(text="Введите своё ФИО")


@dp.message_handler(state=FSMUserInfo.full_name)
async def set_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer("Введите номер блока и комнаты")
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
    await message.answer("Готово!")
    await message.answer_photo(photo=types.InputFile(logo_path),
                               caption=f"Пользователь: {await get_full_name(message.from_user.id)}\n"
                                       f"Номер комнаты: {await get_room(message.from_user.id)}\n"
                                       f"Номер телефона: {await get_phone_number(message.from_user.id)}")
    await state.finish()


# Add record to db
@dp.callback_query_handler(Text("Забронировать место в кинозале"))
async def cmd_book(message: Message):
    await FSMBooking.date.set()
    await message.answer(
        text="Выберите дату",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@dp.message_handler(state=FSMBooking.date)
async def set_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Выберите время")
    await FSMBooking.next()


@dp.message_handler(state=FSMBooking.time)
async def set_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("Пожалуйста, напишите через запятую список всех людей, которые пойдут в кинозал")
    await FSMBooking.next()


@dp.message_handler(state=FSMBooking.list)
async def set_list(message: Message, state: FSMContext):
    await state.update_data(list=message.text)
    data = await state.get_data()
    await add_record(await get_full_name(message.from_user.id), data['date'], data['time'], data['list'])
    await message.answer("Бронирование успешно завершено")
    await state.finish()

# if reserved:
# await message.answer(text="У Вас уже есть забронированное место")
# inkb_date = types.InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="22.01", callback_data='22.01'))
