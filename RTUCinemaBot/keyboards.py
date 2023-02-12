from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

inline_btn_continue = InlineKeyboardButton('Продолжить', callback_data='Продолжить')
inline_kb_continue = InlineKeyboardMarkup().add(inline_btn_continue)
