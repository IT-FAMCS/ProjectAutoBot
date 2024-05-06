from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


start = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="На главную")]], resize_keyboard=True, one_time_keyboard=True)


request = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='Запросить освобождение', callback_data='release'), InlineKeyboardButton(text='Бюджет', callback_data='to_budget'), InlineKeyboardButton(text='Шкафчик', callback_data='to_locker')],
    [InlineKeyboardButton(text='Создатели', callback_data="creators"), InlineKeyboardButton(text='На главную', callback_data='to_main')]])


creators = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='Кирюша Зайдаль', url='https://t.me/kirushazaidal')], [InlineKeyboardButton(text='На главную', callback_data='to_main')]])


to_main = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='На главную', callback_data='to_main')]])


budget = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Запросить возврат', callback_data='return_budget'), InlineKeyboardButton(
    text='Запросить данные о бюджете', callback_data='request_budget')]])


accept = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='Принять', callback_data='accept'), InlineKeyboardButton(text='На главную', callback_data='to_main')]])


locker = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='Положить вещи', callback_data='put'), InlineKeyboardButton(text='Взять вещи', callback_data='take')]])


def admin_accept(user_id):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Принять', callback_data=f'accept_admin:{user_id}'),
            InlineKeyboardButton(
                text='Отклонить', callback_data=f'decline_admin:{user_id}')
        ]
    ])
    return markup


create = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Освобождение', callback_data='a_release'), InlineKeyboardButton(
    text='Бюджет', callback_data='a_budget'), InlineKeyboardButton(text='Шкафчик', callback_data='a_locker')]])
