from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

import app.keyboards as kb
from bot import bot
import app.database.request as rq

router = Router()


class Admin(StatesGroup):
    fio = State()
    username = State()


class Responsible_release(StatesGroup):
    fio = State()
    username = State()


class Responsible_budget(StatesGroup):
    fio = State()
    username = State()


class Secretary(StatesGroup):
    fio = State()
    username = State()


class Responsible_release_delete(StatesGroup):
    username = State()


class Responsible_budget_delete(StatesGroup):
    username = State()



class Secretary_delete(StatesGroup):
    username = State()


class Release_text(StatesGroup):
    text = State()


class Release(StatesGroup):
    username = State()
    fio = State()
    course = State()
    group = State()
    date = State()
    reason = State()


class Return_Budget(StatesGroup):
    username = State()
    fio = State()
    reason = State()
    quantity = State()
    send = State()
    album = State()


class Request_Budget(StatesGroup):
    username = State()
    fio = State()
    date = State()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Добро пожаловать в бот запросов', reply_markup=kb.start)
    await rq.set_user(message.from_user.id, message.from_user.username)


@router.message(Command('admin'))
async def admin(message: Message, state: FSMContext):
    if message.from_user.id == 802188377:
        await message.answer('Введите ФИО админа')
        await state.set_state(Admin.fio)


