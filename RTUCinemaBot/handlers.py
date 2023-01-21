from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from main import dp
from sql import add


# Start of programme
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.answer(text="Укажите действие")


# FSM booking
class FSMBooking(StatesGroup):
    name = State()
    date = State()
    time = State()
    seat = State()


@dp.message_handler(commands=['reserve'])
async def cmd_book(message: Message):
    await FSMBooking.name.set()
    await message.answer(text="Введите своё ФИО")


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
    await message.answer("Бронирование успешно создано")
    await state.finish()
