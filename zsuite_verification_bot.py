import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

# Load token securely from .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Allowed link format
EXPECTED_PREFIX = "https://affiliate.zsuitepay.net/affiliates/signup.php?a_aid="

# Handle /start command
@dp.message(Command("start"))
async def start_verification(message: Message):
    await message.answer(
        "👋 Welcome! Please verify your Brand Partner status.\nSend your referral link below:"
    )

# Handle Brand Partner link submission
@dp.message()
async def verify_link(message: Message):
    user_input = message.text.strip()
    
    # Check if input starts with the expected identifier
    if user_input.startswith(EXPECTED_PREFIX):
        await message.answer("✅ Link verified! Now, please confirm you're human by clicking below.")

        # Send an inline button for human verification
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Verify Me", callback_data="human_verified")]
        ])

        await message.answer("Click the button below to continue:", reply_markup=keyboard)
    else:
        await message.answer("🚫 Invalid link! Please provide a valid Brand Partner link.")

# Handle human verification button click
# @dp.callback_query(lambda c: c.data == "human_verified")
# async def complete_verification(callback_query: CallbackQuery):
#     user_id = callback_query.from_user.id
#     await callback_query.answer("✅ Verification complete! Welcome aboard.")
#     await bot.send_message(user_id, "🎉 Congratulations! You are now a verified Brand Partner.")

@dp.callback_query(lambda c: c.data == "human_verified")
async def complete_verification(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    telegram_group_link = "https://t.me/+fVVtOB6QjrNmZTFh"  # Replace with your actual group link

    # Create an inline button to redirect users
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Go to Main Page", url=telegram_group_link)]
    ])

    # Notify the user and provide the redirect button
    await callback_query.answer("✅ Verification complete! Welcome aboard.")
    await bot.send_message(user_id, "🎉 Congratulations! You are now a verified Brand Partner.\nClick below to proceed:", reply_markup=keyboard)


# Bot startup message
async def on_startup():
    logging.info("✅ Bot is online and running!")

# Main function to start polling
async def main():
    logging.basicConfig(level=logging.INFO)
    await on_startup()
    await dp.start_polling(bot)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
