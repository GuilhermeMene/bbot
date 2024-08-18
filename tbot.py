"""
A telegram bot for follow the trade bot activity
"""

import os
import asyncio
from datetime import datetime
from telebot.async_telebot import AsyncTeleBot
from binance.spot import Spot
from bbot import logger as log
from bbot import state

#Get the token
TOKEN = os.environ.get('BBOT_TOKEN')

#get the chatbot token adn authenticate the bot
KEY = os.environ.get('CB_KEY')
SECRET = os.environ.get('CB_SECRET')

client = Spot(api_key=KEY, api_secret=SECRET)

#Set the bot
bot = AsyncTeleBot(TOKEN)

#Set the usage wiki
usage = 'The usage of the bot is: \n \
            /status: return the status of the bbot (Operational: true of false) and the time of the last loop; \n \
            /balance: return the balances of BTC and USDT from the current wallet; \n \
            /last_trade: return the last efective trade; \n \
            /ping: return the current ping from the bot and Binance; \n \
            /stop: stop the tradebot.'

# Start the bot
@bot.message_handler(commands=['help', 'start'])
async def bot_start(message):
    """
    Method to start the bot and say the hello!
    """
    text = 'Hello, This is the BBot chat.\n' + usage

    await bot.reply_to(message, text)

#Set the status reply
@bot.message_handler(commands=['status'])
async def get_status(message):
    """
    Method to get the current status of the bot
    """
    try:
        with open('Status-logs.txt', "r") as st:
            for line in st:
                pass
            last_status = line
        status = list(last_status.split(':'))

        if state.STATE == 1:
            st = "Able to run"
        else:
            st = "Stopped"

        text = f"The operational state is : {st} \n \
                The operational condition is: {status[2]} \n \
                The last event was recorded at: {status[0]}."

    except:
        text = 'An error occurred. The status cannot be defined.'

    await bot.send_message(message.chat.id, text)

#Set the return of the balance
@bot.message_handler(commands=['balance'])
async def get_balance(message):
    """
    Method to get the balance of the wallet
    """
    try:
        with open('Balance-logs.csv', 'r') as bl:
            for line in bl:
                pass
            last_line = list(line.split(','))

        text = f"BTC balance: {last_line[1]}, and USDT balance: {last_line[2]}"

    except:
        text = "An error occurred. The balance cannot be accessed."

    await bot.send_message(message.chat.id, text)

#Set the last trade of the bot
@bot.message_handler(commands=['last_trade'])
async def get_last_trade(message):
    """
    Method for get the last trade
    """
    try:
        last_trade = log.get_last_trade()

        if last_trade == "File not found":
            text = "The trade record not exists."

        else:
            text = f"Time: {last_trade[0]} \n \
                    Symbol: {last_trade[1]} \n \
                    Price: {last_trade[3]} \n \
                    origQty: {last_trade[4]} \n \
                    execQty: {last_trade[5]} \n \
                    Type: {last_trade[6]} \n \
                    Side: {last_trade[7]}"
    except:
        text = f"An error eccurred. The last trade cannot be accessed."

    await bot.send_message(message.chat.id, text)

#Get the ping from Binance
@bot.message_handler(commands=['ping'])
async def get_ping(message):
    """
    Get the ping from balance
    """
    try:
        dir = os.getcwd()
        with open(os.path.join(dir, 'Status-logs.txt'), "r") as st:
            for line in st:
                pass
            last_status = line
            status = last_status.split(':')

        text = f"The last ping recorded is: {status[4]}."
    except:
        text = 'An error occurred. The status cannot be defined.'

    await bot.send_message(message.chat.id, text)

#Set the STOP
@bot.message_handler(commands=['stop'])
async def set_stop(message):
    """
    Set the stop fopr the BOT
    """
    try:
        state.stop_state()
        text = "The bot will be stopped in the next loop (~ 1 minute)."
    except:
        text = "An error occurred. The bot will continue running."

#Reply for any other message
@bot.message_handler(func=lambda msg: True)
async def echo_all(message):
    await bot.send_message(message.chat.id, usage)


print("Running the bot...")
asyncio.run(bot.polling())
