import kb
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


from config import API_KEY


bot = Bot(token=API_KEY)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Привет!\nЭто приветсвенное сообщение", reply_markup=kb.inline_kb1)


#Пояснительное сообщение к заполнению расписания
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Чтобы коректно заполнить сделайт так, как указано на примере снизу\nтутутут', reply_markup=kb.inline_kb2)







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