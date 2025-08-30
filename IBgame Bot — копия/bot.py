import asyncio
import logging
from mailbox import Message

from aiogram import Bot, Dispatcher,F
from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.handlers import callback_query
from aiogram.methods import DeleteWebhook
from aiogram.types import FSInputFile, InlineKeyboardButton,InlineKeyboardMarkup
from mistralai import Mistral
logging.basicConfig(level=logging.INFO)
from db.models import async_main
import db.requests as rq
ai_token='fvBIVxM6OG3TYZe3WlLCT1jusvjlNVGk'
bot=Bot(token='7507350582:AAGiTlrWCna_FRONZykDuM3BbbGy7uLCQkE')
model='mistral-small-latest'
client=Mistral(ai_token)
dp=Dispatcher()


@dp.message(CommandStart())
async def h(message: types.Message):
    hello = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='start_begin')],
        [InlineKeyboardButton(text='Нет', callback_data='mm4')],
    ])
    await message.answer('Подтвердите согласие на обработку персональных данных: tg_id и имя пользователя', reply_markup=hello)

class Form(StatesGroup):
    waiting_for_input = State()

@dp.callback_query(F.data == 'start_begin')
async def hello(callback_query: types.CallbackQuery):
    await async_main()
    await rq.set_user(callback_query.from_user.id, callback_query.from_user.first_name)
    await callback_query.message.answer(
        f'Привет, {callback_query.from_user.first_name}.\nДобро пожаловать в игру по информационной безопасности💥')
    await callback_query.message.answer(
        f'{callback_query.from_user.first_name}, Вы являетесь специалистом по информационной безопасности в крупной IT компании, Вам приходит сообщение от Вашего начальника👇')
    v = FSInputFile('foo.mp4')
    await callback_query.message.answer_video(v)
    await callback_query.message.answer(
        'Выберите этап: ',
        reply_markup=mainmenu)


mainmenu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Этап 1. Основы стеганографии', callback_data='mm1')],
    [InlineKeyboardButton(text='Этап 2. Методы социальной инженерии', callback_data='mm2')],
    [InlineKeyboardButton(text='Этап 3. Методы защиты информации', callback_data='mm3')],
    [InlineKeyboardButton(text='Завершить игру', callback_data='mm4')],
])

#Обработка нажатия кнопок главного меню
@dp.callback_query(F.data == 'mm1')
async def mm1(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        'В первую очередь стоит разобраться с утечкой конфиденциальной информации. После анализа исходящих сообщений было выявлено 3 случая отправки нехарактерной для компании информации. Проведите работу с сотрудниками, которые выполняли отправку такой информации.',
        reply_markup=bb1)

@dp.callback_query(F.data == 'mm2')
async def mm1(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        'Утечка конфиденциальной информации также может быть связана с применением методов социальной инженерии. Проанализируйте, какие методы применялись в каждом конкретном случае',
        reply_markup=bb2)

@dp.callback_query(F.data == 'mm3')
async def mm1(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        'На основе анализа существующих проблем были выявлены направления совершенствования системы защиты информации в организации.',
        reply_markup=bb3)

@dp.callback_query(F.data == 'mm4')
async def mm1(callback_query: types.CallbackQuery):
    r= await rq.give_res(callback_query.from_user.id)
    await callback_query.message.answer(f'Игра окончена!\nВаш результат {r} баллов!')







#Выбор героев на 1 этапе
bb1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Анна, менеджер отдела по работе с клиентами', callback_data='b1')],
    [InlineKeyboardButton(text='Иван, системный администратор', callback_data='b2')],
    [InlineKeyboardButton(text='Юлия, программист', callback_data='b3')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])

@dp.callback_query(F.data == 'b1')
async def b1(callback_query: types.CallbackQuery):
    f4 = FSInputFile('Анна.png')
    await callback_query.message.answer_photo(f4)
    f1 = FSInputFile('анна гс.ogg')
    await callback_query.message.answer_audio(f1)
    f2 = FSInputFile('Япония.bmp')
    await callback_query.message.answer_photo(f2, 'В изображении скрыто сообщение, найдите его', reply_markup=a)

a = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='qwerty', callback_data='c1'),
     InlineKeyboardButton(text='password', callback_data='c2'),
     InlineKeyboardButton(text='ask', callback_data='c3')],
    [InlineKeyboardButton(text='Назад',callback_data='back')]
])


@dp.callback_query(F.data == 'c1')
async def c1(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Миссия провалена! Будьте внимательны.')
    await callback_query.message.answer(
        'Перейдите к следующему этапу:',
        reply_markup=mainmenu)


@dp.callback_query(F.data == 'c2')
async def c2(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Верно, Вы справились!')
    await rq.set_ball(callback_query.from_user.id, 10, 0, 0)  # Убедитесь, что передаете правильный tg_id
    await callback_query.message.answer(
        'Перейдите к следующему этапу:',
        reply_markup=mainmenu
    )


@dp.callback_query(F.data == 'c3')
async def c3(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Миссия провалена!')
    await callback_query.message.answer(
        'Перейдите к следующему этапу:',
        reply_markup=mainmenu)

@dp.callback_query(F.data == 'back')
async def c3(callback_query: types.CallbackQuery):
    #await callback_query.message.delete()
    await callback_query.message.answer('Выбери этап',reply_markup=mainmenu)







@dp.callback_query(F.data == 'b2')
async def b2(callback_query: types.CallbackQuery):
    f6 = FSInputFile('Иван.png')
    await callback_query.message.answer_photo(f6)
    ff1 = FSInputFile('гс иван.ogg')
    await callback_query.message.answer_audio(ff1)
    await callback_query.message.answer('Файл можно скачать по ссылке')
    await callback_query.message.answer("Ссылка: https://clck.ru/3GQLYc")
    await callback_query.message.answer('Какое сообщение было передано?', reply_markup=a1)

a1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='$t@pler', callback_data='cс1'),
     InlineKeyboardButton(text='Shrimp', callback_data='cс2'),
     InlineKeyboardButton(text='P@$$word ', callback_data='cс3')],
    [InlineKeyboardButton(text='Назад',callback_data='back')]
])

@dp.callback_query(F.data == 'cс1')
async def cс1(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Миссия провалена! Будьте внимательны.')
    await callback_query.message.answer(
        'Перейдите к следующему этапу:',
        reply_markup=mainmenu)

@dp.callback_query(F.data == 'cс2')
async def cс2(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Верно, Вы справились!')
    await callback_query.message.answer('Вы получаете 10 баллов')
    await rq.set_ball(callback_query.from_user.id, 10, 0, 0)
    await callback_query.message.answer(
        'Перейдите к следующему этапу: ',
        reply_markup=mainmenu)

@dp.callback_query(F.data == 'cс3')
async def cс3(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Миссия провалена!')
    await callback_query.message.answer(
        'Перейдите к следующему этапу: ',
        reply_markup=mainmenu)








@dp.callback_query(F.data == 'b3')
async def b3(callback_query: types.CallbackQuery):
    f5 = FSInputFile('Юлия.png')
    await callback_query.message.answer_photo(f5)
    ff2 = FSInputFile('гс юлия.ogg')
    await callback_query.message.answer_audio(ff2)
    await callback_query.message.answer('Отправляю вам ссылку на скачивание файлов проекта сайта')
    await callback_query.message.answer("Ссылка: https://clck.ru/3GQMeC")
    await callback_query.message.answer('Какое сообщение было передано?', reply_markup=a2)
a2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Кит', callback_data='cсс1'),
     InlineKeyboardButton(text='Ком', callback_data='cсс2'),
     InlineKeyboardButton(text='Кот', callback_data='cсс3')],
    [InlineKeyboardButton(text='Назад',callback_data='back')]
])

