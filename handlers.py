"""
Bot handlerlar klassi - barcha buyruqlar va xabarlarni qayta ishlash
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime

from database import Database
from keyboards import Keyboards
from messages import Messages

logger = logging.getLogger(__name__)

# Conversation holatlari
ADD_TASK_NAME, ADD_TASK_PRIORITY, ADD_TASK_DEADLINE, SELECT_TASK_TO_COMPLETE = range(4)


class BotHandlers:
    """Bot handlerlar klassi"""
    
    def __init__(self):
        """Konstruktor"""
        self.db = Database()
        self.keyboards = Keyboards()
        self.messages = Messages()
    
    async def boshlash(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Botni boshlash"""
        user = update.effective_user
        user_id = user.id
        username = user.username or user.first_name
        
        # Foydalanuvchini bazaga qo'shish
        self.db.add_user(user_id, username)
        
        welcome_text = self.messages.get_welcome_message(user.first_name)
        
        await update.message.reply_text(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=self.keyboards.get_main_keyboard()
        )
    
    async def qayta_boshlash(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Botni qayta boshlash"""
        await update.message.reply_text(
            self.messages.RESTART_MESSAGE,
            parse_mode='Markdown',
            reply_markup=self.keyboards.get_main_keyboard()
        )
    
    async def yordam(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Yordam ko'rsatish"""
        await update.message.reply_text(
            self.messages.HELP_MESSAGE,
            parse_mode='Markdown'
        )
    
    # ========== Vazifa qo'shish ==========
    
    async def vazifa_qosh_boshlash(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Vazifa qo'shishni boshlash"""
        await update.message.reply_text(
            self.messages.ADD_TASK_START,
            reply_markup=self.keyboards.get_cancel_keyboard()
        )
        return ADD_TASK_NAME
    
    async def vazifa_nomi(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Vazifa nomini qabul qilish"""
        if update.message.text == "❌ Bekor qilish":
            await update.message.reply_text(
                self.messages.CANCEL_MESSAGE,
                reply_markup=self.keyboards.get_main_keyboard()
            )
            return ConversationHandler.END
        
        context.user_data['task_name'] = update.message.text
        
        await update.message.reply_text(
            f"✏️ Vazifa: *{update.message.text}*\n\n{self.messages.ADD_TASK_PRIORITY}",
            parse_mode='Markdown',
            reply_markup=self.keyboards.get_priority_keyboard()
        )
        return ADD_TASK_PRIORITY
    
    async def muhimlik_daraja(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muhimlik darajasini qabul qilish"""
        text = update.message.text
        
        if text == "❌ Bekor qilish":
            await update.message.reply_text(
                self.messages.CANCEL_MESSAGE,
                reply_markup=self.keyboards.get_main_keyboard()
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
            self.messages.ADD_TASK_DEADLINE,
            reply_markup=self.keyboards.get_skip_keyboard()
        )
        return ADD_TASK_DEADLINE
    
    async def muddat_belgilash(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Muddatni qabul qilish va vazifani saqlash"""
        text = update.message.text
        user_id = update.effective_user.id
        
        if text == "❌ Bekor qilish":
            await update.message.reply_text(
                self.messages.CANCEL_MESSAGE,
                reply_markup=self.keyboards.get_main_keyboard()
            )
            return ConversationHandler.END
        
        deadline = None
        if text != "⏭️ O'tkazish":
            try:
                deadline = datetime.strptime(text, "%Y-%m-%d").date()
            except ValueError:
                await update.message.reply_text(
                    self.messages.ADD_TASK_DEADLINE_ERROR
                )
                return ADD_TASK_DEADLINE
        
        # Vazifani saqlash
        task_name = context.user_data['task_name']
        priority = context.user_data['priority']
        
        self.db.add_task(user_id, task_name, priority, deadline)
        
        await update.message.reply_text(
            self.messages.get_task_added_message(task_name, priority, deadline),
            parse_mode='Markdown',
            reply_markup=self.keyboards.get_main_keyboard()
        )
        
        # User data tozalash
        context.user_data.clear()
        return ConversationHandler.END
    
    # ========== Vazifalar ro'yxati ==========
    
    async def vazifalar_royxati(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Barcha vazifalarni ko'rsatish"""
        user_id = update.effective_user.id
        tasks = self.db.get_tasks(user_id, completed=False)
        
        if not tasks:
            await update.message.reply_text(
                self.messages.NO_TASKS_MESSAGE,
                reply_markup=self.keyboards.get_main_keyboard()
            )
            return
        
        text = self.messages.get_tasks_list_message(tasks)
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def bugungi_vazifalar(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bugungi vazifalarni ko'rsatish"""
        user_id = update.effective_user.id
        today = datetime.now().date()
        tasks = self.db.get_tasks(user_id, completed=False)
        
        today_tasks = [task for task in tasks if task[3] and task[3] <= today]
        
        if not today_tasks:
            await update.message.reply_text(
                self.messages.NO_TODAY_TASKS,
                reply_markup=self.keyboards.get_main_keyboard()
            )
            return
        
        text = self.messages.get_today_tasks_message(today_tasks)
        await update.message.reply_text(text, parse_mode='Markdown')
    
    # ========== Vazifani bajarish ==========
    
    async def bajarildi_boshlash(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Vazifani bajarishni boshlash"""
        user_id = update.effective_user.id
        tasks = self.db.get_tasks(user_id, completed=False)
        
        if not tasks:
            await update.message.reply_text(
                self.messages.NO_PENDING_TASKS,
                reply_markup=self.keyboards.get_main_keyboard()
            )
            return ConversationHandler.END
        
        # Vazifalarni raqamli keyboard qilish
        from telegram import ReplyKeyboardMarkup, KeyboardButton
        keyboard = []
        text = self.messages.SELECT_TASK_TO_COMPLETE
        
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
    
    async def bajarildi_tasdiqlash(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Vazifani bajarilgan deb belgilash"""
        text = update.message.text
        
        if text == "❌ Bekor qilish":
            await update.message.reply_text(
                self.messages.CANCEL_MESSAGE,
                reply_markup=self.keyboards.get_main_keyboard()
            )
            context.user_data.clear()
            return ConversationHandler.END
        
        try:
            task_index = int(text) - 1
            tasks = context.user_data.get('pending_tasks', [])
            
            if 0 <= task_index < len(tasks):
                task = tasks[task_index]
                task_id, task_name = task[0], task[1]
                
                self.db.complete_task(task_id)
                
                await update.message.reply_text(
                    self.messages.get_task_completed_message(task_name),
                    parse_mode='Markdown',
                    reply_markup=self.keyboards.get_main_keyboard()
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
    
    # ========== Statistika ==========
    
    async def statistika(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Statistika ko'rsatish"""
        user_id = update.effective_user.id
        
        total_tasks = self.db.get_task_count(user_id)
        completed_tasks = self.db.get_task_count(user_id, completed=True)
        pending_tasks = total_tasks - completed_tasks
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        text = self.messages.get_stats_message(
            total_tasks, completed_tasks, pending_tasks, completion_rate
        )
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    # ========== Bekor qilish ==========
    
    async def bekor_qilish(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Operatsiyani bekor qilish"""
        await update.message.reply_text(
            self.messages.CANCEL_MESSAGE,
            reply_markup=self.keyboards.get_main_keyboard()
        )
        context.user_data.clear()
        return ConversationHandler.END
    
    # ========== Xabarlarni qayta ishlash ==========
    
    async def xabar_qayta_ishlash(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Tugma xabarlarini qayta ishlash"""
        text = update.message.text
        
        if text == "➕ Vazifa qo'shish":
            return await self.vazifa_qosh_boshlash(update, context)
        elif text == "📋 Vazifalar ro'yxati":
            return await self.vazifalar_royxati(update, context)
        elif text == "📅 Bugungi vazifalar":
            return await self.bugungi_vazifalar(update, context)
        elif text == "✅ Vazifani bajarish":
            return await self.bajarildi_boshlash(update, context)
        elif text == "📊 Statistika":
            return await self.statistika(update, context)
        elif text == "❓ Yordam":
            return await self.yordam(update, context)
        else:
            await update.message.reply_text(
                self.messages.UNKNOWN_MESSAGE,
                reply_markup=self.keyboards.get_main_keyboard()
            )
