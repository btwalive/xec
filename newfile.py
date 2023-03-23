import string
import math
import telebot
from telebot import types

# Set of characters to remove
to_remove = set(string.digits + string.punctuation)

# Initialize total word count and part count to 0
total_words = 0
part_count = 0

# Initialize Telegram bot
bot = telebot.TeleBot("6182913691:AAEzq8hfpTn-LCYiwANGaPK3xwqAF541Mmg")

# Define handler for "/start" command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Please enter the text you want to split into parts.")

# Define handler for text messages
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    global total_words
    global part_count

    # Remove unwanted characters from the message
    filtered_text = ''.join(char for char in message.text if char not in to_remove)
    # Remove extra whitespace
    filtered_text = ' '.join(filtered_text.split())
    # Add full stop at end of sentence
    if filtered_text[-1] not in ['.', '!', '?']:
        filtered_text += "."

    # Split the text into parts of at most 500 words each
    words = filtered_text.split()
    num_words = len(words)
    max_words_per_part = 500
    num_parts = math.ceil(num_words / max_words_per_part) # corrected line

    # Update total word count
    total_words += num_words

    # Update part count
    part_count += num_parts

    # Send the parts as separate messages
    for i in range(num_parts):
        part_start = i * max_words_per_part
        part_end = min((i + 1) * max_words_per_part, num_words)
        part_text = ' '.join(words[part_start:part_end])
        bot.reply_to(message, part_text)

# Start the bot
bot.polling()
