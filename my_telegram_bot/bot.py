import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Состояния для диалога
BUSINESS_NAME, BUSINESS_TYPE, AUTOMATION_GOAL, CONTACT_INFO = range(4)

# ========== ГЛАВНОЕ МЕНЮ ==========
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🤖 Демо-бот для пиццерии", callback_data='demo_pizza')],
        [InlineKeyboardButton("💼 Услуги и цены", callback_data='services')],
        [InlineKeyboardButton("💬 Оставить заявку", callback_data='leave_request')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contacts')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Привет! Я демо-бот *Digital Agency*\n\n"
        "Я покажу как чат-боты могут помочь вашему бизнесу:\n"
        "• Автоматизировать заказы 24/7\n"  
        "• Увеличить продажи на 15-30%\n"
        "• Снизить нагрузку на staff\n\n"
        "Выберите опцию:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ========== ОБРАБОТЧИК КНОПОК ==========
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'demo_pizza':
        await demo_pizza_bot(query)
    elif query.data == 'services':
        await show_services(query)
    elif query.data == 'leave_request':
        await start_leave_request(query)
    elif query.data == 'contacts':
        await show_contacts(query)
    elif query.data == 'back_to_main':
        await back_to_main(query)
    elif query.data == 'pizza_menu':
        await show_pizza_menu(query)
    elif query.data == 'pizza_order':
        await start_pizza_order(query)
    elif query.data == 'pizza_about':
        await pizza_about(query)

# ========== ДЕМО ПИЦЦЕРИЯ ==========
async def demo_pizza_bot(query):
    keyboard = [
        [InlineKeyboardButton("🍕 Посмотреть меню", callback_data='pizza_menu')],
        [InlineKeyboardButton("🛒 Сделать заказ", callback_data='pizza_order')],
        [InlineKeyboardButton("ℹ️ О нас", callback_data='pizza_about')],
        [InlineKeyboardButton("↩️ В главное меню", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🍕 *Добро пожаловать в виртуальную пиццерию!*\n\n"
        "Это демо-версия бота для приема заказов. "
        "Такой же бот может работать для вашего бизнеса 24/7!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def show_pizza_menu(query):
    menu_text = (
        "🍕 *Наше меню:*\n\n"
        "• Маргарита - 450 руб.\n"
        "• Пепперони - 500 руб.\n" 
        "• Гавайская - 550 руб.\n"
        "• Четыре сыра - 600 руб.\n\n"
        "_Это демо-меню. В реальном боте вы можете легко менять цены и ассортимент._"
    )
    
    keyboard = [
        [InlineKeyboardButton("🛒 Сделать заказ", callback_data='pizza_order')],
        [InlineKeyboardButton("↩️ Назад", callback_data='demo_pizza')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')

async def start_pizza_order(query):
    await query.edit_message_text(
        "🎉 *Отлично! Вы увидели демо-версию!*\n\n"
        "Такой же бот для вашего бизнеса:\n"
        "• Будет принимать заказы 24/7\n"
        "• Снизит нагрузку на сотрудников\n" 
        "• Увеличит средний чек на 15-30%\n\n"
        "Хотите рассчитать стоимость для вашего бизнеса?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Рассчитать стоимость", callback_data='leave_request')],
            [InlineKeyboardButton("📞 Связаться сейчас", callback_data='contacts')],
            [InlineKeyboardButton("↩️ В главное меню", callback_data='back_to_main')]
        ]),
        parse_mode='Markdown'
    )

async def pizza_about(query):
    await query.edit_message_text(
        "🏪 *О нашей пиццерии*\n\n"
        "Мы работаем с 2020 года и используем современные технологии "
        "для улучшения обслуживания клиентов!\n\n"
        "Такой же бот может работать и для вашего бизнеса!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Узнать стоимость", callback_data='leave_request')],
            [InlineKeyboardButton("↩️ Назад", callback_data='demo_pizza')]
        ]),
        parse_mode='Markdown'
    )

