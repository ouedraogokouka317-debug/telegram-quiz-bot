import os
import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# =============================
# CONFIG
# =============================
TOKEN = os.getenv("BOT TOKEN ICI")

# Quiz de test (structure finale)
QUIZ = [
    {
        "question": "Quel est le plus grand pays du monde en superficie ?",
        "options": ["Le Canada", "La Russie", "Les États-Unis", "La Chine"],
        "answer": 1,
        "explanation": "La Russie est le plus grand pays du monde par sa superficie."
    },
    {
        "question": "Quel continent est le plus vaste ?",
        "options": ["Afrique", "Asie", "Europe", "Amérique"],
        "answer": 1,
        "explanation": "L’Asie est le continent le plus vaste."
    }
]

# =============================
# COMMANDES
# =============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["index"] = 0
    context.user_data["score"] = 0

    await update.message.reply_text(
        "🎯 Bienvenue dans le Quiz Interactif\n\n"
        "Appuie sur /quiz pour commencer."
    )


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["index"] = 0
    context.user_data["score"] = 0
    await send_question(update, context)


# =============================
# LOGIQUE DU QUIZ
# =============================
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = context.user_data.get("index", 0)

    if index >= len(QUIZ):
        score = context.user_data.get("score", 0)
        await update.effective_chat.send_message(
            f"🏁 Quiz terminé !\n\n"
            f"✅ Score : {score}/{len(QUIZ)}"
        )
        return

    q = QUIZ[index]

    keyboard = []
    for i, option in enumerate(q["options"]):
        keyboard.append([
            InlineKeyboardButton(
                option,
                callback_data=f"{index}|{i}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.effective_chat.send_message(
        f"📚 Question {index + 1}/{len(QUIZ)}\n\n"
        f"{q['question']}",
        reply_markup=reply_markup
    )


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("|")
    q_index = int(data[0])
    selected = int(data[1])

    question = QUIZ[q_index]

    if selected == question["answer"]:
        context.user_data["score"] += 1
        text = "✅ Bonne réponse !\n\n"
    else:
        correct = question["options"][question["answer"]]
        text = f"❌ Mauvaise réponse.\n\n✅ Bonne réponse : {correct}\n\n"

    text += f"ℹ️ {question['explanation']}"

    await query.edit_message_text(text)

    # pause avant question suivante
    await asyncio.sleep(2)

    context.user_data["index"] += 1
    await send_question(update, context)


# =============================
# LANCEMENT DU BOT
# =============================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CallbackQueryHandler(handle_answer))

    print("🤖 Bot en ligne...")
    app.run_polling()


if __name__ == "__main__":
    main()
