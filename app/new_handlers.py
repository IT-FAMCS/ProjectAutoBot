from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
import re
import app.new_keyboards as kb
from bot import bot
import app.database.new_request as rq

router = Router()

class UserReg(StatesGroup):
    fio = State()
    username = State()

class UserDel(StatesGroup):
    username = State()

class Exemption_info(StatesGroup):
    fio = State()
    course = State()
    group = State()
    date = State()
    reason = State()
@router.message(CommandStart())

async def start(message: Message):
    await message.answer('Добро пожаловать в бот запросов!', reply_markup=kb.main_keyboard)
    await rq.set_user(message.from_user.id, message.from_user.username)

@router.callback_query(F.data == "exemption_request")
async def exemption_request(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали запрос на освобождение')
    await callback.message.answer('Напишите своё ФИО')
    await state.set_state(Exemption_info.fio)
    
@router.message(Exemption_info.fio)
async def course(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(Exemption_info.course)
    await message.answer('Напишите свой курс')


@router.message(Exemption_info.course)
async def group(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await state.set_state(Exemption_info.group)
    await message.answer('Напишите свою группу')


@router.message(Exemption_info.group)
async def group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(Exemption_info.date)
    await message.answer('Напишите дату и время')


@router.message(Exemption_info.date)
async def date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(Exemption_info.reason)
    await message.answer('Напишите причину')


@router.message(Exemption_info.reason)
async def reason(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_id = message.from_user.id
    await message.answer(f'Ваш запрос на освобождение:\nФИО: {data["fio"]}\nВаш тег: @{data['username']}\nКурс: {data["course"]}\nГруппа: {data["group"]}\nДата и время: {data["date"]}\nПричина: {message.text}',
                         reply_markup=kb.user_confirm_exemption)
    await state.clear()

@router.callback_query(F.data == 'user_confirmed_exepmtion')
async def user_confirmed_exemption(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    request_data = callback.message.text[:4].capitalize()
    await callback.message.edit_text(f'Ваш запрос на {state.get_data()["date"]} принят на рассмотрение.')
    await callback.message.answer('Главное меню', reply_markup=kb.main_keyboard)
    user_id = callback.message.chat.id
    state.clear()
    await rq.set_request(request_data)
    request_id = await rq.get_request_id(request_data)
    admins = await rq.get_exemption_admins()
    for admin in admins:
        await bot.send_message(admin, request_data, reply_markup=kb.admin_handle_request(user_id, request_id))
        
@router.callback_query(F.data == "user_cancel_exemption")
async def user_cancel_exemption(callback: CallbackQuery, state: FSMContext):
    state.clear()
    await callback.message.edit_text('Вы отменили запрос')
    await callback.message.answer('Главное меню', reply_markup=kb.main_keyboard)

@router.callback_query(F.data == "approve_request")
async def approve_exemption(callback: CallbackQuery):
    request_id = callback.data.split(':')[1]
    request_status = await rq.is_request_approved(request_id)
    await callback.answer('')
    if await request_status == "Unprocessed":
        await callback.message.edit_reply_markup()
        await callback.message.answer('Вы одобрили запрос. Запрос передан в секретариат')
        user_id = await rq.get_request_tg_id(request_id)
        request_data = await rq.get_request_data(request_id)
        if(request_data.startswith("Запрос на освобождение")):
            request_date = re.search('Дата и время: (.*)\nПричина:', request_data).group(1)
            await bot.send_message(user_id, f'Ваш запрос на {request_date} одобрен и передан секретарям', reply_markup=kb.main_keyboard)
        else:
            pass #сюда обработчик бюджета ебнуть надо, но я пока не придумал, как он структурируется
        request_data = "Одобрен з" + request_data[1:]
        secretaries = await rq.get_secretaries()
        for secretary in secretaries:
            await bot.send_message(secretary, request_data)
        await rq.set_request_approved(request_id)
    elif request_status == "approved" or "Declined":
        await callback.message.edit_text('Запрос уже обработан')
    else:
        await callback.message.edit_text('Обратитесь за поддержкой в IT-отдел')
        

@router.callback_query(F.data == "decline_request")
async def approve_exemption(callback: CallbackQuery):
    request_id = callback.data.split(':')[1]
    request_status = await rq.is_request_approved(request_id)
    await callback.answer('')
    if await request_status == "Unprocessed":
        await callback.message.edit_reply_markup()
        await callback.message.answer('Вы отклонили запрос')
        user_id = await rq.get_request_tg_id(request_id)
        request_data = await rq.get_request_data(request_id)
        if(request_data.startswith("Запрос на освобождение")):
            request_date = re.search('Дата и время: (.*)\nПричина:', request_data).group(1)
            await bot.send_message(user_id, f'Ваш запрос на {request_date} отказан', reply_markup=kb.main_keyboard)
        else:
            pass #сюда обработчик бюджета ебнуть надо, но я пока не придумал, как он структурируется
        request_data = "Одобрен з" + request_data[1:]
        secretaries = await rq.get_secretaries()
        for secretary in secretaries:
            await bot.send_message(secretary, request_data)
        await rq.set_request_approved(request_id)
    elif request_status == "approved" or "Declined":
        await callback.message.edit_text('Запрос уже обработан')
    else:
        await callback.message.edit_text('Обратитесь за поддержкой в IT-отдел')        
