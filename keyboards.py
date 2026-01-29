"""
Telegram klaviaturalari
"""

from telegram import ReplyKeyboardMarkup, KeyboardButton

class Keyboards:
    """Klaviatura klassi"""
    
    @staticmethod
    def get_main_keyboard():
        """Asosiy keyboard"""
        keyboard = [
            [KeyboardButton("➕ Vazifa qo'shish"), KeyboardButton("📋 Vazifalar ro'yxati")],
            [KeyboardButton("📅 Bugungi vazifalar"), KeyboardButton("✅ Vazifani bajarish")],
            [KeyboardButton("📊 Statistika"), KeyboardButton("❓ Yordam")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def get_priority_keyboard():
        """Muhimlik darajasi keyboard"""
        keyboard = [
            [KeyboardButton("🔴 Yuqori"), KeyboardButton("🟡 O'rta")],
            [KeyboardButton("🟢 Past"), KeyboardButton("❌ Bekor qilish")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def get_cancel_keyboard():
        """Bekor qilish keyboard"""
        keyboard = [[KeyboardButton("❌ Bekor qilish")]]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    @staticmethod
    def get_skip_keyboard():
        """O'tkazish keyboard"""
        keyboard = [
            [KeyboardButton("⏭️ O'tkazish"), KeyboardButton("❌ Bekor qilish")]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
