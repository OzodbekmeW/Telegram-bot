"""
Reja Bot - Vazifalarni boshqarish uchun Telegram bot
OOP tamoyiliga asoslangan versiya
"""

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

from config import Config
from handlers import BotHandlers, ADD_TASK_NAME, ADD_TASK_PRIORITY, ADD_TASK_DEADLINE, SELECT_TASK_TO_COMPLETE

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)


class RejaBot:
    """Reja Bot klassi"""
    
    def __init__(self):
        """Konstruktor"""
        self.config = Config()
        self.handlers = BotHandlers()
        self.application = None
    
    def setup_handlers(self):
        """Handlerlarni sozlash"""
        add_task_conv = ConversationHandler(
            entry_points=[
                CommandHandler('add', self.handlers.vazifa_qosh_boshlash),
                MessageHandler(filters.Regex('^➕ Vazifa qo\'shish$'), self.handlers.vazifa_qosh_boshlash)
            ],
            states={
                ADD_TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.vazifa_nomi)],
                ADD_TASK_PRIORITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.muhimlik_daraja)],
                ADD_TASK_DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.muddat_belgilash)],
            },
            fallbacks=[CommandHandler('cancel', self.handlers.bekor_qilish)]
        )
        
        done_task_conv = ConversationHandler(
            entry_points=[
                CommandHandler('done', self.handlers.bajarildi_boshlash),
                MessageHandler(filters.Regex('^✅ Vazifani bajarish$'), self.handlers.bajarildi_boshlash)
            ],
            states={
                SELECT_TASK_TO_COMPLETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.bajarildi_tasdiqlash)],
            },
            fallbacks=[CommandHandler('cancel', self.handlers.bekor_qilish)]
        )
        
        self.application.add_handler(CommandHandler('start', self.handlers.boshlash))
        self.application.add_handler(CommandHandler('restart', self.handlers.qayta_boshlash))
        self.application.add_handler(CommandHandler('help', self.handlers.yordam))
        self.application.add_handler(CommandHandler('list', self.handlers.vazifalar_royxati))
        self.application.add_handler(CommandHandler('today', self.handlers.bugungi_vazifalar))
        self.application.add_handler(CommandHandler('stats', self.handlers.statistika))
        
        self.application.add_handler(add_task_conv)
        self.application.add_handler(done_task_conv)
        
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.xabar_qayta_ishlash))
    
    def run(self):
        """Botni ishga tushirish"""
        self.application = Application.builder().token(self.config.BOT_TOKEN).build()
        
        self.setup_handlers()
        
        logger.info("🚀 Reja Bot ishga tushirildi...")
        logger.info(f"📊 Debug rejimi: {self.config.DEBUG}")
        
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Asosiy funksiya"""
    bot = RejaBot()
    bot.run()


if __name__ == '__main__':
    main()
