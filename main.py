from telegram.ext import *
import wikipedia
import imdb

movies = imdb.IMDb()

def start_command(update,context):
    update.message.reply_text("Hello")

def handle_message(update,context):
    text = str(update.message.text).lower()
    if "calc" in text:
        val = text.split()[1]
        res = eval(val)
    elif "wiki" in text:
        update.message.reply_text("Fetching data...")
        val = text.replace("wiki ","")
        res = wikipedia.summary(val)

    elif "imdb" in text:
        update.message.reply_text("Fetching data...")
        val = text.replace("imdb ","")
        mov = movies.search_movie(val)
        id = mov[0].getID()
        movie = movies.get_movie(id)
        res = "Title: "+str(movie["title"])
        res += "\nYear: "+str(movie["year"])
        res += "\nRating: "+str(movie["rating"])
        res += "\nDirectors: "+','.join(map(str,movie["directors"]))
        res += "\nCasting: "+','.join(map(str,movie["cast"]))
    update.message.reply_text(res)


def main():
    updater  = Updater("5193952210:AAFxazh2V_hzlDBh49qmgh1o-e5-gqpcFMA",use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(MessageHandler(Filters.text,handle_message))
    

    updater.start_polling()
    updater.idle()

main()
