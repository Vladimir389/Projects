import asyncio
import logging
import pymysql

from aiogram import Bot,Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN, host, user, database1, password


bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Приветствую! Введите команду /help чтобы увидеть другие команды")

@dp.message(Command("add"))
async def def_help(message: Message):
    print(message.chat.id)
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=database1,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Successfully connected...")
    except Exception as e:
        print("Error connection...")
        print(e)
    try:
        with connection.cursor() as cursor:
            insert = "INSERT INTO `users` (Username, user_id) VALUES (%s, %s);"
            cursor.execute(insert, (message.chat.username, message.chat.id))
            connection.commit()
        await message.answer("Добавление данных прошло успешно")
        print("Добавление прошло успешно")
    except Exception as e:
        print(f"error {e}")
    finally:
        connection.close()
        print("successfully disabled...")

@dp.message(Command("add1"))
async def def_add(message: Message):
    try:
        with open('info_user.txt', 'a', encoding='utf-8') as file:
            user = f"\nID:{message.chat.id}, USERNAME:{message.chat.username}\n"
            file.write(user)
        await message.answer("Ваши данные успешно добавлены")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@dp.message(Command("help"))
async def def_help(message: Message):
    await message.answer("Чтобы записать ваши данные в базу данных введите /add, \
                         чтобы записать в блокнот /add1, чтобы вывести все записанные данные \
                         введите /collect")

@dp.message(Command("collect"))
async def def_collect(message: Message):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=database1,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Successfully connected...")
    except Exception as e:
        print("Error connection...")
        print(e)

    try:
        with connection.cursor() as cursor:
            collect = "SELECT * FROM users.users"
            cursor.execute(collect)
            collect_r = cursor.fetchall()
        await message.answer(str(collect_r))
    except Exception as e:
        print(f"Error {e}")
    finally:
        connection.close()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
    except Exception as e:
        print("Error: ", e)