@dp.callback_query(F.data == 'cсс1')
async def cсс1(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Миссия провалена!')
    await callback_query.message.answer(
        'Перейдите к следующему этапу: ',
        reply_markup=mainmenu)

@dp.callback_query(F.data == 'cсс2')
async def cсс2(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Верно, Вы справились!')
    await rq.set_ball(callback_query.from_user.id, 10, 0, 0)
    await callback_query.message.answer(
        'Перейдите к следующему этапу: ',
        reply_markup=mainmenu)

@dp.callback_query(F.data == 'cсс3')
async def cсс3(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Миссия провалена!')
    await callback_query.message.answer(
        'Перейдите к следующему этапу: ',
        reply_markup=mainmenu)







#Выбор героев на 2 этапе
bb2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Дарья, бухгалтер', callback_data='b21')],
    [InlineKeyboardButton(text='Александр, менеджер-стажер', callback_data='b22')],
    [InlineKeyboardButton(text='Анастасия, секретарь', callback_data='b23')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]

])

@dp.callback_query(F.data == 'b21')
async def b21(callback_query: types.CallbackQuery):
    f4 = FSInputFile('Дарья.jpg')
    await callback_query.message.answer_photo(f4)
    await callback_query.message.answer('Определите, какой это метод социальной инженерии?',reply_markup=dasha_b21)

dasha_b21=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фишинг', callback_data='fishing'),
     InlineKeyboardButton(text='Тайпсквоттинг', callback_data='taip'),
     InlineKeyboardButton(text='Крэкинг', callback_data='kraking')],
     [InlineKeyboardButton(text='Назад', callback_data='back')]
])
@dp.callback_query(F.data == 'fishing')
async def fishing(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Верно')
    await callback_query.message.answer('Выберите следующего сотрудника',reply_markup=bb2)
    await rq.set_ball(callback_query.from_user.id, 0, 10, 0)
@dp.callback_query(F.data == 'taip')
async def taip(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('Выберите следующего сотрудника', reply_markup=bb2)
@dp.callback_query(F.data == 'kraking')
async def kraking(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('Выберите следующего сотрудника', reply_markup=bb2)

@dp.callback_query(F.data == 'b22')
async def b21(callback_query: types.CallbackQuery):
    f4 = FSInputFile('Александр.jpg')
    await callback_query.message.answer_photo(f4)
    await callback_query.message.answer('Определите, какой это метод социальной инженерии?',reply_markup=aleksandr_b22)

aleksandr_b22=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фишинг', callback_data='fishing'),
     InlineKeyboardButton(text='Кража личности', callback_data='krazha'),
     InlineKeyboardButton(text='Крэкинг', callback_data='kraking')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])
@dp.callback_query(F.data == 'fishing')
async def fishing(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('Выберите следующего сотрудника', reply_markup=bb2)
@dp.callback_query(F.data == 'krazha')
async def taip(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Верно')
    await rq.set_ball(callback_query.from_user.id, 0, 10, 0)  # Убедитесь, что передаете правильный tg_id
    await callback_query.message.answer('Выберите следующего сотрудника', reply_markup=bb2)
@dp.callback_query(F.data == 'kraking')
async def kraking(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('Выберите следующего сотрудника', reply_markup=bb2)


@dp.callback_query(F.data == 'b23')
async def b21(callback_query: types.CallbackQuery):
    f4 = FSInputFile('Анастасия.jpg')
    await callback_query.message.answer_photo(f4)
    await callback_query.message.answer('Определите, какой это метод социальной инженерии?',reply_markup=anastasia_b23)

anastasia_b23=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фишинг', callback_data='fish'),
     InlineKeyboardButton(text='Тайпсквоттинг', callback_data='taips'),
     InlineKeyboardButton(text='Крэкинг', callback_data='krakin')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])
@dp.callback_query(F.data == 'fish')
async def fishing(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('Перейдите к следующему этапу',reply_markup=mainmenu)
@dp.callback_query(F.data == 'taips')
async def taip(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Верно')
    await rq.set_ball(callback_query.from_user.id, 0, 10, 0)  # Убедитесь, что передаете правильный tg_id
    await callback_query.message.answer('Перейдите к следующему этапу',reply_markup=mainmenu)
@dp.callback_query(F.data == 'krakin')
async def kraking(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('Перейдите к следующему этапу',reply_markup=mainmenu)










#Выбор героев на 3 этапе
bb3 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Политика разграничения доступа', callback_data='b31')],
    [InlineKeyboardButton(text='Система аутентификации', callback_data='b32')],
    [InlineKeyboardButton(text='Защита от утечки конфиденциальной информации', callback_data='b33')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])


@dp.callback_query(F.data == 'b31')
async def pol(callback_query: types.CallbackQuery):
    await callback_query.message.answer('При работе с данными важно, чтобы у каждой группы сотрудников был свой набор прав доступа к различным объектам. При этом сотрудники одного отдела не должны иметь доступ к данным другого отдела.')
    await  callback_query.message.answer('Какая это модель разграничения доступа?',reply_markup=polb31)
polb31=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Дискреционная',callback_data='disk'),
     InlineKeyboardButton(text='Ролевая',callback_data='rol'),
     InlineKeyboardButton(text='Мандатная',callback_data='mand')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])
@dp.callback_query(F.data == 'disk')
async def pol1(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer( 'Выбери следующий шаг',reply_markup=bb3)
@dp.callback_query(F.data == 'mand')
async def pol2(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('Выбери следующий шаг', reply_markup=bb3)
@dp.callback_query(F.data == 'rol')
async def pol3(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Верно')
    await rq.set_ball(callback_query.from_user.id, 0, 0, 10)  # Убедитесь, что передаете правильный tg_id
    await callback_query.message.answer('Выбери следующий шаг', reply_markup=bb3)





@dp.callback_query(F.data == 'b32')
async def sist(callback_query: types.CallbackQuery):
    await callback_query.message.answer('При организации пропускного режима было решено использовать биометрические данные, какой способ аутентификации будут использоваться')
    await  callback_query.message.answer('Какая это способ аутентификации?',reply_markup=sistb32)
sistb32=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Я знаю',callback_data='know'),
     InlineKeyboardButton(text='Я владею',callback_data='have'),
     InlineKeyboardButton(text='Я есть',callback_data='eat')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])

@dp.callback_query(F.data == 'know')
async def know(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('Выбери следующий шаг', reply_markup=bb3)
@dp.callback_query(F.data == 'have')
async def have(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('Выбери следующий шаг', reply_markup=bb3)
@dp.callback_query(F.data == 'eat')
async def eat(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Верно')
    await rq.set_ball(callback_query.from_user.id, 0, 0, 10)  # Убедитесь, что передаете правильный tg_id
    await callback_query.message.answer('Выбери следующий шаг', reply_markup=bb3)















@dp.callback_query(F.data == 'b33')
async def pol3(callback_query: types.CallbackQuery):
    await callback_query.message.answer('В компании было принято использовать систему предотвращения утечек информации (DLP-система), которая предназначена для защиты от угроз:\n1.Перехвата информации по побочным каналам \n2.Несанкционированного доступа нарушителя к защищаемой системе и её ресурсам\n3.Передачи или копирования легальными пользователями секретной информации за пределы защищаемой системы')
    await callback_query.message.answer('Выбери верный ответ',reply_markup=pol3b33)

pol3b33=InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1',callback_data='one'),
     InlineKeyboardButton(text='2',callback_data='two'),
     InlineKeyboardButton(text='3',callback_data='three')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])

@dp.callback_query(F.data == 'one')
async def two(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('THE END\nВаш результат оценит Юлия Александровна и поставит оценку в журнал')

@dp.callback_query(F.data == 'two')
async def two(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Неверно')
    await callback_query.message.answer('THE END\nВаш результат оценит Юлия Александровна и поставит оценку в журнал')
@dp.callback_query(F.data == 'three')
async def three(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Верно')
    await rq.set_ball(callback_query.from_user.id, 0, 0, 10)  # Убедитесь, что передаете правильный tg_id
    await callback_query.message.answer('THE END\nВаш результат оценит Юлия Александровна и поставит оценку в журнал')


@dp.message()
async def message_handler(msg:Message):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                'role': 'system',
                'content': '',
            },
            {
                'role': 'user',
                'content': msg.text,
            },
        ]
    )


    await bot.send_message(msg.chat.id,chat_response.choices[0].message.content,parse_mode='Markdown')





async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')