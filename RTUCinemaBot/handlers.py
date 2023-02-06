from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from main import dp
from sql import add_record, add_user, get_full_name, get_room, check_user


# reserved = False


# FSM
class FSMUserInfo(StatesGroup):
    full_name = State()
    room = State()


class FSMBooking(StatesGroup):
    date = State()
    time = State()
    list = State()


# Start of programme
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    if await check_user(message.from_user.id):
        await message.answer(text=f"Пользователь: {await get_full_name(message.from_user.id)}\n"
                                  f"Номер комнаты: {await get_room(message.from_user.id)}")
    else:
        kb_add_user = [[types.KeyboardButton(text="Продолжить")]]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb_add_user,
            resize_keyboard=True)
        greetings = f"""Привет, {message.from_user.first_name}!
Перед тем как приступить к работе, Вам необходимо внести короткую информацию о себе.
Пожалуйста, нажмите кнопку "Продолжить" """
        await message.answer(text=greetings, reply_markup=keyboard)


# Add user to db
@dp.message_handler(Text("Продолжить"))
async def cmd_add_user(message: Message):
    await FSMUserInfo.full_name.set()
    await message.answer(
        text="Введите своё ФИО",
        reply_markup=types.ReplyKeyboardRemove(),
    )


@dp.message_handler(state=FSMUserInfo.full_name)
async def set_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Введите номер блока и комнаты")
    await FSMUserInfo.next()


@dp.message_handler(state=FSMUserInfo.room)
async def set_room(message: Message, state: FSMContext):
    await state.update_data(room=message.text)
    data = await state.get_data()
    kb_reserve = [[types.KeyboardButton(text="Забронировать место в кинозале")]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_reserve,
        resize_keyboard=True)
    await add_user(message.from_user.id, message.from_user.username, data['full_name'], data['room'])
    await message.answer("Готово!", reply_markup=keyboard)
    await state.finish()


# Add record to db
@dp.message_handler(Text("Забронировать место в кинозале"))
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
    await message.answer("Пожалуйста, через запятую напишите список людей, которые пойдут с Вами в кинозал")
    await FSMBooking.next()


@dp.message_handler(state=FSMBooking.list)
async def set_list(message: Message, state: FSMContext):
    await state.update_data(list=message.text)
    data = await state.get_data()
    await add_record(await get_full_name(message.from_user.id), data['date'], data['time'], data['list'])
    await message.answer("Бронирование успешно завершено")
    await state.finish()

# await message.answer(text=message.from_user.id)
# await message.answer(text=message.from_user.first_name)
# if reserved:
# await message.answer(text="У Вас уже есть забронированное место")
# await state.clear()
# global reserved
# reserved = True
# inkb_date = types.InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="22.01", callback_data='22.01'))
