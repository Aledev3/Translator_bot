from googletrans import Translator
import json
import telebot

# Inserisci qui il token del tuo bot Telegram
TOKEN = "token_bot"

# Inizializzazione del bot
bot = telebot.TeleBot(TOKEN)

# Funzione per caricare il database JSON
def load_database():
    try:
        with open("user_language_db.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Funzione per salvare il database JSON
def save_database(data):
    with open("user_language_db.json", "w") as f:
        json.dump(data, f)


# Comando /set per impostare la lingua preferita
@bot.message_handler(commands=['set'])
def handle_set_language(message):
    if message.chat.type != 'private':
        bot.reply_to(message, "Il comando /set può essere utilizzato solo in chat private.")
        return

    language = message.text.split('/set ', 1)[-1]
    user_id = str(message.from_user.id)

    database = load_database()
    database[user_id] = language
    save_database(database)

    bot.reply_to(message, f"Hai impostato la tua lingua preferita a {language}. Ora puoi iniziare a tradurre il testo.")

@bot.message_handler(func=lambda message: True)
def translate_text(message):
    if message.chat.type != 'private':
        bot.reply_to(message, "Questo comando può essere utilizzato solo in chat private.")
        return

    user_id = str(message.from_user.id)
    database = load_database()

    if user_id not in database:
        bot.reply_to(message, "Prima di tradurre, devi impostare la tua lingua preferita con /set [lingua].")
        return

    language = database[user_id]
    text = message.text

    # Aggiungi qui il codice per tradurre il testo con la libreria di traduzione che stai utilizzando
    # Ad esempio, con la libreria Googletrans:
    #translator = Translator()
    translator = Translator()
    translated_text = translator.translate(text, dest=language)
    bot.reply_to(message, translated_text.text)

    # Nel codice sopra, sostituisci GoogleTranslator con il metodo corretto per tradurre il testo
    # nella lingua corretta utilizzando la libreria che hai scelto



# Esegui il bot
bot.polling()
