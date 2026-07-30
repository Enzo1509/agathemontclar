import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

# Configuration des logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.environ.get("TELEGRAM_TOKEN")

WELCOME_TEXT = """Coucou {name} 🧡

Moi c'est Agathe ! Installe-toi confortablement dans mon salon... On dit souvent que les rousses qui ont la trentaine ont du caractère... et tu as bien fait d'être curieux 😏
Mon salon est parfait pour avoir un aperçu, mais mes vraies discussions intimistes se passent au chaud, dans ma chambre 🗝️✨ 
Je t'attends sur mon profil privé ➡️ @agathemontclar 😊"""

# Remplace l'URL ci-dessous par le lien direct de la photo d'Agathe
PHOTO_URL = "https://i.imgur.com/votre_photo.jpg"

async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = update.chat_join_request
    user = request.from_user
    chat_id = request.chat.id

    # 1. Validation automatique dans le canal
    try:
        await context.bot.approve_chat_join_request(chat_id=chat_id, user_id=user.id)
        logging.info(f"Demande approuvée pour {user.first_name} ({user.id})")
    except Exception as e:
        logging.error(f"Erreur lors de l'approbation : {e}")

    # 2. Envoi du DM automatique
    try:
        keyboard = [
            [InlineKeyboardButton("💬 M'écrire en privé", url="https://t.me/agathemontclar")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = WELCOME_TEXT.format(name=user.first_name or "à toi")

        await context.bot.send_photo(
            chat_id=user.id,
            photo=PHOTO_URL,
            caption=text,
            reply_markup=reply_markup
        )
        logging.info(f"DM privé envoyé avec succès à {user.first_name} ({user.id})")
    except Exception as e:
        logging.warning(f"Impossible d'envoyer le DM à {user.id} : {e}")

def main():
    if not TOKEN:
        raise ValueError("Erreur : La variable TELEGRAM_TOKEN n'est pas définie dans l'environnement.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(ChatJoinRequestHandler(handle_join_request))
    
    logging.info("Le bot Agathe est démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()