@router.message(Admin.fio)
async def admin_username(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(Admin.username)
    await message.answer('Введите тег админа')


@router.message(Admin.username)
async def admin_final(message: Message, state: FSMContext):
    await state.update_data(username=message.text.split('@')[1])
    data = await state.get_data()
    user_tg_id = await rq.find_user(data["username"])
    await message.answer('Админ создан', reply_markup=kb.to_main)
    await rq.set_admin(data["fio"], user_tg_id)
    await state.clear()


@router.message(Command('create'))
async def creat(message: Message):
    admins = await rq.get_admins()
    if message.from_user.id in admins:
        await message.answer('Кого вы хотите создать?', reply_markup=kb.create)
    else:
        await message.answer('У вас нет доступа')


@router.callback_query(F.data == 'a_release')
async def a_release(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали создание ответсвенного за освобождение')
    await state.set_state(Responsible_release.fio)
    await callback.message.answer('Введите ФИО ответственного')


@router.message(Responsible_release.fio)
async def tg_id_release(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(Responsible_release.username)
    await message.answer('Введите тег ответственного')


@router.message(Responsible_release.username)
async def release_final(message: Message, state: FSMContext):
    await state.update_data(username=message.text.split('@')[1])
    data = await state.get_data()
    user_tg_id = await rq.find_user(data["username"])
    await message.answer('Отвественный создан', reply_markup=kb.to_main)
    await rq.set_release_admin(data["fio"], user_tg_id)
    await state.clear()


@router.callback_query(F.data == 'a_budget')
async def a_budget(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали создание ответственного за бюджет')
    await state.set_state(Responsible_budget.fio)
    await callback.message.answer('Введите ФИО ответственного')


@router.message(Responsible_budget.fio)
async def tg_id_budget(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(Responsible_budget.username)
    await message.answer('Введите тег ответственного')


@router.message(Responsible_budget.username)
async def budget_final(message: Message, state: FSMContext):
    await state.update_data(username=message.text.split('@')[1])
    data = await state.get_data()
    user_tg_id = await rq.find_user(data["username"])
    await message.answer('Отвественный создан', reply_markup=kb.to_main)
    await rq.set_budget_admin(data["fio"], user_tg_id)
    await state.clear()


@router.callback_query(F.data == 'a_secretary')
async def a_secretary(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали создание секретаря')
    await state.set_state(Secretary.fio)
    await callback.message.answer('Введите ФИО секретаря')


@router.message(Secretary.fio)
async def tg_id_secretary(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(Secretary.username)
    await message.answer('Введите тег секретаря')


@router.message(Secretary.username)
async def secretary_final(message: Message, state: FSMContext):
    await state.update_data(username=message.text.split('@')[1])
    data = await state.get_data()
    user_tg_id = await rq.find_user(data["username"])
    await message.answer('Секретарь создан', reply_markup=kb.to_main)
    await rq.set_secretary(data["fio"], user_tg_id)
    await state.clear()


@router.message(Command('delete'))
async def delete(message: Message):
    admins = await rq.get_admins()
    if message.from_user.id in admins:
        await message.answer('Кого вы хотите удалить?', reply_markup=kb.delete)
    else:
        await message.answer('У вас нет доступа')


@router.callback_query(F.data == 'd_release')
async def d_release(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали удаление ответсвенного за освобождение')
    await state.set_state(Responsible_release_delete.username)
    await callback.message.answer('Введите тег ответственного')


@router.message(Responsible_release_delete.username)
async def release_delete_final(message: Message, state: FSMContext):
    username = message.text.split('@')[1]
    user_tg_id = await rq.find_user(username)
    await rq.delete_release_admin(user_tg_id)
    await message.answer('Отвественный удалён', reply_markup=kb.to_main)
    await state.clear()


@router.callback_query(F.data == 'd_budget')
async def d_budget(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали удаление ответственного за бюджет')
    await state.set_state(Responsible_budget_delete.username)
    await callback.message.answer('Введите тег ответственного')


@router.message(Responsible_budget_delete.username)
async def budget_delete_final(message: Message, state: FSMContext):
    username = message.text.split('@')[1]
    user_tg_id = await rq.find_user(username)
    await rq.delete_budget_admin(user_tg_id)
    await message.answer('Отвественный удалён', reply_markup=kb.to_main)
    await state.clear()



@router.callback_query(F.data == 'd_secretary')
async def d_secretary(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали удаление секретаря')
    await state.set_state(Secretary_delete.username)
    await callback.message.answer('Введите тег секретаря')


@router.message(Secretary_delete.username)
async def secretary_delete_final(message: Message, state: FSMContext):
    username = message.text.split('@')[1]
    user_tg_id = await rq.find_user(username)
    await rq.delete_secretary(user_tg_id)
    await message.answer('Секретарь удалён', reply_markup=kb.to_main)
    await state.clear()


@router.message(F.text == 'На главную')
async def main_2(message: Message):
    await message.answer('Выберете запрос', reply_markup=kb.request)


@router.callback_query(F.data == 'to_main')
async def main(callback: CallbackQuery):
    await callback.answer('Вы перемещены на главную страницу')
    await callback.message.answer('Выберете запрос', reply_markup=kb.request)


@router.callback_query(F.data == 'creators')
async def creators(callback: CallbackQuery):
    await callback.answer('Создатели бота')
    await callback.message.answer('Создатели бота', reply_markup=kb.creators)


@router.callback_query(F.data == 'release')
async def release(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Напишите своё ФИО')
    await state.set_state(Release.fio)


@router.message(Release.fio)
async def course(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(Release.course)
    await message.answer('Напишите свой курс')


@router.message(Release.course)
async def group(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await state.set_state(Release.group)
    await message.answer('Напишите свою группу')


@router.message(Release.group)
async def group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(Release.date)
    await message.answer('Напишите дату и время')


@router.message(Release.date)
async def date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(Release.username)
    await state.update_data(username=message.from_user.username)
    await state.set_state(Release.reason)
    await message.answer('Напишите причину')


@router.message(Release.reason)
async def reason(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_id = message.from_user.id
    await message.answer(f'Ваш запрос на освобождение:\nФИО: {data["fio"]}\nВаш тег: @{data['username']}\nКурс: {data["course"]}\nГруппа: {data["group"]}\nДата и время: {data["date"]}\nПричина: {message.text}',
                         reply_markup=kb.accept_release)
    await state.clear()


@router.callback_query(F.data == 'to_budget')
async def budget(callback: CallbackQuery):
    await callback.answer('Вы перемещены к бюджету')
    await callback.message.answer(text='Что бы вы хотели?', reply_markup=kb.budget)


@router.callback_query(F.data == 'return_budget')
async def return_budget(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали запрос на возврат денег')
    await state.set_state(Return_Budget.fio)
    await callback.message.answer('Введите своё ФИО')


@router.message(Return_Budget.fio)
async def fio_budget(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(Return_Budget.reason)
    await message.answer('Напишите причину')


@router.message(Return_Budget.reason)
async def reason_budget(message: Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await state.set_state(Return_Budget.quantity)
    await message.answer('Напишите количество денег для возвращения')


@router.message(Return_Budget.quantity)
async def quantity_budget(message: Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await state.set_state(Return_Budget.send)
    await message.answer('Введите куда прислать(номер карты или ерип с банком)')


@router.message(Return_Budget.send)
async def send_budget(message: Message, state: FSMContext):
    await state.update_data(send=message.text)
    await state.set_state(Return_Budget.username)
    await state.update_data(username=message.from_user.username)
    await state.set_state(Return_Budget.album)
    await message.answer('Пришлите фото чека(только одно)')


@router.message(Return_Budget.album)
async def photo_budget(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer('Пожалуйста, пришлите фото чека.')
        return
    data = await state.get_data()
    photo = message.photo[-1].file_id
    await state.update_data(album=photo)
    await message.answer(f'Ваш запрос на возврат:\nФИО: {data["fio"]}\nВаш тег: @{data['username']}\nПричина: {data["reason"]}\nКоличество: {data["quantity"]}\nКуда: {data["send"]}', reply_markup=kb.accept_budget)
    await message.answer_photo(photo)


@router.callback_query(F.data == 'request_budget')
async def request_budget(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Вы выбрали запрос на данные о бюджете')
    await state.set_state(Request_Budget.fio)
    await callback.message.answer('Введите своё ФИО')


@router.message(Request_Budget.fio)
async def fio_budget(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await state.set_state(Request_Budget.username)
    await state.update_data(username=message.from_user.username)
    await state.set_state(Request_Budget.date)
    await message.answer('Введите промежуток времени')


@router.message(Request_Budget.date)
async def date_budget(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    await message.answer(f'Ваш запрос бюджета:\nФИО: {data['fio']}\nВаш тег: @{data['username']}\nДата: {data['date']}', reply_markup=kb.accept_budget_date)
    await state.clear()



@router.callback_query(F.data == "accept_release")
async def process_accept_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Ваш запрос принят')
    user_id = callback.message.chat.id
    data = callback.message.text
    await state.set_state(Release_text.text)
    await state.update_data(text=data)
    await rq.set_request(data)
    id_request = await rq.get_request_id(data)
    admins = await rq.get_release_admins()
    for admin in admins:
        await bot.send_message(admin, data, reply_markup=kb.admin_accept_r(user_id, id_request))


@router.callback_query(F.data == "accept_budget")
async def process_accept_button(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Ваш запрос принят')
    user_id = callback.message.chat.id
    data = callback.message.text
    dt = await state.get_data()
    photo = dt['album']
    await rq.set_request(data)
    id_request = await rq.get_request_id(data)
    admins = await rq.get_budget_admins()
    for admin in admins:
        await bot.send_message(admin, data, reply_markup=kb.admin_accept(user_id, id_request))
        await bot.send_photo(admin, photo)
    await state.clear()


@router.callback_query(F.data == "accept_budget_date")
async def process_accept_button(callback: CallbackQuery):
    await callback.answer('Ваш запрос принят')
    user_id = callback.message.chat.id
    data = callback.message.text
    await rq.set_request(data)
    id_request = await rq.get_request_id(data)
    admins = await rq.get_budget_admins()
    for admin in admins:
        await bot.send_message(admin, data, reply_markup=kb.admin_accept(user_id, id_request))



@router.callback_query(F.data.contains('accept_admin_r'))
async def accept_admin_r(callback: CallbackQuery, state: FSMContext):
    rq_id = callback.data.split(':')[2]
    if await rq.get_request_accepted(rq_id) == "False":
        await callback.answer('Вы приняли запрос')
        msg = await state.get_data()
        user_id = callback.data.split(':')[1]
        await bot.send_message(user_id, 'Ваш запрос принят', reply_markup=kb.start)
        secretaries = await rq.get_secretaries()
        for secretary in secretaries:
            await bot.send_message(secretary, msg['text'])
        await rq.set_request_accepted(rq_id)
    else:
        await callback.answer('Запрос уже обработан')


@router.callback_query(F.data.contains('accept_admin'))
async def accept_admin(callback: CallbackQuery):
    rq_id = callback.data.split(':')[2]
    if await rq.get_request_accepted(rq_id) == "False":
        await callback.answer('Вы приняли запрос')

        user_id = callback.data.split(':')[1]
        await bot.send_message(user_id, 'Ваш запрос принят', reply_markup=kb.start)
        await rq.set_request_accepted(rq_id)
    else:
        await callback.answer('Запрос уже обработан')


@router.callback_query(F.data.contains('decline_admin'))
async def decline_admin(callback: CallbackQuery):
    rq_id = callback.data.split(':')[2]
    if await rq.get_request_accepted(rq_id) == "False":
        await callback.answer('Вы отклонили запрос')

        user_id = callback.data.split(':')[1]
        await bot.send_message(user_id, 'Ваш запрос отклонён', reply_markup=kb.start)
        await rq.set_request_accepted(rq_id)
    else:
        await callback.answer('Запрос уже обработан')
