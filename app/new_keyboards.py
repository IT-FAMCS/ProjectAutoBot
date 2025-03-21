from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Запрос освобождения", callback_data= 'exemption_request'),
         InlineKeyboardButton(text="Меню бюджета", callback_data= 'budget_menu')]
    ]
)

user_confirm_exemption = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text="Всё верно", callback_data= 'user_confirmed_exemption'),
     InlineKeyboardButton(text="Отмена", callback_data='user_cancel_exemption')]
    ]
)
def admin_handle_request(user_id, request_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить", callback_data= f'approve_request:{request_id}'),
        InlineKeyboardButton(text="Отклонить", callback_data= f'decline_request:{request_id}')] 
        ]
    )
    return markup