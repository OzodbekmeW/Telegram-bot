"""
Reja Bot - Vazifalarni boshqarish uchun Telegram bot
"""

import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from database import Database
from datetime import datetime

# .env faylini yuklash
load_dotenv()

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

ADD_TASK_NAME, ADD_TASK_PRIORITY, ADD_TASK_DEADLINE, SELECT_TASK_TO_COMPLETE = range(4)


BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

db = Database()

def get_main_keyboard():
    """Asosiy keyboard"""
    keyboard = [
        [KeyboardButton("➕ Vazifa qo'shish"), KeyboardButton("📋 Vazifalar ro'yxati")],
        [KeyboardButton("📅 Bugungi vazifalar"), KeyboardButton("✅ Vazifani bajarish")],
        [KeyboardButton("📊 Statistika"), KeyboardButton("❓ Yordam")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_priority_keyboard():
    """Muhimlik darajasi keyboard"""
    keyboard = [
        [KeyboardButton("🔴 Yuqori"), KeyboardButton("🟡 O'rta")],
        [KeyboardButton("🟢 Past"), KeyboardButton("❌ Bekor qilish")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start buyrug'i"""
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    db.add_user(user_id, username)
    
    welcome_text = f"""
👋 Assalomu alaykum, {user.first_name}!

Men *Reja Bot* - sizning shaxsiy vazifalar menejeringizman! 

🎯 Men sizga quyidagilarda yordam bera olaman:
• Vazifalar qo'shish va boshqarish
• Muhim vazifalarni eslatib turish
• Statistikangizni ko'rish
• Kundalik rejalaringizni tuzish

Quyidagi tugmalardan foydalaning yoki /help buyrug'ini yuboring.

Keling, birgalikda samarali ishlaylik! 💪
    """
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot ma'lumotlarini yangilash"""
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name
    
    db.add_user(user_id, username)
    
    context.user_data.clear()
    
    await update.message.reply_text(
        "🔄 *Bot yangilandi!*\n\n"
        "✅ Barcha ma'lumotlar yangilandi\n"
        "✅ Interfeys qayta yuklandi\n\n"
        "Davom etishingiz mumkin! 💪",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam buyrug'i"""
    help_text = """
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
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def add_task_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Vazifa qo'shishni boshlash"""
    await update.message.reply_text(
        "📝 Yangi vazifa qo'shamiz!\n\n"
        "Vazifa nomini kiriting:\n"
        "(Bekor qilish uchun /cancel)",
        reply_markup=ReplyKeyboardMarkup([[KeyboardButton("❌ Bekor qilish")]], resize_keyboard=True)
    )
    return ADD_TASK_NAME

async def add_task_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Vazifa nomini qabul qilish"""
    if update.message.text == "❌ Bekor qilish":
        await update.message.reply_text(
            "❌ Bekor qilindi.",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END
    
    context.user_data['task_name'] = update.message.text
    
    await update.message.reply_text(
        f"✏️ Vazifa: *{update.message.text}*\n\n"
        "Muhimlik darajasini tanlang:",
        parse_mode='Markdown',
        reply_markup=get_priority_keyboard()
    )
    return ADD_TASK_PRIORITY

async def add_task_priority(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muhimlik darajasini qabul qilish"""
    text = update.message.text
    
    if text == "❌ Bekor qilish":
        await update.message.reply_text(
            "❌ Bekor qilindi.",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END
    
    priority_map = {
        "🔴 Yuqori": "yuqori",
        "🟡 O'rta": "o'rta",
        "🟢 Past": "past"
    }
    
    priority = priority_map.get(text, "o'rta")
    context.user_data['priority'] = priority
    
    await update.message.reply_text(
        "📅 Muddat kiriting (masalan: 2025-01-30)\n"
        "yoki /skip bosing:",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("⏭️ O'tkazish"), KeyboardButton("❌ Bekor qilish")]],
            resize_keyboard=True
        )
    )
    return ADD_TASK_DEADLINE

async def add_task_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muddatni qabul qilish va vazifani saqlash"""
    text = update.message.text
    user_id = update.effective_user.id
    
    if text == "❌ Bekor qilish":
        await update.message.reply_text(
            "❌ Bekor qilindi.",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END
    
    deadline = None
    if text != "⏭️ O'tkazish":
        try:
            deadline = datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            await update.message.reply_text(
                "❌ Noto'g'ri format! Iltimos, yyyy-mm-dd formatida kiriting."
            )
            return ADD_TASK_DEADLINE
    
    # Vazifani saqlash
    task_name = context.user_data['task_name']
    priority = context.user_data['priority']
    
    db.add_task(user_id, task_name, priority, deadline)
    
    priority_emoji = {
        "yuqori": "🔴",
        "o'rta": "🟡",
        "past": "🟢"
    }
    
    deadline_text = f"\n📅 Muddat: {deadline}" if deadline else ""
    
    await update.message.reply_text(
        f"✅ *Vazifa qo'shildi!*\n\n"
        f"📌 {task_name}\n"
        f"{priority_emoji[priority]} Muhimlik: {priority.capitalize()}"
        f"{deadline_text}\n\n"
        f"Omad! 💪",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )
    
    # User data tozalash
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Operatsiyani bekor qilish"""
    await update.message.reply_text(
        "❌ Bekor qilindi.",
        reply_markup=get_main_keyboard()
    )
    context.user_data.clear()
    return ConversationHandler.END

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha vazifalarni ko'rsatish"""
    user_id = update.effective_user.id
    tasks = db.get_tasks(user_id, completed=False)
    
    if not tasks:
        await update.message.reply_text(
            "📭 Sizda hozircha vazifalar yo'q.\n\n"
            "➕ Yangi vazifa qo'shish uchun tugmani bosing!",
            reply_markup=get_main_keyboard()
        )
        return
    
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
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def today_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bugungi vazifalarni ko'rsatish"""
    user_id = update.effective_user.id
    today = datetime.now().date()
    tasks = db.get_tasks(user_id, completed=False)
    
    today_tasks = [task for task in tasks if task[3] and task[3] <= today]
    
    if not today_tasks:
        await update.message.reply_text(
            "📅 Bugun uchun vazifalar yo'q.\n\n"
            "Aqilli mehnat qiling va hardoim reja tuzing! 😊",
            reply_markup=get_main_keyboard()
        )
        return
    
    priority_emoji = {
        "yuqori": "🔴",
        "o'rta": "🟡",
        "past": "🟢"
    }
    
    text = "📅 *Bugungi vazifalar:*\n\n"
    
    for i, task in enumerate(today_tasks, 1):
        task_id, task_name, priority, deadline, _, _ = task
        emoji = priority_emoji.get(priority, "⚪")
        text += f"{i}. {emoji} {task_name}\n"
    
    text += f"\n💪 Bugun {len(today_tasks)} ta vazifa bajarish kerak!"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def done_task_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Vazifani bajarishni boshlash"""
    user_id = update.effective_user.id
    tasks = db.get_tasks(user_id, completed=False)
    
    if not tasks:
        await update.message.reply_text(
            "📭 Bajarilmagan vazifalar yo'q!\n\n"
            "Barcha vazifalar bajarildi! 🎉",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END
    
    # Vazifalarni raqamli keyboard qilish
    keyboard = []
    text = "✅ *Qaysi vazifani bajardingiz?*\n\n"
    
    for i, task in enumerate(tasks, 1):
        task_id, task_name, priority, _, _, _ = task
        text += f"{i}. {task_name}\n"
        keyboard.append([KeyboardButton(f"{i}")])
    
    keyboard.append([KeyboardButton("❌ Bekor qilish")])
    
    context.user_data['pending_tasks'] = tasks
    
    await update.message.reply_text(
        text,
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return SELECT_TASK_TO_COMPLETE

async def done_task_complete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Vazifani bajarilgan deb belgilash"""
    text = update.message.text
    
    if text == "❌ Bekor qilish":
        await update.message.reply_text(
            "❌ Bekor qilindi.",
            reply_markup=get_main_keyboard()
        )
        context.user_data.clear()
        return ConversationHandler.END
    
    try:
        task_index = int(text) - 1
        tasks = context.user_data.get('pending_tasks', [])
        
        if 0 <= task_index < len(tasks):
            task = tasks[task_index]
            task_id, task_name = task[0], task[1]
            
            db.complete_task(task_id)
            
            await update.message.reply_text(
                f"🎉 *Ajoyib!*\n\n"
                f"✅ '{task_name}' bajarildi!\n\n"
                f"Davom eting! 💪",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ Noto'g'ri raqam. Qaytadan urinib ko'ring."
            )
            return SELECT_TASK_TO_COMPLETE
    except ValueError:
        await update.message.reply_text(
            "❌ Iltimos, vazifa raqamini kiriting."
        )
        return SELECT_TASK_TO_COMPLETE
    
    context.user_data.clear()
    return ConversationHandler.END

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistika ko'rsatish"""
    user_id = update.effective_user.id
    
    total_tasks = db.get_task_count(user_id)
    completed_tasks = db.get_task_count(user_id, completed=True)
    pending_tasks = total_tasks - completed_tasks
    
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    text = f"""
📊 *Sizning statistikangiz:*

📝 Jami vazifalar: {total_tasks}
✅ Bajarilgan: {completed_tasks}
⏳ Jarayonda: {pending_tasks}
📈 Bajarilish darajasi: {completion_rate:.1f}%

"""
    
    if completion_rate >= 80:
        text += "🌟 Ajoyib! Siz zo'r ishlamoqdasiz!"
    elif completion_rate >= 50:
        text += "👍 Yaxshi! Davom eting!"
    else:
        text += "💪 Oldinga! Siz qila olasiz!"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugma xabarlarini qayta ishlash"""
    text = update.message.text
    
    if text == "➕ Vazifa qo'shish":
        return await add_task_start(update, context)
    elif text == "📋 Vazifalar ro'yxati":
        return await list_tasks(update, context)
    elif text == "📅 Bugungi vazifalar":
        return await today_tasks(update, context)
    elif text == "✅ Vazifani bajarish":
        return await done_task_start(update, context)
    elif text == "📊 Statistika":
        return await stats(update, context)
    elif text == "❓ Yordam":
        return await help_command(update, context)
    else:
        await update.message.reply_text(
            "🤔 Tushunmadim. Tugmalardan foydalaning yoki /help buyrug'ini yuboring.",
            reply_markup=get_main_keyboard()
        )

def main():
    """Botni ishga tushirish"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    add_task_conv = ConversationHandler(
        entry_points=[
            CommandHandler('add', add_task_start),
            MessageHandler(filters.Regex('^➕ Vazifa qo\'shish$'), add_task_start)
        ],
        states={
            ADD_TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_task_name)],
            ADD_TASK_PRIORITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_task_priority)],
            ADD_TASK_DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_task_deadline)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    done_task_conv = ConversationHandler(
        entry_points=[
            CommandHandler('done', done_task_start),
            MessageHandler(filters.Regex('^✅ Vazifani bajarish$'), done_task_start)
        ],
        states={
            SELECT_TASK_TO_COMPLETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, done_task_complete)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('restart', restart))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('list', list_tasks))
    application.add_handler(CommandHandler('today', today_tasks))
    application.add_handler(CommandHandler('stats', stats))
    
    application.add_handler(add_task_conv)
    application.add_handler(done_task_conv)
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot ishga tushirildi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
