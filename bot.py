import telebot
from telebot import types

bot = telebot.TeleBot('TOKEN')

expenses_data = []


def calculate_total_expenses():
    total_expenses = sum(expense[0] for expense in expenses_data)
    return total_expenses


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_expenses_button = types.KeyboardButton("Add Expenses")
    delete_and_start_again_button = types.KeyboardButton("Delete All")
    total_expenses_button = types.KeyboardButton("Total Expenses")
    help_button = types.KeyboardButton("Help")

    markup.add(add_expenses_button, delete_and_start_again_button,
               total_expenses_button, help_button)

    # Reduce font size for all buttons
    for row in markup.keyboard:
        for button in row:
            button["text_size"] = "small"

    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi!👋 Take control of your finances with our budget tracker.",
                     reply_markup=main_menu())


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "Add Expenses":
        bot.send_message(message.chat.id, "Great! Please enter the amount and description of expenses, "
                                          "separated by a comma (e.g., 50.00, Grocery):")
        bot.register_next_step_handler(message, process_expenses)
    elif message.text == "Delete All":
        expenses_data.clear()
        bot.send_message(message.chat.id, "Everything deleted.", reply_markup=main_menu())
    elif message.text == "Total Expenses":
        total_expenses_text = calculate_total_expenses()
        bot.send_message(message.chat.id, f"Total Expenses: ${total_expenses_text:.2f}",
                         reply_markup=main_menu())
    elif message.text == "Help":
        bot.send_message(message.chat.id, "This is the help message. You can add your instructions here.",
                         reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, "I do not understand you. Please use the buttons.", reply_markup=main_menu())


def process_expenses(message):
    try:
        expenses_amount, expenses_description = map(str.strip, message.text.split(','))
        expenses_amount = float(expenses_amount)
        expenses_data.append((expenses_amount, expenses_description))
        remaining_budget = calculate_total_expenses()
        bot.send_message(message.chat.id,
                         f"Expenses of ${expenses_amount:.2f} for '{expenses_description}' added successfully!\n"
                         f"Remaining Budget: ${remaining_budget:.2f}",
                         reply_markup=main_menu())
    except ValueError:
        bot.send_message(message.chat.id, "Invalid input. Please enter a valid number for expenses.",
                         reply_markup=main_menu())


bot.polling(none_stop=True, interval=0)
