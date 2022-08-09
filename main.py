import database as db
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater, 
    CallbackContext, 
    CommandHandler, 
    MessageHandler, 
    ConversationHandler, 
    Filters, 
    CallbackQueryHandler
)

# Telegram API Key from database
API_KEY = db.get_api_key()

# Global user message tracker
current_user_message = None

# States
MESSAGE, CONFIRM, DIALOG = range(3)

def start_command(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text="  Tatilsepeti'ne Hoşgeldiniz!\n"
                                 "Sorularınızı iletebilirsiniz 🤖")
    return MESSAGE

def handle_message(update: Update, context: CallbackContext) -> int:
    user_message = update.message.text
    bot_response = response(user_message)
    context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)
    if bot_response != db.UNIDENTIFIED_DIALOG:
        buttons = [
            [InlineKeyboardButton('✅ Evet', callback_data='confirmed')], 
            [InlineKeyboardButton('❌ Hayır', callback_data='unconfirmed')] 
        ]
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                reply_markup=InlineKeyboardMarkup(buttons),
                                text="Yanıt yardımcı oldu mu?")
        global current_user_message ; current_user_message = user_message
        return CONFIRM
    return MESSAGE

def response(user_message:str) -> str:
    return db.get_response(user_message)

def confirm_query(update: Update, context: CallbackContext) -> int:
    query = update.callback_query.data
    update.callback_query.answer()

    if query == 'confirmed': 
        context.bot.send_message(chat_id=update.effective_chat.id, text="Başka soru sorabilirsiniz.")
        return MESSAGE
    if query == 'unconfirmed':
        dialogs = db.get_dialog_suggestions(current_user_message)
        buttons = [
            [InlineKeyboardButton(dialogs[0][1], callback_data=dialogs[0][0])], 
            [InlineKeyboardButton(dialogs[1][1], callback_data=dialogs[1][0])],
            [InlineKeyboardButton(dialogs[2][1], callback_data=dialogs[2][0])],
            [InlineKeyboardButton(dialogs[3][1], callback_data=dialogs[3][0])],
            [InlineKeyboardButton("🔴 Sorum bunlardan biri değil.", callback_data='Final')]
        ]
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                reply_markup=InlineKeyboardMarkup(buttons),
                                text="Bu sorulardan birinin cevabını mı arıyorsunuz?")
        return DIALOG

def dialog_query(update: Update, context: CallbackContext) -> int:
    query = update.callback_query.data
    update.callback_query.answer()
    if query == 'Final':
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                text="İşlemlerinizin tamamlanması ve sizlere daha detaylı bilgi aktarmamız "
                                     "için 444 44 20 numarasından tatil danışmanlarımıza ulaşabilirsiniz.")
    else:
        dialog = db.get_dialog_by_id(query)
        bot_output = dialog[2]
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=bot_output)
    return ConversationHandler.END


def main() -> None:
    updater = Updater(token=API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    
    # Handlers
    start_handler = CommandHandler(command='start', callback=start_command)
    message_handler = MessageHandler(filters=Filters.text & (~Filters.command), callback=handle_message)
    conv_handler = ConversationHandler(
            entry_points=[start_handler, message_handler, CallbackQueryHandler(callback=dialog_query)],
            states={
                MESSAGE: [message_handler],
                CONFIRM: [CallbackQueryHandler(callback=confirm_query)],
                DIALOG: [CallbackQueryHandler(callback=dialog_query)],
            },
            fallbacks=[message_handler]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