# ========== УСЛУГИ И ЦЕНЫ ==========
async def show_services(query):
    services_text = (
        "💼 *Наши услуги:*\n\n"
        "🤖 *Чат-боты для бизнеса*\n"
        "• Прием заказов и записей\n"
        "• Автоответчик на вопросы\n"
        "• Интеграция с CRM\n\n"
        "💰 *Стоимость:*\n"
        "• От 15 000 руб. за готового бота\n"
        "• Срок: 5-7 дней\n\n"
        "📋 *Что входит:*\n"
        "• Настройка и запуск\n"
        "• Обучение управлению\n" 
        "• Поддержка 1 месяц\n\n"
        "_*Бесплатная консультация и демо!*_"
    )
    
    keyboard = [
        [InlineKeyboardButton("💬 Оставить заявку", callback_data='leave_request')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contacts')],
        [InlineKeyboardButton("↩️ В главное меню", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(services_text, reply_markup=reply_markup, parse_mode='Markdown')

# ========== СБОР ЗАЯВОК ==========
async def start_leave_request(query):
    await query.edit_message_text(
        "📝 *Оставить заявку*\n\n"
        "Ответьте на 4 простых вопроса для расчета стоимости:\n\n"
        "*Вопрос 1/4:*\nКак называется ваш бизнес?",
        parse_mode='Markdown'
    )
    return BUSINESS_NAME

async def get_business_name(update: Update, context):
    context.user_data['business_name'] = update.message.text
    await update.message.reply_text(
        "*Вопрос 2/4:*\nКакая у вас сфера? (ресторан, салон красоты, доставка...)",
        parse_mode='Markdown'
    )
    return BUSINESS_TYPE

async def get_business_type(update: Update, context):
    context.user_data['business_type'] = update.message.text
    await update.message.reply_text(
        "*Вопрос 3/4:*\nЧто хотите автоматизировать? (прием заказов, запись клиентов...)",
        parse_mode='Markdown'
    )
    return AUTOMATION_GOAL

async def get_automation_goal(update: Update, context):
    context.user_data['automation_goal'] = update.message.text
    await update.message.reply_text(
        "*Вопрос 4/4:*\nВаш номер Telegram для связи?",
        parse_mode='Markdown'
    )
    return CONTACT_INFO

async def get_contact_info(update: Update, context):
    context.user_data['contact_info'] = update.message.text
    user_data = context.user_data
    
    # Формируем заявку
    application_text = (
        "🎉 *НОВАЯ ЗАЯВКА!*\n\n"
        f"*Бизнес:* {user_data['business_name']}\n"
        f"*Сфера:* {user_data['business_type']}\n"
        f"*Задача:* {user_data['automation_goal']}\n"
        f"*Контакты:* {user_data['contact_info']}\n\n"
        "_Не забудьте связаться с клиентом!_"
    )
    
    # Здесь бот отправит заявку вам в личку
    # Пока просто выводим в консоль
    print("="*50)
    print("НОВАЯ ЗАЯВКА:")
    print(f"Бизнес: {user_data['business_name']}")
    print(f"Сфера: {user_data['business_type']}") 
    print(f"Задача: {user_data['automation_goal']}")
    print(f"Контакты: {user_data['contact_info']}")
    print("="*50)
    
    await update.message.reply_text(
        "✅ *Спасибо! Заявка принята!*\n\n"
        "Наш менеджер свяжется с вами в течение 2 часов для бесплатной консультации "
        "и расчета точной стоимости.\n\n"
        "А пока посмотрите демо-версии ботов 👇",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Демо-боты", callback_data='demo_pizza')],
            [InlineKeyboardButton("📞 Связаться сейчас", callback_data='contacts')]
        ]),
        parse_mode='Markdown'
    )
    return ConversationHandler.END

# ========== КОНТАКТЫ ==========
async def show_contacts(query):
    await query.edit_message_text(
        "📞 *Контакты*\n\n"
        "💬 *Telegram:* @your_username\n"
        "📱 *Телефон:* +7 (XXX) XXX-XX-XX\n"
        "🕐 *Время работы:* 9:00-21:00\n\n"
        "💡 *Бесплатная консультация* - ответим на все вопросы!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Оставить заявку", callback_data='leave_request')],
            [InlineKeyboardButton("↩️ В главное меню", callback_data='back_to_main')]
        ]),
        parse_mode='Markdown'
    )

# ========== НАЗАД В ГЛАВНОЕ МЕНЮ ==========
async def back_to_main(query):
    keyboard = [
        [InlineKeyboardButton("🤖 Демо-бот для пиццерии", callback_data='demo_pizza')],
        [InlineKeyboardButton("💼 Услуги и цены", callback_data='services')],
        [InlineKeyboardButton("💬 Оставить заявку", callback_data='leave_request')],
        [InlineKeyboardButton("📞 Контакты", callback_data='contacts')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "👋 Главное меню. Выберите опцию:",
        reply_markup=reply_markup
    )

async def cancel(update: Update, context):
    await update.message.reply_text('Диалог прерван. Напишите /start чтобы начать заново.')
    return ConversationHandler.END

def main():
    # Создаем приложение
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    
    # Обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Обработчик диалога для заявок
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_leave_request, pattern='^leave_request$')],
        states={
            BUSINESS_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_business_name)],
            BUSINESS_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_business_type)],
            AUTOMATION_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_automation_goal)],
            CONTACT_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact_info)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()