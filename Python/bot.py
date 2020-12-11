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
    waiting_for_course = State()
    waiting_for_faculty = State()
    waiting_for_group = State()



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
    await bot.send_message(callback_query.from_user.id, 'Введите курс')
    await FillInfo.waiting_for_course.set()

@dp.message_handler(state=FillInfo.waiting_for_course, content_types=types.ContentTypes.TEXT)
async def fill_faculty(message: types.Message, state: FSMContext):
    await state.update_data(chosen_course=message.text.lower())
    await FillInfo.next()
    await message.answer("Теперь введите факультет")


@dp.message_handler(state=FillInfo.waiting_for_faculty, content_types=types.ContentTypes.TEXT)
async def fil_group(message: types.Message, state: FSMContext):
    await state.update_data(chosen_faculty=message.text)
    await FillInfo.next()
    await message.answer("Теперь введите номер группы")


@dp.message_handler(state=FillInfo.waiting_for_group, content_types=types.ContentTypes.TEXT)
async def show_info(message: types.Message, state: FSMContext):
    await state.update_data(chosen_group=message.text.lower())
    user_data = await state.get_data()
    await message.answer(f"Вы студент {user_data['chosen_course']}-ого курса, учитесь на факультете {user_data['chosen_faculty']}\n"
                         f"В группе {user_data['chosen_group']}")
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