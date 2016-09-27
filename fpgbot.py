#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, StringCommandHandler, Job
from telegram.ext.dispatcher import run_async
import logging
import time
from signal import signal, SIGINT, SIGTERM, SIGABRT
import settings
from peewee import *
from datetime import datetime
import urllib2, json


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


db = SqliteDatabase('users.db')

jobs = {}

class BaseModel(Model):
    class Meta:
        database = db
        
class User(BaseModel):
    id = IntegerField(primary_key=True)
    latitude = FloatField()
    longitude = FloatField()
    active = BooleanField()
    lastupdated = DateTimeField(null = True)
    
class UserPokemons(BaseModel):
    user = ForeignKeyField(User)
    pokemon = CharField()
    
    
class UserEncounter(BaseModel):
    user = ForeignKeyField(User)
    encounter = CharField()
    expires = DateTimeField()

db.connect()

#db.create_tables([User, UserPokemons, UserEncounter])


def start(bot, update):
    update.message.reply_text('Hello and welcome to the Pokemon Go bot. Send me your location to start!')

def help(bot, update):
    cmd = [ "Available commands",
            "",
            "Send your location - sets location to watch",
            "/stop - stops bot",
            "/watchlist - lists all pokemons on watchlist", 
            "/ignorelist - lists all pokemons not on watchlist", 
            "/ignore <pokemon> - ignores a pokemon", 
            "/watch <pokemon> - restores a pokemon on watchlist",
            "/maxdistance <distance> - sets maximum distance between you and the pokemon (max 200 meters)",
            "/catchable <distance> - sets a catchable distance, pokemons within this range will always be sent (set 0 to disable)",
            "/status - show your current status",
            "/default - set default watchlist and values",
            "" ]
    update.message.reply_text("\n".join(cmd))

def echo(bot, update):
    logger.info(update.message.text)
    update.message.reply_text("Sorry, I dont understand you. Send me /help for a list of commands.")


def job_callback(bot, job):

    user = User.select().where(User.id == job.context).order_by(User.lastupdated).get()
        
    if user.lastupdated is None or (datetime.now() - user.lastupdated).total_seconds() > settings.periodicity:
        url = settings.api
        url = url.replace("LAT", str(user.latitude))
        url = url.replace("LNG", str(user.longitude))

        req = urllib2.Request(url)
        req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01') 
        req.add_header('Connection', 'keep-alive') 
        req.add_header('Origin', 'https://fastpokemap.se')  
        #req.add_header('Accept-Encoding', 'gzip, deflate, sdch, br')  
        req.add_header('Accept-Language', 'sv-SE,sv;q=0.8,en-US;q=0.6,en;q=0.4')  
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36')  
        
        try:
            resp = urllib2.urlopen(req)
            content = resp.read()
        except:
            logging.warn("Something bad happened")
            content = ""

        try:
            data = json.loads(content)
        except ValueError:
            logger.info("No data recieved")
            
        if 'error' in data.keys():
            logger.info("Time to get pokemon status for user " + str(user.id) + " - Server overloaded, retrying in one second")
        elif 'result' in data.keys():
            logger.info("Time to get pokemon status for user " + str(user.id) + " - Fetched new pokemons")
            for pokemon in data['result']:
                vanishes = datetime.fromtimestamp(float(pokemon['expiration_timestamp_ms']) / 1e3)
                vanishesText = vanishes.strftime("%H:%M:%S")
                
                ue, created = UserEncounter.get_or_create(user = user, encounter = pokemon['encounter_id'], expires = vanishes)
                ue.save()
                
                if created:
                    logger.info("Saw new pokemon: " + settings.pokemons[pokemon['pokemon_id']])
                else:
                    logger.info("Got already handled pokemon: " + settings.pokemons[pokemon['pokemon_id']])
                
                if created:
                    try:
                        up = UserPokemons.get(UserPokemons.user == user, UserPokemons.pokemon == pokemon['pokemon_id'])
                    except UserPokemons.DoesNotExist:
                        # its not in our blacklist, signal the user!
                        
                        msg = "Saw " + settings.pokemons[pokemon['pokemon_id']] + ", vanishes " + vanishesText
                        logger.info(msg)
                        latitude = pokemon['latitude']
                        longitude = pokemon['longitude']
                        bot.sendMessage(chat_id=user.id, parse_mode='Markdown', text=msg)
                        bot.send_location(chat_id=user.id, latitude=latitude, longitude=longitude)
                
            logger.info("Done fetching pokemons")
            user.lastupdated = datetime.now()
            user.save()
        else:
            logger.info("Neither error nor result in response..?")



    
