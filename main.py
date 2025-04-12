import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

# Вставь свой токен здесь
API_TOKEN = '7925011476:AAEHrn0QkfwwBUTL4xz0HGP3j57S07d1whU'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Состояния


class TrialLessonFSM(StatesGroup):
    goal = State()
    level = State()
    age = State()
    teacher_pref = State()
    format_pref = State()
    time = State()


# Кнопки
start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(KeyboardButton("Записаться на пробное занятие"))


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Здравствуйте! Я виртуальный администратор школы английского языка. Чем могу помочь?", reply_markup=start_kb)


@dp.message_handler(lambda message: message.text == "Записаться на пробное занятие")
async def book_trial(message: types.Message):
    await TrialLessonFSM.goal.set()
    await message.answer("Расскажите, пожалуйста, зачем вам нужен английский? Работа, учёба, путешествия?")


@dp.message_handler(state=TrialLessonFSM.goal)
async def process_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await TrialLessonFSM.level.set()
    await message.answer("Какой у вас уровень английского? (Начальный, Средний, Продвинутый)")


@dp.message_handler(state=TrialLessonFSM.level)
async def process_level(message: types.Message, state: FSMContext):
    await state.update_data(level=message.text)
    await TrialLessonFSM.age.set()
    await message.answer("Сколько вам лет?")


@dp.message_handler(state=TrialLessonFSM.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await TrialLessonFSM.teacher_pref.set()
    await message.answer("Вы предпочитаете преподавателя-русскоязычного/казахоязычного или носителя языка?")


@dp.message_handler(state=TrialLessonFSM.teacher_pref)
async def process_teacher(message: types.Message, state: FSMContext):
    await state.update_data(teacher=message.text)
    await TrialLessonFSM.format_pref.set()
    await message.answer("Удобнее заниматься онлайн или офлайн?")


@dp.message_handler(state=TrialLessonFSM.format_pref)
async def process_format(message: types.Message, state: FSMContext):
    await state.update_data(format=message.text)
    await TrialLessonFSM.time.set()
    await message.answer("Когда вам удобно пройти пробный урок? (утро, день, вечер; будни или выходные?)")


@dp.message_handler(state=TrialLessonFSM.time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    data = await state.get_data()

    summary = (
        f"Отлично! Вот что я записал:\n"
        f"🎯 Цель: {data['goal']}\n"
        f"📚 Уровень: {data['level']}\n"
        f"🎂 Возраст: {data['age']}\n"
        f"👩‍🏫 Преподаватель: {data['teacher']}\n"
        f"💻 Формат: {data['format']}\n"
        f"🕒 Время: {data['time']}\n\n"
        f"Мы подберём для вас преподавателя и свяжемся для подтверждения записи. До встречи на уроке! 😊"
    )

    await message.answer(summary)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
