# Serverda botni ishga tushirish bo'yicha qo'llanma

## 🚨 Serverda ishlamasligi sabablari:

### 1. **Bot tokeni noto'g'ri yoki yo'q**
```bash
# .env faylini tekshiring
cat .env
# BOT_TOKEN to'g'ri ekanligini tasdiqlang
```

### 2. **Python versiyasi mos emas**
```bash
# Python versiyasini tekshiring
python3 --version
# Talab: Python 3.8+
```

### 3. **Kutubxonalar o'rnatilmagan**
```bash
# Virtual environment yaratish
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows

# Kutubxonalarni o'rnatish
pip install -r requirements.txt
```

### 4. **Port yoki firewall muammosi**
```bash
# Bot polling rejimida ishlaydi, port kerak emas
# Lekin internet ulanishi kerak
ping api.telegram.org
```

### 5. **.env fayli yo'q**
```bash
# .env.example dan nusxa oling
cp .env.example .env
nano .env  # tokenni kiriting
```

### 6. **SQLite xatoligi**
```bash
# Database yaratish uchun yozish huquqi kerak
chmod 755 .
# yoki
mkdir -p data
# va database.py da yo'lni o'zgartiring
```

## ✅ To'g'ri o'rnatish tartibi:

### Linux/Ubuntu serverda:

```bash
# 1. Repository ni clone qiling
git clone https://github.com/OzodbekmeW/Telegram-bot.git
cd Telegram-bot

# 2. Python va pip o'rnatish
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# 3. Virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Kutubxonalarni o'rnatish
pip install --upgrade pip
pip install -r requirements.txt

# 5. .env faylini sozlash
cp .env.example .env
nano .env
# BOT_TOKEN ni kiriting va saqlang (Ctrl+X, Y, Enter)

# 6. Botni test qilish
python bot.py
# Agar ishlasa Ctrl+C bilan to'xtating

# 7. Background da ishga tushirish
nohup python bot.py > bot.log 2>&1 &

# 8. Botni tekshirish
tail -f bot.log
```

### systemd service yaratish (Ubuntu/Linux):

```bash
# Service fayli yaratish
sudo nano /etc/systemd/system/reja-bot.service
```

Quyidagini kiriting:
```ini
[Unit]
Description=Reja Bot - Telegram Task Manager
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/Telegram-bot
Environment="PATH=/home/YOUR_USERNAME/Telegram-bot/venv/bin"
ExecStart=/home/YOUR_USERNAME/Telegram-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Service ni yoqish
sudo systemctl daemon-reload
sudo systemctl enable reja-bot
sudo systemctl start reja-bot

# Status tekshirish
sudo systemctl status reja-bot

# Loglarni ko'rish
sudo journalctl -u reja-bot -f
```

## 🐛 Xatolarni tuzatish:

### Xato 1: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Xato 2: "NetworkError" yoki "Conflict"
```bash
# Boshqa joyda bot ochiq bo'lishi mumkin
pkill -f "python.*bot.py"
python bot.py
```

### Xato 3: "Unauthorized" (401)
```bash
# Token noto'g'ri
nano .env
# Yangi token kiriting
```

### Xato 4: Database xatosi
```bash
# Database faylini o'chiring va qayta yarating
rm reja_bot.db
python bot.py
```

## 📊 Monitoring:

```bash
# Bot ishlayotganini tekshirish
ps aux | grep bot.py

# Log faylini ko'rish
tail -f bot.log

# Bot to'xtatish
pkill -f "python.*bot.py"

# Bot qayta ishga tushirish
nohup python bot.py > bot.log 2>&1 &
```

## 🌐 Cloud platformalar:

### Heroku:
1. `Procfile` yarating: `web: python bot.py`
2. `runtime.txt`: `python-3.11.0`
3. Deploy qiling

### Railway:
1. GitHub repository ulang
2. Environment variables qo'shing
3. Deploy qiling

### PythonAnywhere:
1. Bash console oching
2. Repository clone qiling
3. Web app sozlang

## ⚠️ Muhim eslatmalar:

1. `.env` faylini GitHub ga yuklamang!
2. Bot tokenini hech kimga bermang
3. Database faylini muntazam backup qiling
4. Loglarni tekshirib turing
5. Server restart qilganda botni qayta ishga tushiring

## 📞 Yordam:

Agar muammo hal bo'lmasa:
1. `bot.log` faylini tekshiring
2. `python bot.py` ni to'g'ridan-to'g'ri ishga tushiring
3. Xato xabarini o'qing va Google da qidiring
