"""
Bot xabarlari va matnlari
"""

class Messages:
    """Xabarlar klassi"""
    
    # Umumiy xabarlar
    CANCEL_MESSAGE = "❌ Bekor qilindi."
    UNKNOWN_MESSAGE = "🤔 Tushunmadim. Tugmalardan foydalaning yoki /help buyrug'ini yuboring."
    
    # Start xabari
    @staticmethod
    def get_welcome_message(first_name: str) -> str:
        """Xush kelibsiz xabari"""
        return f"""
👋 Assalomu alaykum, {first_name}!

Men *Reja Bot* - sizning shaxsiy vazifalar menejeringizman! 

🎯 Men sizga quyidagilarda yordam bera olaman:
• Vazifalar qo'shish va boshqarish
• Muhim vazifalarni eslatib turish
• Statistikangizni ko'rish
• Kundalik rejalaringizni tuzish

Quyidagi tugmalardan foydalaning yoki /help buyrug'ini yuboring.

Keling, birgalikda samarali ishlaylik! 💪
        """
    HELP_MESSAGE = """
📚 *Buyruqlar ro'yxati:*

/start - Botni boshlash
/restart - Botni yangilash
/add - Yangi vazifa qo'shish
/list - Barcha vazifalar
/today - Bugungi vazifalar
/done - Vazifani bajarish
/stats - Statistika
/help - Yordam

💡 *Maslahatlar:*
• Vazifa qo'shishda muhimlik darajasini belgilang
• Har kuni vazifalaringizni tekshirib turing
• Bajarilgan vazifalarni vaqtida belgilang

Muvaffaqiyatlar! 🌟
    """
    
    # Vazifa qo'shish
    ADD_TASK_START = "📝 Yangi vazifa qo'shamiz!\n\nVazifa nomini kiriting:\n(Bekor qilish uchun /cancel)"
    ADD_TASK_PRIORITY = "Muhimlik darajasini tanlang:"
    ADD_TASK_DEADLINE = "📅 Muddat kiriting (masalan: 2026-01-30)\nyoki /skip bosing:"
    ADD_TASK_DEADLINE_ERROR = "❌ Noto'g'ri format! Iltimos, yyyy-mm-dd formatida kiriting."
    
    @staticmethod
    def get_task_added_message(task_name: str, priority: str, deadline=None) -> str:
        """Vazifa qo'shildi xabari"""
        priority_emoji = {
            "yuqori": "🔴",
            "o'rta": "🟡",
            "past": "🟢"
        }
        deadline_text = f"\n📅 Muddat: {deadline}" if deadline else ""
        
        return (
            f"✅ *Vazifa qo'shildi!*\n\n"
            f"📌 {task_name}\n"
            f"{priority_emoji.get(priority, '⚪')} Muhimlik: {priority.capitalize()}"
            f"{deadline_text}\n\n"
            f"Omad! 💪"
        )
    
    # Vazifalar ro'yxati
    NO_TASKS_MESSAGE = "📭 Sizda hozircha vazifalar yo'q.\n\n➕ Yangi vazifa qo'shish uchun tugmani bosing!"
    
    @staticmethod
    def get_tasks_list_message(tasks: list) -> str:
        """Vazifalar ro'yxati xabari"""
        priority_emoji = {
            "yuqori": "🔴",
            "o'rta": "🟡",
            "past": "🟢"
        }
        
        text = "📋 *Sizning vazifalaringiz:*\n\n"
        
        for i, task in enumerate(tasks, 1):
            task_id, task_name, priority, deadline, _, _ = task
            emoji = priority_emoji.get(priority, "⚪")
            deadline_text = f" 📅 {deadline}" if deadline else ""
            text += f"{i}. {emoji} {task_name}{deadline_text}\n"
        
        text += f"\n💡 Jami: {len(tasks)} ta vazifa"
        return text
    
    # Bugungi vazifalar
    NO_TODAY_TASKS = "📅 Bugun uchun vazifalar yo'q.\n\nDam oling yoki yangi reja tuzing! 😊"
    
    @staticmethod
    def get_today_tasks_message(tasks: list) -> str:
        """Bugungi vazifalar xabari"""
        priority_emoji = {
            "yuqori": "🔴",
            "o'rta": "🟡",
            "past": "🟢"
        }
        
        text = "📅 *Bugungi vazifalar:*\n\n"
        
        for i, task in enumerate(tasks, 1):
            task_id, task_name, priority, deadline, _, _ = task
            emoji = priority_emoji.get(priority, "⚪")
            text += f"{i}. {emoji} {task_name}\n"
        
        text += f"\n💪 Bugun {len(tasks)} ta vazifa bajarish kerak!"
        return text
    
    # Vazifani bajarish
    NO_PENDING_TASKS = "📭 Bajarilmagan vazifalar yo'q!\n\nBarcha vazifalar bajarildi! 🎉"
    SELECT_TASK_TO_COMPLETE = "✅ *Qaysi vazifani bajardingiz?*\n\n"
    
    @staticmethod
    def get_task_completed_message(task_name: str) -> str:
        """Vazifa bajarildi xabari"""
        return (
            f"🎉 *Ajoyib!*\n\n"
            f"✅ '{task_name}' bajarildi!\n\n"
            f"Davom eting! 💪"
        )
    
    # Statistika
    @staticmethod
    def get_stats_message(total: int, completed: int, pending: int, rate: float) -> str:
        """Statistika xabari"""
        text = f"""
📊 *Sizning statistikangiz:*

📝 Jami vazifalar: {total}
✅ Bajarilgan: {completed}
⏳ Jarayonda: {pending}
📈 Bajarilish darajasi: {rate:.1f}%

"""
        if rate >= 80:
            text += "🌟 Ajoyib! Siz zo'r ishlamoqdasiz!"
        elif rate >= 50:
            text += "👍 Yaxshi! Davom eting!"
        else:
            text += "💪 Oldinga! Siz qila olasiz!"
        
        return text
    
    # Restart xabari
    RESTART_MESSAGE = "🔄 *Bot yangilandi!*\n\nBarcha sozlamalar qayta yuklandi.\nDavom etishingiz mumkin! ✅"
