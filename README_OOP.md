# 🤖 Reja Bot - OOP strukturali versiya

To'liq qayta ishlangan OOP (Object-Oriented Programming) tamoyiliga asoslangan Telegram bot.

## 📂 Fayl tuzilishi

```
Telegram bot/
│
├── bot.py              # Asosiy bot klassi va entry point
├── config.py           # Konfiguratsiya sozlamalari
├── database.py         # Ma'lumotlar bazasi klassi
├── handlers.py         # Bot handlerlar klassi
├── keyboards.py        # Telegram klaviaturalari
├── messages.py         # Bot xabarlari va matnlari
│
├── .env                # Muhit o'zgaruvchilari
├── .env.example        # Konfiguratsiya namunasi
├── requirements.txt    # Python kutubxonalari
├── .gitignore          # Git ignore
└── README.md           # Dokumentatsiya
```

## 🏗️ Arxitektura

### 1. **bot.py** - Asosiy fayl
- `RejaBot` klassi - botni boshqarish
- Handlerlarni sozlash
- Botni ishga tushirish

### 2. **config.py** - Konfiguratsiya
- `Config` klassi - barcha sozlamalar
- Environment variables bilan ishlash
- Bot tokeni, DB nomi, Debug rejimi

### 3. **database.py** - Ma'lumotlar bazasi
- `Database` klassi - SQLite bilan ishlash
- CRUD operatsiyalari
- Foydalanuvchilar va vazifalar

### 4. **handlers.py** - Handlerlar
- `BotHandlers` klassi - barcha buyruqlar
- Conversation handlerlar
- Xabarlarni qayta ishlash

### 5. **keyboards.py** - Klaviaturalar
- `Keyboards` klassi - barcha tugmalar
- Asosiy, muhimlik, bekor qilish tugmalari

### 6. **messages.py** - Xabarlar
- `Messages` klassi - barcha matnlar
- Xush kelibsiz, yordam, xato xabarlari
- Dinamik xabarlar yaratish

## 🚀 Ishga tushirish

```bash
cd "/Users/ozodbek_tursunpulatov/Desktop/Python/Telegram bot"
source venv/bin/activate
python bot.py
```

## 🎯 OOP afzalliklari

✅ **Modullik** - har bir funksiya alohida faylda
✅ **Qayta ishlatish** - klasslarni oson qayta ishlatish mumkin
✅ **Tushunarlilik** - kod toza va tushunarli
✅ **Kengaytirish** - yangi funksiyalar qo'shish oson
✅ **Test qilish** - har bir klassni alohida test qilish
✅ **Xatoliklarni topish** - muammolarni tezda topish

## 📋 Klasslar diagrammasi

```
RejaBot
  ├── Config (konfiguratsiya)
  ├── BotHandlers
  │     ├── Database (ma'lumotlar bazasi)
  │     ├── Keyboards (tugmalar)
  │     └── Messages (xabarlar)
  └── Application (telegram bot)
```

## 🔧 Yangi funksiya qo'shish

1. **Handler qo'shish** - `handlers.py` ga yangi metod
2. **Xabar qo'shish** - `messages.py` ga yangi matn
3. **Klaviatura qo'shish** - `keyboards.py` ga yangi tugma
4. **Sozlama qo'shish** - `config.py` ga yangi o'zgaruvchi
5. **Handler ulash** - `bot.py` da `setup_handlers()` ga qo'shish

## 💡 Misol: Yangi buyruq qo'shish

```python
# handlers.py ga qo'shing:
async def my_new_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yangi buyruq!")

# bot.py da setup_handlers() ga qo'shing:
self.application.add_handler(CommandHandler('new', self.handlers.my_new_command))
```

## 🎓 O'rganish uchun

- `config.py` - sodda konfiguratsiya klassi
- `keyboards.py` - statik metodlar bilan ishlash
- `messages.py` - dinamik xabarlar yaratish
- `handlers.py` - async metodlar va conversation
- `bot.py` - klasslarni birlashtirish

---

**Muvaffaqiyatlar! Bot to'liq OOP strukturasida ishlayapti! 🎉**
