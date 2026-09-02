import os
import logging
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

# Configuration des logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = os.environ.get("TELEGRAM_TOKEN")

WELCOME_TEXT = """Ravie de te voir ici 🧡

Tu as trouvé le chemin jusqu'à moi...

Ici, c'est juste un aperçu. Ce que je choisis de te laisser voir.

Mais j'aime bien savoir qui est assez curieux pour aller un peu plus loin.

Reste un peu. Regarde.

Et si tu as envie d'en découvrir davantage... tu sais déjà où ça se passe 🧡

Je te laisse commencer par mon canal public 🫦
https://t.me/+enHVtdnHs8hkNzFk
"""

# Lien direct de la photo hébergée sur ton GitHub
PHOTO_URL = "https://raw.githubusercontent.com/Enzo1509/agathemontclar/main/image1.jpg"

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
        
        # Sécurisation du prénom pour éviter les crashs de formatage
        safe_name = html.escape(user.first_name or "à toi")
        text = WELCOME_TEXT.format(name=safe_name)

        await context.bot.send_photo(
            chat_id=user.id,
            photo=PHOTO_URL,
            caption=text,
            parse_mode="HTML",
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