def location(bot, update, job_queue):
    message = update.message
    location = message.location
    chat = message.chat
    
    logger.info("Got location " + str(location.latitude) + " " + str(location.longitude) + " for user " + str(chat.id))
 
    u, created = User.get_or_create(id=chat.id, defaults={'latitude': location.latitude, 'longitude': location.longitude, 'active': True, 'lastupdated': datetime.now() })
    u.latitude = location.latitude
    u.longitude = location.longitude
    u.active = True
    
    rows = u.save()
    if rows == 1:
        if created:
            update.message.reply_text("Welcome new user, stored your location")
            set_default(u)
        else:
            update.message.reply_text("Updated your location, activating tracking")
    else:
        logger.warn("Saved something else than one row: " + str(rows))
        
        
    if u.id in jobs:
        logger.info("Job already activated for user")
        return
     
    logger.info("Activating job for user")
    job = Job(job_callback, 1, context=u.id)
    jobs[u.id] = job
    job_queue.put(job)
    

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
   
def ignorelist(bot, update):
    logger.info("ignorelist")
    message = update.message
    chat = message.chat
    update.message.reply_text("Listing pokemons on ignorelist")

    try:
        u = User.get(User.id == chat.id)
    except User.DoesNotExist:
        update.message.reply_text("Please start by setting your location")
        return
    
    il = []
    
    ups = UserPokemons.select().join(User).where(User.id == chat.id)
    for up in ups:
        il.append(settings.pokemons[up.pokemon])
        
    update.message.reply_text("\n".join(il))
        
def watchlist(bot, update):
    logger.info("watchlist")
    message = update.message
    chat = message.chat
    update.message.reply_text("Listing pokemons on watchlist")
    
    try:
        u = User.get(User.id == chat.id)
    except User.DoesNotExist:
        update.message.reply_text("Please start by setting your location")
        return
        
        
    ups = UserPokemons.select().where(UserPokemons.user == u)
    
    wl = []
    
    for p in settings.pokemons:
        show = True
        for up in ups:
            if p == up.pokemon:
                show = False
                
        if show:
            wl.append(settings.pokemons[p])
            
        
    update.message.reply_text("\n".join(wl))
    
    
    
def ignore(bot, update, args):
    logger.info("ignore")
    message = update.message
    chat = message.chat
    
    if len(args) != 1:
        update.message.reply_text("Usage: /ignore <pokemon>, i.e. /ignore pidgey")
        return

    try:
        u = User.get(User.id == chat.id)
    except User.DoesNotExist:
        update.message.reply_text("Please start by setting your location")
        return

    pokemonToFind = args[0]
    
    for p in settings.pokemons:
        if settings.pokemons[p].lower() == pokemonToFind.lower():
        
            up, created = UserPokemons.get_or_create(user = u, pokemon = p)
            rows = up.save()
            update.message.reply_text("Ignoring " + settings.pokemons[p])
            return
    
    update.message.reply_text("Could not find any pokemon named " + pokemonToFind)
    
def watch(bot, update, args):
    logger.info("watch")
    message = update.message
    chat = message.chat
    
    if len(args) != 1:
        update.message.reply_text("Usage: /watch <pokemon>, i.e. /watch pidgey")
        return

    try:
        u = User.get(User.id == chat.id)
    except User.DoesNotExist:
        update.message.reply_text("Please start by setting your location")
        return
        
    pokemonToFind = args[0]
    
    for p in settings.pokemons:
        if settings.pokemons[p].lower() == pokemonToFind.lower():
            query = UserPokemons.delete().where(UserPokemons.user == u, UserPokemons.pokemon == p)
            rows = query.execute() 

            update.message.reply_text("Added " + settings.pokemons[p] + " to watchlist")
            return
    
    update.message.reply_text("Could not find any pokemon named " + message.text)
    
    


