import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from datetime import datetime, timedelta


API_TOKEN = '7952778498:AAFSY_hV_e_47AmMqdEU7WDs6WFyiIL_C0o'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)

# Инициализация диспетчера с использованием хранилища
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Хранение данных о пользователях
users_data = {}

# Характеристики лопат
shovels_info = {
    "Деревянная лопата": {
        "характеристика": "Простая лопата, которая позволяет собирать до 10 морковок за раз."
    },
    "Каменная лопата": {
        "характеристика": "Немного улучшенная лопата, собирает от 5 до 15 морковок."
    },
    "Железная лопата": {
        "характеристика": "Сильная лопата, соберет от 10 до 25 морковок."
    },
    "Алмазная лопата": {
        "характеристика": "Очень мощная лопата, которая соберет от 20 до 50 морковок."
    },
    "Золотая лопата": {
        "характеристика": "Самая лучшая лопата, соберет от 30 до 70 морковок."
    }
}

# Приветственное сообщение
async def send_welcome(message: types.Message):
    await message.answer("Привет, фермер! 🌾 Добро пожаловать в игру по фарму морковок! 🥕 Здесь ты можешь:\n"
                         "/farm — начать фармить морковки!\n"
                         "/inventory — посмотреть инвентарь !\n"
                         "/shop — магазин улучшений!\n"
                         "Готов к действию? Начни с команды /farm!", reply_markup=types.ReplyKeyboardRemove())

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await send_welcome(message)

# Для команды /farm
@dp.message(Command("farm"))
async def cmd_farm(message: types.Message):
    user_id = message.from_user.id
    current_time = datetime.now()

    # Если пользователя нет в данных, создаем его с дефолтными значениями
    if user_id not in users_data:
        users_data[user_id] = {
            "last_farmed": datetime.min,  # последний фарм, по умолчанию минимальное значение
            "shovel": 1,  # уровень лопаты (деревянная)
            "carrots": 0  # начальное количество морковок
        }

    # Проверим, когда пользователь последний раз фармил
    last_farmed = users_data[user_id]["last_farmed"]
    time_diff = current_time - last_farmed
    if time_diff < timedelta(hours=1):
        remaining_time = timedelta(hours=1) - time_diff
        await message.answer(f"Подожди ещё {remaining_time.seconds // 60} минут(ы), чтобы снова покопать морковки!")
        return

    # Тип лопаты и количество морковок
    shovel_level = users_data[user_id]["shovel"]
    if shovel_level == 1:
        # Деревянная лопата (1-10 морковок)
        carrots = random.randint(1, 10)
    elif shovel_level == 2:
        # Каменная лопата (5-15 морковок)
        carrots = random.randint(5, 15)
    elif shovel_level == 3:
        # Железная лопата (10-25 морковок)
        carrots = random.randint(10, 25)
    elif shovel_level == 4:
        # Алмазная лопата (20-50 морковок)
        carrots = random.randint(20, 50)
    elif shovel_level == 5:
        # Золотая лопата (30-70 морковок)
        carrots = random.randint(30, 70)
    else:
        # По умолчанию (если лопата не определена)
        carrots = 0

    # Обновляем количество морковок пользователя
    users_data[user_id]["carrots"] += carrots

    # Сохраняем данные о фарме и времени
    users_data[user_id]["last_farmed"] = current_time

    # Отправляем сообщение о результате фарма
    await message.answer(f"Ты выкопал(а) {carrots} морковок! 🥕\n"
                         f"У тебя теперь {users_data[user_id]['carrots']} морковок. 🌾\n"
                         "Теперь подожди час, чтобы снова фармить.")


# Команда /inventory
@dp.message(Command("inventory"))
async def cmd_inventory(message: types.Message):
    user_id = message.from_user.id

    # Проверяем, есть ли у пользователя данные
    if user_id not in users_data:
        await message.answer("Ты еще не начал фармить морковки. Используй команду /farm, чтобы начать!")
        return

    # Получаем информацию о пользователе
    carrots = users_data[user_id]["carrots"]
    shovel_level = users_data[user_id]["shovel"]
    shovel_name = list(shovels_info.keys())[shovel_level - 1]

    # Отправляем сообщение с информацией об инвентаре
    await message.answer(f"Твой инвентарь:\n"
                         f"Морковки: {carrots} 🥕\n"
                         f"Лопата: {shovel_name} - {shovels_info[shovel_name]['характеристика']}")


