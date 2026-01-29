# 🤖 Reja Bot - Vazifalar Boshqaruv Telegram Boti

Telegram orqali kundalik vazifalarni boshqarish uchun mo'ljallangan o'zbek tilidagi bot.

## 🌟 Xususiyatlar

- ✅ Vazifalar qo'shish va boshqarish
- 📊 Muhimlik darajasini belgilash (yuqori, o'rta, past)
- 📅 Muddatlarni belgilash
- 📋 Vazifalar ro'yxatini ko'rish
- ✨ Vazifalarni bajarilgan deb belgilash
- 📈 Shaxsiy statistikani ko'rish
- 🎯 Bugungi vazifalarni tekshirish
- 💬 Do'stona o'zbek tilidagi interfeys

## 📋 Talablar

- Python 3.8 yoki undan yuqori
- Telegram Bot Token (@BotFather dan)

## 🚀 O'rnatish

1. **Repository ni klonlash:**
```bash
cd /path/to/your/project
```

2. **Virtual muhit yaratish (tavsiya etiladi):**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# yoki
venv\Scripts\activate  # Windows
```

3. **Kerakli kutubxonalarni o'rnatish:**
```bash
pip install -r requirements.txt
```

4. **Bot tokenini sozlash:**
```bash
# .env.example faylini .env ga nusxalash
cp .env.example .env

# .env faylini tahrirlash va bot tokenini kiritish
nano .env  # yoki boshqa matn muharriri
```

`.env` faylida:
```
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

## 🎮 Ishga tushirish

```bash
python bot.py
```

## 📖 Foydalanish

### Asosiy buyruqlar:

- `/start` - Botni boshlash
- `/add` - Yangi vazifa qo'shish
- `/list` - Barcha vazifalar ro'yxati
- `/today` - Bugungi vazifalar
- `/done` - Vazifani bajarilgan deb belgilash
- `/stats` - Shaxsiy statistika
- `/help` - Yordam

### Tugmalar:

Bot qulay foydalanish uchun interaktiv tugmalarni taqdim etadi:
- ➕ Vazifa qo'shish
- 📋 Vazifalar ro'yxati
- 📅 Bugungi vazifalar
- ✅ Vazifani bajarish
- 📊 Statistika
- ❓ Yordam

## 🗂️ Fayl tuzilishi

```
Telegram bot/
│
├── bot.py              # Asosiy bot fayli
├── database.py         # Ma'lumotlar bazasi moduli
├── requirements.txt    # Python kutubxonalari
├── .env.example       # Konfiguratsiya namunasi
├── .env               # Konfiguratsiya (yaratiladi)
├── reja_bot.db        # SQLite bazasi (avtomatik yaratiladi)
└── README.md          # Ushbu fayl
```

## 🎯 Vazifa qo'shish misoli

1. "➕ Vazifa qo'shish" tugmasini bosing yoki `/add` yuboring
2. Vazifa nomini kiriting: `Dars tayyorlash`
3. Muhimlik darajasini tanlang: `🔴 Yuqori`
4. Muddatni kiriting (ixtiyoriy): `2026-01-30` yoki "⏭️ O'tkazish"
5. Vazifa qo'shildi! ✅

## 💾 Ma'lumotlar bazasi

Bot SQLite ma'lumotlar bazasidan foydalanadi. Barcha ma'lumotlar mahalliy `reja_bot.db` faylida saqlanadi.

**Jadvallar:**
- `users` - Foydalanuvchilar
- `tasks` - Vazifalar

## 🔒 Xavfsizlik

- Bot tokenini hech qachon oshkor qilmang
- `.env` faylini `.gitignore` ga qo'shing
- Repository ga yuklashdan oldin maxfiy ma'lumotlarni olib tashlang

## 🐛 Muammolarni hal qilish

**Bot ishlamayapti:**
- Bot tokenini tekshiring
- Internet ulanishini tekshiring
- Python versiyasini tekshiring (3.8+)

**Ma'lumotlar saqlanmayapti:**
- `reja_bot.db` faylini yaratish uchun ruxsat bor-yo'qligini tekshiring
- Ma'lumotlar bazasi faylini o'chirib, qayta ishga tushiring

**Kutubxonalar o'rnatilmadi:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🤝 Hissa qo'shish

Takliflar va xatoliklar haqida xabar berishingiz mumkin!

## 📝 Litsenziya

Ushbu loyiha shaxsiy va ta'lim maqsadlari uchun yaratilgan.

## 👨‍💻 Muallif

Ozodbek Tursunpulatov

## 🙏 Minnatdorchilik

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) kutubxonasi
- Telegram Bot API

---

**Omad! Muvaffaqiyatli vazifalar boshqarish! 🎉**
