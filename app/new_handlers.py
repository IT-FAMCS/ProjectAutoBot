from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
import re
import app.new_keyboards as kb
from bot import bot
import app.database.new_request as rq
import app.middlewares as mw
from typing import List
router = Router()
router.message.middleware(mw.MediaGroupMiddleware())
#state классы

class UserReg(StatesGroup):
    fio = State()
    username = State()

class ExemptionReg(StatesGroup):
    fio = State()
    course = State()
    group = State()
    date = State()
    reason = State()

class RepaymentReg(StatesGroup):
    items = State()
    gurantor = State()
    expenses = State()
    requisites = State()
    photos = State()

class UserDel(StatesGroup):
    username = State()
#хендлеры меню

@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Добро пожаловать в бот запросов!', reply_markup=await kb.main_keyboard(message.from_user.id))
    await rq.set_user(message.from_user.id, message.from_user.username)

@router.message(Command("main"))
async def main_menu(message: Message):
    await message.answer('Главное меню', reply_markup= await kb.main_keyboard(message.from_user.id))

@router.callback_query(F.data == "budget_menu")
async def budget_menu(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Меню бюджета", reply_markup=kb.budget_menu)

@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text("Админ панель :smiling_imp:", reply_markup=kb.admin_panel)


#хендлеры админ панели

@router.callback_query(F.data == "set_exemption_admin")
async def set_exemption_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(UserReg.fio)
    await state.update_data(admin_type="exemption")
    await callback.message.edit_text("Вы выбрали добавление ответсвенного за освобождения")
    await callback.message.answer("Отправьте ФИО ответсвенного")

@router.callback_query(F.data == "set_budget_admin")
async def set_budget_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(UserReg.fio)
    await state.update_data(admin_type="budget")
    await callback.message.edit_text("Вы выбрали добавление ответсвенного за бюджет")
    await callback.message.answer("Отправьте ФИО ответсвенного")

@router.callback_query(F.data == "set_secretary")
async def set_secretary(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(UserReg.fio)
    await state.update_data(admin_type="secretary")
    await callback.message.edit_text("Вы выбрали добавление секретаря")
    await callback.message.answer("Отправьте ФИО ответсвенного")

@router.message(UserReg.fio)
async def admin_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(UserReg.username)
    await message.answer('Отправьте тег ответственного')

@router.message(UserReg.username)
async def admin_username(message: Message, state: FSMContext):
    data = await state.get_data()
    admin_id = await rq.find_user(username = message.text.split('@')[1])
    if admin_id == None:
        await message.answer("Кажется, что пользователь не запускал бота. Попросите его запустить бота и попробуйте ещё раз")
        await state.clear()
        return
    if data["admin_type"] == "exemption":
        exemption_admins = await rq.get_exemption_admins()
        if admin_id in exemption_admins:
            await message.answer("Человек, которого вы пытаетесь добавить, уже является ответсвенным за освобождения")
            await state.clear()
            return  
        rq.set_exemption_admin(fio = data["fio"], tg_id=admin_id)
        await message.answer("Вы добавили нового ответственного за освобождения")
        await state.clear()
        return
    
    if data["admin_type"] == "budget":
        secretaries = await rq.get_budget_admins()
        if admin_id in secretaries:
            message.answer("Человек, которого вы пытаетесь добавить, уже является ответсвенным за бюджет")
            await state.clear()
            return  
        rq.set_budget_admin(fio = data["fio"], tg_id=admin_id)
        await message.answer("Вы добавили нового ответственного за бюджет")
        await state.clear()
        return
    
    if data["admin_type"] == "secretary":
        secretaries = await rq.get_secretaries()
        if admin_id in secretaries:
            message.answer("Человек, которого вы пытаетесь добавить, уже является секретарём")
            await state.clear()
            return  
        rq.set_secretary(fio = data["fio"], tg_id=admin_id)
        await message.answer("Вы добавили нового секретаря")
        await state.clear()
        return

@router.callback_query(F.data == "delete_exemption_admin")
async def set_exemption_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(UserDel.username)
    await state.update_data(admin_type="exemption")
    await callback.message.edit_text("Вы выбрали удаление ответсвенного за освобождения")
    await callback.message.answer("Отправьте юзернейм ответсвенного за освобождения")

@router.callback_query(F.data == "delete_budget_admin")
async def set_exemption_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(UserDel.username)
    await state.update_data(admin_type="budget")
    await callback.message.edit_text("Вы выбрали удаление ответсвенного за бюджет")
    await callback.message.answer("Отправьте юзернейм ответсвенного за бюджет")

@router.callback_query(F.data == "delete_secretary")
async def set_exemption_admin(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await state.set_state(UserDel.username)
    await state.update_data(admin_type="secretary")
    await callback.message.edit_text("Вы выбрали удаление секретаря")
    await callback.message.answer("Отправьте юзернейм секретаря")

@router.message(UserDel.username)
async def admin_username(message: Message, state: FSMContext):
    data = await state.get_data()
    admin_id = await rq.find_user(username = message.text.split('@')[1])
    if admin_id == None:
        await message.answer("Этот пользователь не использует бота. Вероятнее всего, вы ошиблись")
        await state.clear()
        return
    if data["admin_type"] == "exemption":
        exemption_admins = await rq.get_exemption_admins()
        if admin_id not in exemption_admins:
            await message.answer("Данный пользователем не является ответственным за освобождения")
            await state.clear()
            return  
        rq.delete_exemption_admin(admin_id)
        await message.answer("Вы удалили ответственного за освобождения")
        await state.clear()
        return
    
    if data["admin_type"] == "budget":
        secretaries = await rq.get_budget_admins()
        if admin_id in secretaries:
            message.answer("Данный пользователем не является ответственным за бюджет")
            await state.clear()
            return  
        rq.delete_budget_admin(admin_id)
        await message.answer("Вы удалили ответственного за бюджет")
        await state.clear()
        return
    
    if data["admin_type"] == "secretary":
        secretaries = await rq.get_secretaries()
        if admin_id in secretaries:
            message.answer("Данный пользователем не является секретарём")
            await state.clear()
            return  
        rq.delete_secretary(admin_id)
        await message.answer("Вы удалили секретаря")
        await state.clear()
        return


#хендлеры запроса освободоса

@router.callback_query(F.data == "exemption_request")
async def exemption_request(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text('Вы выбрали запрос на освобождение')
    await callback.message.answer('Напишите своё ФИО')
    await state.set_state(ExemptionReg.fio)
    
@router.message(ExemptionReg.fio)
async def fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(ExemptionReg.course)
    await message.answer('Напишите свой курс')

@router.message(ExemptionReg.course)
async def course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await state.set_state(ExemptionReg.group)
    await message.answer('Напишите свою группу')

@router.message(ExemptionReg.group)
async def group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(ExemptionReg.date)
    await message.answer('Напишите дату и время')

@router.message(ExemptionReg.date)
async def date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(ExemptionReg.reason)
    await message.answer('Напишите причину')

@router.message(ExemptionReg.reason)
async def reason(message: Message, state: FSMContext):
    data = await state.get_data()
    username = message.from_user.username
    await message.answer(f'Ваш запрос на освобождение:\nФИО: {data["fio"]}\nВаш тег: @{username}\nКурс: {data["course"]}\nГруппа: {data["group"]}\nДата и время: {data["date"]}\nПричина: {message.text}',
                         reply_markup=kb.user_confirm_exemption)

@router.callback_query(F.data == 'user_confirmed_exemption')
async def user_confirmed_exemption(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    request_data = 'З'+ callback.message.text[5:]
    data = await state.get_data()
    request_date = data["date"]
    user_id = callback.message.chat.id
    await callback.message.edit_text(f'Ваш запрос на {request_date} принят на рассмотрение.')
    await callback.message.answer('Главное меню', reply_markup= await kb.main_keyboard(user_id))
    await state.clear()
    await rq.set_request(text=request_data, tg_id=user_id)
    request_id = await rq.get_request_id(request_data)
    admins = await rq.get_exemption_admins()
    for admin in admins:
        await bot.send_message(admin, request_data, reply_markup=kb.admin_handle_request(request_id))
        
@router.callback_query(F.data == "user_cancel_exemption")
async def user_cancel_exemption(callback: CallbackQuery, state: FSMContext):
    state.clear()
    await callback.message.edit_text('Вы отменили запрос')
    await callback.message.answer('Главное меню', reply_markup= await kb.main_keyboard(callback.message.chat.id))

#хендлеры запроса возврата средств

@router.callback_query(F.data == "repayment_request")
async def repayment_request(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text('Вы выбрали запрос возврата средств')
    await callback.message.answer('Напишите, что было куплено')
    await state.set_state(RepaymentReg.items)

@router.message(RepaymentReg.items)
async def items(message: Message, state: FSMContext):
    await state.update_data(items=message.text)
    await state.set_state(RepaymentReg.gurantor)
    await message.answer('Напишите поручителя. Если поручителя нету, оставьте -')
    
@router.message(RepaymentReg.gurantor)
async def gurantor(message: Message, state: FSMContext):
    await state.update_data(gurantor=message.text)
    await state.set_state(RepaymentReg.requisites)
    await message.answer('Отправьте реквизиты (номер карты, реквизиты для пополнения через ЕРИП)')

@router.message(RepaymentReg.requisites)
async def requeisites(message: Message, state: FSMContext):
    await state.update_data(requisites=message.text)
    await state.set_state(RepaymentReg.photos)
    await message.answer('Отправьте фото чеков')
    
@router.message(RepaymentReg.photos)
async def gurantor(message: Message, state: FSMContext, album: List[Message] = []):
    #как же уёбищно тг обрабатывает альбомы, это просто невыносимо, я в шоке, что такое вообще сделали. я просто в ахуе
    if len(album) == 0:
        await message.answer("Вы не отправили фотографии. Отправьте фотографии")
        return
    for element in album:
        if not element.photo:
            await message.answer("Вы отправили что-то, но не фото (возможно фото как файл). Отправьте фото как фото")
            return
    await state.update_data(album=album)
    data = await state.get_data()
    username = message.from_user.username
    await message.answer(f'Ваш запрос на возврат средств:\nВаш тег: @{username}\nПредметы: {data["items"]}\nПоручитель: {data["gurantor"]}\nРеквизиты: {data["requisites"]}', reply_markup=kb.user_confirm_repayment)
    
@router.callback_query(F.data == 'user_confirmed_repayment')
async def user_confirmed_repayment(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    request_data = 'З'+ callback.message.text[5:]
    data = await state.get_data()
    user_id = callback.message.chat.id
    await callback.message.edit_text(f'Ваш запрос на возврат средств за {data["items"]} принят на рассмотрение.')
    await callback.message.answer('Главное меню', reply_markup= await kb.main_keyboard(user_id))
    photo_ids =[]
    for element in data["album"]:
        photo_ids.append(element.photo[-1].file_id)
    
    await rq.set_request(text=request_data, tg_id=user_id, photo_ids=photo_ids)
    request_id = await rq.get_request_id(request_data)
    admins = await rq.get_exemption_admins()
    group_elements =[InputMediaPhoto(media=photo_ids[0], caption=request_data)]
    for photo_id in photo_ids[:1]:
        group_elements.append(InputMediaPhoto(media=photo_id))
    
    for admin in admins:
            await bot.send_media_group(admin, group_elements)
            await bot.send_message(f"Запрос на возврат средств за {data["items"]}", reply_markup=kb.admin_handle_request)
        
@router.callback_query(F.data == "user_cancel_repayment")
async def user_cancel_exemption(callback: CallbackQuery, state: FSMContext):
    state.clear()
    await callback.message.edit_text('Вы отменили запрос')
    await callback.message.answer('Главное меню', reply_markup= await kb.main_keyboard(callback.message.chat.id))

#хендлеры одобрения/отказа

@router.callback_query(F.data == "approve_request")
async def approve_request(callback: CallbackQuery):
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
            await bot.send_message(user_id, f'Ваш запрос на {request_date} одобрен и передан секретарям', reply_markup= await kb.main_keyboard(user_id))
        else:
            pass 
        request_data = "Одобрен з" + request_data[1:]
        secretaries = await rq.get_secretaries()
        for secretary in secretaries:
            await bot.send_message(secretary, request_data)
        await rq.set_request_approved(request_id)
    elif request_status == "Approved" or "Declined":
        await callback.message.edit_text('Запрос уже обработан')
    else:
        await callback.message.edit_text('Обратитесь за поддержкой в IT-отдел')

@router.callback_query(F.data == "decline_request")
async def approve_request(callback: CallbackQuery):
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
            await bot.send_message(user_id, f'Ваш запрос на {request_date} отказан', reply_markup= await kb.main_keyboard(user_id))
        else:
            pass #сюда обработчик бюджета ебнуть надо, но я пока не придумал, как он структурируется
        await rq.set_request_declined(request_id)
    elif request_status == "Approved" or "Declined":
        await callback.message.edit_text('Запрос уже обработан')
    else:
        await callback.message.edit_text('Обратитесь за поддержкой в IT-отдел')        