from aiogram import types

# Команда /shop
@dp.message(Command("shop"))
async def cmd_shop(message: types.Message):
    user_id = message.from_user.id

    # Если пользователя нет в данных, создаем его с дефолтными значениями
    if user_id not in users_data:
        users_data[user_id] = {
            "carrots": 0,  # Начальное количество морковок
            "shovel": 1    # Деревянная лопата (по умолчанию)
        }

    user_data = users_data[user_id]

    # Выводим сообщение о балансе
    await message.answer(f"У вас {user_data['carrots']} морковок. 💰\n"
                         "Добро пожаловать в магазин! 🛒 Здесь ты можешь купить улучшения для своей фермы.\n"
                         "Каждая лопата улучшает вашу ферму, позволяя собирать больше морковок за один раз.\n"
                         "Выберите номер лопаты, чтобы купить!\n")

    # Перечень товаров с их ценами
    shovel_list = {
        "1": {"name": "Каменная лопата🙄", "price": 15},
        "2": {"name": "Железная лопата🤗", "price": 30},
        "3": {"name": "Алмазная лопата😲", "price": 50},
        "4": {"name": "Золотая лопата😎", "price": 100},
        "5": {"name": "Кристальная лопата😍", "price": 200}
    }

    # Отправляем описание товаров с ценами
    for shovel_key, shovel_info in shovel_list.items():
        await message.answer(f"{shovel_key}. {shovel_info['name']} - {shovel_info['price']} морковок")

    # Добавляем стикеры для атмосферности
    await message.answer("Пиши номер лопаты, чтобы купить ее. ✨")
    await message.answer_sticker("CAACAgEAAxkBAAEBu5pgRWNATOSwU8ON4yzfgA-EzXaUto2AfwAC0gADoUjL6dQpEwIbH3qOGWdzZTl6g8v66K9r2HbhY_eGS7F_hQ")

# Обработчик сообщений, когда пользователь вводит номер для покупки
@dp.message()
async def handle_purchase(message: types.Message):
    user_id = message.from_user.id
    user_data = users_data.get(user_id)

    if not user_data:
        return  # Если пользователя нет в базе, выходим

    # Перечень товаров с их ценами
    shovel_list = {
        "1": {"name": "Каменная лопата", "price": 15},
        "2": {"name": "Железная лопата", "price": 30},
        "3": {"name": "Алмазная лопата", "price": 50},
        "4": {"name": "Золотая лопата", "price": 100},
        "5": {"name": "Кристальная лопата", "price": 200}
    }

    shovel_number = message.text.strip()

    # Проверяем, что введен правильный номер лопаты
    if shovel_number not in shovel_list:
        await message.answer("Пожалуйста, введите номер лопаты, чтобы купить. 😅")
        return

    shovel_info = shovel_list[shovel_number]
    price = shovel_info['price']

    # Проверяем, достаточно ли морковок для покупки
    if user_data['carrots'] < price:
        await message.answer(f"У вас недостаточно морковок для покупки {shovel_info['name']}! 😞")
        return

    # Проводим покупку
    user_data['carrots'] -= price
    user_data['shovel'] = int(shovel_number)  # Обновляем лопату

    await message.answer(f"Поздравляем! Вы купили {shovel_info['name']}! 🎉\n"
                         f"Теперь у вас {user_data['carrots']} морковок и {shovel_info['name']} в инвентаре.")



    # Отправляем описание товаров с ценами
    for shovel_key, shovel_info in shovel_list.items():
        await message.answer(f"{shovel_key}. {shovel_info['name']} - {shovel_info['price']} морковок")

    # Добавляем стикеры для атмосферности
    await message.answer("Пиши номер лопаты, чтобы купить ее. ✨")
    await message.answer_sticker("CAACAgEAAxkBAAEBu5pgRWNATOSwU8ON4yzfgA-EzXaUto2AfwAC0gADoUjL6dQpEwIbH3qOGWdzZTl6g8v66K9r2HbhY_eGS7F_hQ")


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
