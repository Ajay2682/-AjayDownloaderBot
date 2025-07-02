from flask import Flask
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import os
import requests

TOKEN = "7880080432:AAHlXu-zaLY7NiTot91kpxtLdh2FkRWMpP4"  # your bot token
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Ajay Insta Downloader Bot is Running!"

# Telegram Bot Handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[
        InlineKeyboardButton("📥 Download Instagram", url="https://www.instagram.com"),
        InlineKeyboardButton("📝 Caption Generator", callback_data='caption_help')
    ]]
    await update.message.reply_text(
        "👋 Welcome to Ajay Insta Downloader Bot!\n\n"
        "📥 Send any Instagram link to download.\n"
        "✍️ Type `caption love` or `hashtag attitude` to get started.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "instagram.com" in text:
        await update.message.reply_text("📥 Downloading from Instagram...\n⏳ Please wait...")
        await send_instagram_download(update, text)

    elif text.lower().startswith("caption"):
        topic = text.split(" ", 1)[1] if " " in text else "love"
        await update.message.reply_text(generate_caption(topic))

    elif text.lower().startswith("hashtag"):
        topic = text.split(" ", 1)[1] if " " in text else "style"
        await update.message.reply_text(generate_hashtags(topic))

    else:
        await update.message.reply_text("❓ Unknown command. Try sending an Instagram link or type `caption love`.")

def generate_caption(topic):
    captions = {
        "love": "💖 Love is in the air, and so are my vibes 💕",
        "attitude": "😎 I’m not special, I’m just a limited edition 🔥",
        "funny": "😂 I’m on a seafood diet. I see food and I eat it!",
        "selfie": "📸 Selfie game: 100% on point!",
        "style": "💃 Style isn’t what you wear, it’s how you wear it."
    }
    return captions.get(topic.lower(), f"📝 Sorry, no caption found for '{topic}'.")

def generate_hashtags(topic):
    hashtags = {
        "love": "#love #romantic #couplegoals #heart #sweetvibes",
        "attitude": "#attitude #bossvibes #cool #swagger #mood",
        "funny": "#funny #lol #haha #meme #funnymood",
        "style": "#style #instafashion #ootd #lookbook",
        "travel": "#travel #wanderlust #adventure #vacay"
    }
    return hashtags.get(topic.lower(), f"🏷️ No hashtags found for '{topic}'.")

async def send_instagram_download(update, link):
    try:
        api = f"https://instasupersave.com/api/convert"
        res = requests.post(api, json={"url": link})
        data = res.json()

        if "url" in data:
            await update.message.reply_video(video=data["url"])
        else:
            await update.message.reply_text("❌ Failed to fetch download link.")
    except:
        await update.message.reply_text("⚠️ Error downloading content.")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
