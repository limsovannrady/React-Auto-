import os
import random
import logging
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReactionTypeEmoji
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

ADMIN_ID = int(os.getenv('ADMIN_ID', '5002402843'))

# Only standard Telegram reaction emojis that actually work
REACTION_EMOJIS = [
    # Most reliable basic reactions
    "👍", "👎", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🤬", "😢", "🎉", "🤩", 
    "🤮", "💩", "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "🌚", "🌭", "💯", 
    "🤣", "⚡", "🍌", "🏆", "💔", "🤨", "😐", "🍓", "🍾", "💋", "😈", "😴", "😭", 
    "🤓", "👻", "👀", "🎃", "🙈", "😇", "😨", "🤝", "🤗", "🎅", "🎄", "🤪", "🗿", 
    "🆒", "💘", "🙉", "🦄", "😘", "💊", "🙊", "😎", "👾"
]
logger.info(f"Loaded {len(REACTION_EMOJIS)} supported emojis for auto-reactions")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    if not update.message:
        logger.warning("Received /start command without valid message")
        return

    user = update.effective_user

    last_name = user.last_name if user and user.last_name else (user.first_name if user and user.first_name else "មិត្ត")

    safe_last_name = html.escape(last_name)
    start_message = (
        f'<tg-emoji emoji-id="5472055112702629499">👋</tg-emoji> សួស្តី {safe_last_name} សូមស្វាគមន៍មកកាន់ Auto Reaction Bot\n\n'
        f'Bot នេះអាច Reaction ដោយស្វ័យប្រវត្តិទៅលើសារទាំងអស់នៅក្នុងក្រុមដូចជា <tg-emoji emoji-id="5373292756342938165">😗</tg-emoji><tg-emoji emoji-id="5370900820336319679">🥰</tg-emoji><tg-emoji emoji-id="5372886001465170842">😍</tg-emoji><tg-emoji emoji-id="5372881676433105377">😆</tg-emoji><tg-emoji emoji-id="5370953476635368811">😂</tg-emoji><tg-emoji emoji-id="5370564490037303348">😝</tg-emoji><tg-emoji emoji-id="5373141891321699086">😎</tg-emoji>\n\n'
        f'<blockquote><tg-emoji emoji-id="5373039692574893940">👨‍🏫</tg-emoji> របៀបប្រើ:\n\n'
        f"1. បន្ថែម Bot ទៅក្នុងក្រុមរបស់អ្នក\n"
        f"2. Add bot ទៅជា admin group\n"
        f"3. បន្ទាប់មក Bot នឹងចាប់ផ្ដើម Reaction ដោយស្វ័យប្រវត្តិ</blockquote>"
    )
    
    # Create inline keyboard with "Add bot to Group" button
    keyboard = [
        [InlineKeyboardButton("🤖 បន្ថែមបូតទៅក្រុម", url=f"https://t.me/{context.bot.username}?startgroup=true")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(start_message, reply_markup=reply_markup, parse_mode='HTML')

    # Notify admin about new user
    try:
        full_name = user.full_name if user else "មិនស្គាល់"
        username = f"@{user.username}" if user and user.username else "គ្មាន username"
        user_id = user.id if user else "មិនស្គាល់"
        admin_message = (
            f"🔔 អ្នកប្រើប្រាស់ថ្មី!\n\n"
            f"👤 ឈ្មោះ: {full_name}\n"
            f"🔗 Username: {username}\n"
            f"🆔 ID: {user_id}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
        logger.info(f"Admin notified about new user: {user_id}")
    except Exception as e:
        logger.error(f"Failed to notify admin: {e}")

async def auto_react(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Auto react to messages in group chats."""
    # Check if we have valid message and chat objects
    if not update.effective_chat or not update.message:
        logger.warning("Received update without valid chat or message")
        return
        
    logger.info(f"Message received in {update.effective_chat.type} chat (ID: {update.effective_chat.id})")
    
    # React to messages in all chat types (private, group, supergroup)
    if update.effective_chat.type in ['private', 'group', 'supergroup']:
        try:
            # Choose a random emoji from the list
            random_emoji = random.choice(REACTION_EMOJIS)
            
            logger.info(f"Attempting to react with {random_emoji} to message {update.message.message_id}")
            
            # React to the message
            await context.bot.set_message_reaction(
                chat_id=update.effective_chat.id,
                message_id=update.message.message_id,
                reaction=[ReactionTypeEmoji(random_emoji)],
                is_big=False
            )
            
            logger.info(f"Successfully reacted with {random_emoji} to message in chat {update.effective_chat.id}")
            
        except Exception as e:
            logger.error(f"Failed to react to message: {e}")
    else:
        logger.info(f"Received message in {update.effective_chat.type} chat - chat type not supported for reactions")

def main() -> None:
    """Start the bot."""
    # Get bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not found!")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Add command handler for /start
    application.add_handler(CommandHandler("start", start))
    
    # Add message handler for auto-reactions (react to ALL messages except commands and bot messages)
    application.add_handler(MessageHandler(
        ~filters.COMMAND & ~filters.StatusUpdate.ALL & ~filters.UpdateType.EDITED_MESSAGE, 
        auto_react
    ))
    
    # Run the bot until the user presses Ctrl-C
    logger.info("Starting Telegram bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()