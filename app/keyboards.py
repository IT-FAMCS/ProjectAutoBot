from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import app.database.request as rq
async def main_keyboard(user_id):
    inline_keyboard=[
        [InlineKeyboardButton(text="Запросить освобождение", callback_data= 'exemption_request'),
        InlineKeyboardButton(text="Меню бюджета", callback_data= 'budget_menu')]]
    admins = await rq.get_admins()
    if user_id in admins:
        inline_keyboard.append(InlineKeyboardButton(text ="Админ панель", callback_data= "admin_panel"))
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

budget_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Запросить возврат средств", callback_data="repayment_request"),
         InlineKeyboardButton(text="Запросить данные о бюджете", callback_data="budget_data_request")]
    ]
)

admin_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить ответственного за освобождения", callback_data="set_exemption_admin"),
         InlineKeyboardButton(text="Удалить ответсвенного за освобождения", callback_data="delete_exemption_admin")],
        [InlineKeyboardButton(text="Добавить ответственного за бюджет", callback_data="set_budget_admin"),
         InlineKeyboardButton(text="Удалить ответсвенного за бюджет", callback_data="delete_budget_admin")],
        [InlineKeyboardButton(text="Добавить секретаря", callback_data="set_secretary"),
         InlineKeyboardButton(text="Удалить секретаря", callback_data="delete_secretary")]
    ]
)

user_confirm_exemption = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text="Всё верно", callback_data= 'user_confirmed_exemption'),
     InlineKeyboardButton(text="Отмена", callback_data='user_cancel_exemption')]
    ]
)

user_confirm_repayment = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text="Всё верно", callback_data= 'user_confirmed_repayment'),
     InlineKeyboardButton(text="Отмена", callback_data='user_cancel_repayment')]
    ]
)
def admin_handle_request(request_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить", callback_data= f'approve_request:{request_id}'),
        InlineKeyboardButton(text="Отклонить", callback_data= f'decline_request:{request_id}')] 
        ]
    )
    return markup