from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
import asyncio

# 🔧 Sozlamalar
TOKEN = "8283034036:AAF7yHt_YH8OHoRCVvV0ND7zWFcD3wyuKkg"
ADMIN_ID = 7853450608
ADMIN_USERNAME = "@L_I_I_1_L"
CARD_NUMBER = "5614686835566046"

# ✅ Yangi aiogram 3.13 formatida to‘g‘rilangan
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# /start buyrug‘i
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🚀 Ishni boshlash", callback_data="start_process")],
        [types.InlineKeyboardButton(text="📞 Admin bilan bog‘lanish", url=f"https://t.me/{ADMIN_USERNAME[1:]}")]
    ])

    text = (
        "💎 <b>Assalomu alaykum!</b>\n\n"
        "Siz <b>rasmiy va ishonchli Instagram galochka olish xizmatiga</b> xush kelibsiz!\n\n"
        "Biz <b>100% halol</b> ishlaymiz — hech qanday firibgarlik yo‘q.\n"
        "To‘lov tasdiqlangach, sizning username’ingiz <b>5 daqiqa</b> ichida tekshiruvga yuboriladi.\n\n"
        "✅ <b>Ish vaqti:</b> 24/7\n"
        "✅ <b>Kafolat:</b> To‘lov bajarilmasa — pul qaytariladi\n"
        "✅ <b>Natija:</b> 5 daqiqa ichida tayyor\n\n"
        f"📞 <b>Admin:</b> {ADMIN_USERNAME}"
    )

    await message.answer(text, reply_markup=kb)


# “Ishni boshlash” bosilganda — tarif tanlash
@dp.callback_query(lambda c: c.data == "start_process")
async def choose_tariff(callback: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="🟢 1 oylik — 10 000 so‘m", callback_data="tariff_oylik"),
            types.InlineKeyboardButton(text="🔵 1 yillik — 230 000 so‘m", callback_data="tariff_yillik")
        ]
    ])
    await callback.message.answer("📦 Iltimos, kerakli tarifni tanlang:", reply_markup=kb)
    await callback.answer()


# Tarif tanlanganda
@dp.callback_query(lambda c: c.data.startswith("tariff_"))
async def show_payment(callback: types.CallbackQuery):
    if callback.data == "tariff_oylik":
        tarif_text = "🟢 <b>1 oylik</b> — 10 000 so‘m"
        tolov_text = "💸 10 000 so‘m <b>o‘tkazing</b> 👇"
    else:
        tarif_text = "🔵 <b>1 yillik</b> — 230 000 so‘m"
        tolov_text = "💸 230 000 so‘m <b>o‘tkazing</b> 👇"

    await callback.message.answer(
        f"✅ <b>Tanlangan tarif:</b> {tarif_text}\n\n"
        f"{tolov_text}\n"
        f"💳 <b>Karta raqami:</b>\n<code>{CARD_NUMBER}</code>\n\n"
        f"📸 To‘lovni amalga oshirgach, chekni shu yerga yuboring."
    )
    await callback.answer()


# ✅ Chek yuborilganda
@dp.message(lambda m: m.photo)
async def receive_check(message: types.Message):
    user = message.from_user
    caption = message.caption or "Chek yuborildi."

    info = (
        f"📩 <b>Yangi to‘lov cheki!</b>\n\n"
        f"👤 Foydalanuvchi: {user.full_name}\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"📱 Username: @{user.username if user.username else 'yo‘q'}\n\n"
        f"💬 Izoh: {caption}"
    )

    # 🔔 Admin’ga chek yuborish
    await bot.send_photo(chat_id=ADMIN_ID, photo=message.photo[-1].file_id, caption=info)

    # 🔹 Foydalanuvchiga javob
    await message.reply(
        "✅ <b>To‘lov qabul qilindi!</b>\n"
        "⏳ <b>Galochka 5 daqiqa ichida tayyor bo‘ladi.</b>\n"
        "Rahmat ishonchingiz uchun 💎"
    )


# 🔥 Botni ishga tushurish
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
