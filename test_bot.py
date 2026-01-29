#!/usr/bin/env python3
"""
Bot test skripti - barcha funksiyalarni tekshirish
"""

print("🧪 Bot Test Natijasi")
print("=" * 50)

# Fayllarni tekshirish
import os
files = ['bot.py', 'handlers.py', 'config.py', 'database.py', 'keyboards.py', 'messages.py', '.env']
print("\n📁 Fayllar:")
for f in files:
    exists = "✅" if os.path.exists(f) else "❌"
    print(f"  {exists} {f}")

# Modullarni import qilish
print("\n📦 Modullar:")
try:
    from config import Config
    print("  ✅ Config")
except Exception as e:
    print(f"  ❌ Config: {e}")

try:
    from database import Database
    print("  ✅ Database")
except Exception as e:
    print(f"  ❌ Database: {e}")

try:
    from keyboards import Keyboards
    print("  ✅ Keyboards")
except Exception as e:
    print(f"  ❌ Keyboards: {e}")

try:
    from messages import Messages
    print("  ✅ Messages")
except Exception as e:
    print(f"  ❌ Messages: {e}")

try:
    from handlers import BotHandlers
    print("  ✅ Handlers")
except Exception as e:
    print(f"  ❌ Handlers: {e}")

try:
    from bot import RejaBot
    print("  ✅ Bot")
except Exception as e:
    print(f"  ❌ Bot: {e}")

# Database testlari
print("\n🗄️ Database Test:")
try:
    db = Database()
    print("  ✅ Database ulanishi")
    
    # Test user qo'shish
    db.add_user(12345, "test_user")
    print("  ✅ User qo'shish")
    
    # Test task qo'shish
    from datetime import datetime, timedelta
    deadline = datetime.now().date() + timedelta(days=1)
    db.add_task(12345, "Test vazifa", "yuqori", deadline)
    print("  ✅ Task qo'shish")
    
    # Tasklar olish
    tasks = db.get_tasks(12345, completed=False)
    print(f"  ✅ Tasklar olish ({len(tasks)} ta)")
    
    # Statistika
    count = db.get_task_count(12345)
    print(f"  ✅ Statistika ({count} ta task)")
    
except Exception as e:
    print(f"  ❌ Database xatosi: {e}")

# Keyboard testlari
print("\n⌨️ Keyboard Test:")
try:
    kb = Keyboards()
    main_kb = kb.get_main_keyboard()
    print("  ✅ Asosiy keyboard")
    
    priority_kb = kb.get_priority_keyboard()
    print("  ✅ Muhimlik keyboard")
    
    cancel_kb = kb.get_cancel_keyboard()
    print("  ✅ Bekor qilish keyboard")
    
except Exception as e:
    print(f"  ❌ Keyboard xatosi: {e}")

# Messages testlari
print("\n💬 Messages Test:")
try:
    msg = Messages()
    welcome = msg.get_welcome_message("Test")
    print("  ✅ Welcome xabar")
    
    help_msg = msg.HELP_MESSAGE
    print("  ✅ Help xabar")
    
    stats_msg = msg.get_stats_message(10, 5, 5, 50.0)
    print("  ✅ Statistika xabar")
    
except Exception as e:
    print(f"  ❌ Messages xatosi: {e}")

# Handlers testlari
print("\n🎛️ Handlers Test:")
try:
    handler = BotHandlers()
    print("  ✅ Handler yaratish")
    
    # Metodlarni tekshirish
    methods = ['boshlash', 'qayta_boshlash', 'yordam', 'vazifa_qosh_boshlash', 
               'vazifalar_royxati', 'bugungi_vazifalar', 'statistika', 
               'bajarildi_boshlash', 'bekor_qilish', 'xabar_qayta_ishlash']
    
    for method in methods:
        if hasattr(handler, method):
            print(f"  ✅ {method}()")
        else:
            print(f"  ❌ {method}() topilmadi")
            
except Exception as e:
    print(f"  ❌ Handlers xatosi: {e}")

print("\n" + "=" * 50)
print("✅ Test yakunlandi!")
