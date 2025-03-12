from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


start = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="На главную")]], resize_keyboard=True, one_time_keyboard=True)


request = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='Запросить освобождение', callback_data='release'), InlineKeyboardButton(text='Бюджет', callback_data='to_budget')],
    [InlineKeyboardButton(text='Создатели', callback_data="creators"), InlineKeyboardButton(text='На главную', callback_data='to_main')]])


creators = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text='Кирюша Зайдаль', url='https://t.me/kirushazaidal')], [InlineKeyboardButton(text='На главную', callback_data='to_main')]])


to_main = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='На главную', callback_data='to_main')]])


budget = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Запросить возврат', callback_data='return_budget'), InlineKeyboardButton(
    text='Запросить данные о бюджете', callback_data='request_budget')]])




def admin_accept(user_id, id_request):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Принять', callback_data=f'accept_admin:{user_id}:{id_request}'),
            InlineKeyboardButton(
                text='Отклонить', callback_data=f'decline_admin:{user_id}:{id_request}')
        ]
    ])
    return markup


def admin_accept_r(user_id, id_request):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Принять', callback_data=f'accept_admin_r:{user_id}:{id_request}'),
            InlineKeyboardButton(
                text='Отклонить', callback_data=f'decline_admin:{user_id}:{id_request}')
        ]
    ])
    return markup


create = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Освобождение', callback_data='a_release'), InlineKeyboardButton(
    text='Бюджет', callback_data='a_budget')],
    [InlineKeyboardButton(text='Секретарь', callback_data='a_secretary')
     ]])

delete = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Освобождение', callback_data='d_release'), InlineKeyboardButton(
    text='Бюджет', callback_data='d_budget')],
    [InlineKeyboardButton(text='Секретарь', callback_data='d_secretary')
     ]])

# def accept_release(tg_id):
#     markup = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(
#             text="Принять", callback_data=f"accept_release:{tg_id}")],
#         [InlineKeyboardButton(text="На главную", callback_data="to_main")]
#     ])
#     return markup

accept_release = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="Принять", callback_data="accept_release")],
    [InlineKeyboardButton(text="На главную", callback_data="to_main")]
])


accept_budget = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Принять", callback_data="accept_budget")],
    [InlineKeyboardButton(text="На главную", callback_data="to_main")]
])

accept_budget_date = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Принять", callback_data="accept_budget_date")],
    [InlineKeyboardButton(text="На главную", callback_data="to_main")]
])
