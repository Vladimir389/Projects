import asyncio
import logging
import pymysql
from contextlib import asynccontextmanager

from aiogram import Bot,Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,BufferedInputFile

from config import TOKEN, host, user, database1, password, photo_path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Приветствую {message.from_user.first_name}! Введите команду /help чтобы увидеть другие команды")

@asynccontextmanager
async def get_db_connection():
    connection = None
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=database1,
            cursorclass=pymysql.cursors.DictCursor
        )
        logger.info("Successfully connected to database")
        yield connection
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if connection:
            connection.close()
            logger.info("Database connection closed")

@dp.message(Command("add"))
async def def_help(message: Message):
    print(message.chat.id)
    async with get_db_connection() as connection:
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
    await message.answer("Список команд: \n \
                         /add - Добавляет данные о пользователе в Базу данных\n \
                         /add1 - Добавляет данные о пользователе в файл txt\n  \
                         /collect - Выводит все данный из базы данных \n \
                         /sms - Запускает рассылку всем пользователям из базы данных\n \
                         /id - Выводит ваше имя")

@dp.message(Command("collect"))
async def def_collect(message: Message):
    async with get_db_connection() as connection:
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
            print("successfully disabled...")

@dp.message(Command("sms"))
async def sms(message: Message):
    async with get_db_connection() as connection:        
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id FROM users")
            results = cursor.fetchall()
            try:
                user_ids = [row['user_id'] for row in results]
                
                with open(photo_path, 'rb') as file:
                    photo_bytes = file.read()
                
                photo = BufferedInputFile(photo_bytes, filename="image.jpg")
                
                for user_id in user_ids:
                    try:
                        await bot.send_photo(
                            chat_id=user_id,
                            photo=photo,  # Передаем BufferedInputFile
                            caption="Ваше фото"
                        )
                    except Exception as e:
                        print(f"Ошибка отправки пользователю {user_id}: {e}")
                
                    await message.answer("Рассылка завершена")
                return user_ids
            except Exception as e:
                print(e)
                

@dp.message(Command("id"))
async def def_id(message: Message):
    await message.answer(message.from_user.full_name)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
    except Exception as e:
        print("Error: ", e)

