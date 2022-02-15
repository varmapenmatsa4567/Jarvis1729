from telegram.ext import *
from telegram import *
import wikipedia
import imdb
import wolframalpha
import requests
from bs4 import BeautifulSoup

movies = imdb.IMDb()

wid = "V7WAUA-P9LHUVAXEG"

bot = Bot("5193952210:AAFxazh2V_hzlDBh49qmgh1o-e5-gqpcFMA")

def getUrl(q):
    url = 'https://www.google.com/search?q='+q+" stackoverflow"

    res = requests.get(url)
    bs = BeautifulSoup(res.content,"html.parser")
    links = bs.find_all("a")
    for link in links:
        if 'href' in link.attrs:
            k = str(link.attrs['href'])
            if "https" in k and "stackoverflow.com" in k:
                return k[7:]

def getdata(url):
	r = requests.get(url)
	return r.text

def start_command(update,context):
    update.message.reply_text("Hello")

def handle_message(update,context):
    text = str(update.message.text).lower()
    if "wiki" in text:
        update.message.reply_text("Fetching data...")
        val = text.replace("wiki ","")
        res = wikipedia.summary(val)

    elif "imdb" in text:
        update.message.reply_text("Fetching data...")
        bot.send_chat_action(chat_id=update.message.chat_id,action=ChatAction.TYPING)
        val = text.replace("imdb ","")
        mov = movies.search_movie(val)
        id = mov[0].getID()
        movie = movies.get_movie(id)
        res = "Title: "+str(movie["title"])
        res += "\nYear: "+str(movie["year"])
        res += "\nRating: "+str(movie["rating"])
        res += "\nDirectors: "+','.join(map(str,movie["directors"]))
        res += "\nCasting: "+','.join(map(str,movie["cast"]))
    
    elif "program" in text:
        update.message.reply_text("Fetching data from stack overflow...")
        bot.send_chat_action(chat_id=update.message.chat_id,action=ChatAction.TYPING)
        val = text
        url = getUrl(val)
        htmldata = getdata(url)
        soup = BeautifulSoup(htmldata, 'html.parser')
        data = ''
        cnt = 0
        for data in soup.find_all("code"):
            if len(data.get_text())>10:
                cnt+=1
                bot.send_message(chat_id=update.message.chat_id,text=data.get_text())
                # update.message.reply_text(data.get_text())
            if cnt > 5:
                break
        res = "done"
    else:
        update.message.reply_text("Fetching data...")
        bot.send_chat_action(chat_id=update.message.chat_id,action=ChatAction.TYPING)
        client = wolframalpha.Client(wid)
        res = client.query(text)
        res = next(res.results).text

    update.message.reply_text(res)


def main():
    updater  = Updater("5193952210:AAFxazh2V_hzlDBh49qmgh1o-e5-gqpcFMA",use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(MessageHandler(Filters.text,handle_message))
    

    updater.start_polling()
    updater.idle()

main()
