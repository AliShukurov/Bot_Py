import kb
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import API_KEY
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage



storage = MemoryStorage()
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=storage)

class FillInfo(StatesGroup):
    waiting_for_monday = State()
    waiting_for_tuesday = State()
    waiting_for_wednesday = State()
    waiting_for_thursday = State()
    waiting_for_friday = State()
    waiting_for_saturday = State()



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Привет!\nЭто приветсвенное сообщение", reply_markup=kb.inline_kb1)


#Пояснительное сообщение к заполнению расписания(обработчик нажатия батон1)
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Чтобы коректно заполнить сделайт так, как указано на примере снизу\nтутутут', reply_markup=kb.inline_kb2)



#Заполнение расписания по дням 
@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Заполните для понедельника:')
    await FillInfo.waiting_for_monday.set()

@dp.message_handler(state=FillInfo.waiting_for_monday, content_types=types.ContentTypes.TEXT)
async def fill_2(message: types.Message, state: FSMContext):
    await state.update_data(chosen_monday=message.text.lower())
    await FillInfo.next()
    await message.answer("Заполните для вторника:")

@dp.message_handler(state=FillInfo.waiting_for_tuesday, content_types=types.ContentTypes.TEXT)
async def fill_3(message: types.Message, state: FSMContext):
    await state.update_data(chosen_tuesday=message.text.upper())
    await FillInfo.next()
    await message.answer("Заполните для среды:")

@dp.message_handler(state=FillInfo.waiting_for_wednesday, content_types=types.ContentTypes.TEXT)
async def fill_4(message: types.Message, state: FSMContext):
    await state.update_data(chosen_wednesday=message.text.lower())
    await FillInfo.next()
    await message.answer("Заполните для четверга:")    

@dp.message_handler(state=FillInfo.waiting_for_thursday, content_types=types.ContentTypes.TEXT)
async def fill_5(message: types.Message, state: FSMContext):
    await state.update_data(chosen_thursday=message.text.upper())
    await FillInfo.next()
    await message.answer("Заполните для пятницы:")

@dp.message_handler(state=FillInfo.waiting_for_friday, content_types=types.ContentTypes.TEXT)
async def fill_6(message: types.Message, state: FSMContext):
    await state.update_data(chosen_friday=message.text.lower())
    await FillInfo.next()
    await message.answer("Заполните для субботы:")


@dp.message_handler(state=FillInfo.waiting_for_saturday, content_types=types.ContentTypes.TEXT)
async def show_info(message: types.Message, state: FSMContext):
    await state.update_data(chosen_saturday=message.text.lower())
    user_data = await state.get_data()
    await message.answer(f"Расписание на неделю:\n    \n"
                         f"Понедельник:\n{user_data['chosen_monday']}\n   \n" 
                         f"Вторник:\n{user_data['chosen_tuesday']}\n     \n"
                         f"Среда:\n{user_data['chosen_wednesday']}\n      \n"
                         f"Четверг:\n{user_data['chosen_thursday']}\n      \n"
                         f"Пятница:\n{user_data['chosen_friday']}\n      \n"
                         f"Пятница:\n{user_data['chosen_saturday']}\n      \n")
    await state.finish()





#убираем шаблонные сообщ, вдург пригодится 
@dp.message_handler(commands=['rm'])
async def process_rm_command(message: types.Message):
    await message.reply("Убираем шаблоны сообщений", reply_markup=kb.ReplyKeyboardRemove())

#Ответ на некоректные сообщения и картинки 
@dp.message_handler(content_types=types.ContentTypes.ANY, state="*")
async def all_other_messages(message: types.Message):
    if message.content_type == "text":
        await message.reply("Ничего не понимаю!")
    else:
        await message.reply("Этот бот принимает только текстовые сообщения!")



if __name__ == '__main__':
    executor.start_polling(dp)