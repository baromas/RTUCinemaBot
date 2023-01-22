from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from main import dp
from sql import add


# reserved = False


# Start of programme
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    kb_reserve = [[types.KeyboardButton(text="Забронировать место в кинозале")]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_reserve,
        resize_keyboard=True)
    greetings = "Здравствуй, {}!".format(message.from_user.first_name)
    await message.answer(text=greetings, reply_markup=keyboard)


# await message.answer(text=message.from_user.id)
# await message.answer(text=message.from_user.first_name)
# if reserved:
# await message.answer(text="У Вас уже есть забронированное место")
# await state.clear()
# global reserved
# reserved = True

#inkb_date = types.InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="22.01", callback_data='22.01'))


# FSM booking
class FSMBooking(StatesGroup):
    name = State()
    date = State()
    time = State()
    seat = State()


@dp.message_handler(Text("Забронировать место в кинозале"))
async def cmd_book(message: Message):
    await FSMBooking.name.set()
    await message.answer(
        text="Введите своё ФИО",
        reply_markup=types.ReplyKeyboardRemove(),
        )


@dp.message_handler(state=FSMBooking.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Выберите дату")
    await FSMBooking.next()


@dp.message_handler(state=FSMBooking.date)
async def set_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Выберите время")
    await FSMBooking.next()


@dp.message_handler(state=FSMBooking.time)
async def set_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("Выберите место")
    await FSMBooking.next()


@dp.message_handler(state=FSMBooking.seat)
async def set_seat(message: Message, state: FSMContext):
    await state.update_data(seat=message.text)
    data = await state.get_data()
    await add(data['name'], data['date'], data['time'], data['seat'])
    await message.answer("Бронирование успешно завершено")
    await state.finish()