def status(bot, update):
    logger.info("status")
    message = update.message
    chat = message.chat
    
    try:
        u = User.get(User.id == chat.id)
    except User.DoesNotExist:
        update.message.reply_text("Please start by setting your location")
        return
        
    if u.active:
        update.message.reply_text("You are active at " + str(u.latitude) + " " + str(u.longitude))
        lastupdated_text = u.lastupdated.strftime("%H:%M:%S")
        update.message.reply_text("Last check for pokemons: " + lastupdated_text)
        
    else:
        update.message.reply_text("You are inactive")
    
def stop(bot, update, job_queue):
    logger.info("stop")
    message = update.message
    chat = message.chat
    
    try:
        u = User.get(User.id == chat.id)
    except User.DoesNotExist:
        update.message.reply_text("Please start by setting your location")
        return
    
    u.active = False
    rows = u.save()
    
    if rows == 1:
        update.message.reply_text("You are deactivated")
    else:
        logger.warn("Saved something else than one row: " + str(rows))
        
    if u.id in jobs:
        jobs[u.id].schedule_removal()
        del jobs[u.id]
        logger.info("Removing job")
        return
        
    logger.info("No job to remove for user")

   
def maxdistance(bot, update):
    logger.info("maxdistance")
    update.message.reply_text("Not yet implemented")

def catchable(bot, update):
    logger.info("catchable")
    update.message.reply_text("Not yet implemented")    


def set_default(u):
    # delete all in ignorelist
    query = UserPokemons.delete().where(UserPokemons.user == u)
    rows = query.execute() 
    
    for p in settings.ignore_default:
        up, created = UserPokemons.get_or_create(user = u, pokemon = p)
        up.save()
    
def default(bot, update):
    logger.info("default")
    update.message.reply_text("Defaulting your settings, check ignorelist/watchlist")    
    
    message = update.message
    chat = message.chat
    
    try:
        u = User.get(User.id == chat.id)
    except User.DoesNotExist:
        update.message.reply_text("Please start by setting your location")
        return

    set_default(u)
        
        
def gc_callback(bot, job):
    c = UserEncounter.select().where(UserEncounter.expires < datetime.now()).count()
    t = UserEncounter.select().count()
    logger.info("Garbage collecting " + str(c) + " of total " + str(t) + " rows in UserEncounter")
    
    query = UserEncounter.delete().where(UserEncounter.expires < datetime.now())
    c = query.execute()

                
def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(settings.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("stop", stop, pass_job_queue=True))
    dp.add_handler(CommandHandler("ignorelist", ignorelist))
    dp.add_handler(CommandHandler("watchlist", watchlist))
    dp.add_handler(CommandHandler(command="ignore", callback=ignore, pass_args=True))
    dp.add_handler(CommandHandler(command="watch", callback=watch, pass_args=True))
    dp.add_handler(CommandHandler("maxdistance", maxdistance))
    dp.add_handler(CommandHandler("catchable", catchable))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("default", default))

    dp.add_handler(MessageHandler([Filters.text], echo))
    dp.add_handler(MessageHandler([Filters.location], location, pass_job_queue=True))
    dp.add_handler(MessageHandler([Filters.command], echo))
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    
    users = User.select().where(User.active == True)
    
    for user in users:
        logger.info("Activating job for user " + str(user.id))
        job = Job(job_callback, 1, context=user.id)
        jobs[user.id] = job
        updater.job_queue.put(job)        
    
    job = Job(gc_callback, settings.garbage_collect)
    updater.job_queue.put(job)   
    
    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()
    
    updater.idle()
    
    
    # stop_signals=(SIGINT, SIGTERM, SIGABRT)
    # for sig in stop_signals:
        # signal(sig, updater.signal_handler)
        
    # updater.is_idle = True
    
    # while updater.is_idle:
        # time.sleep(1)
        

if __name__ == '__main__':
    main()
