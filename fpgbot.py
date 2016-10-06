#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, StringCommandHandler, Job
from telegram.ext.dispatcher import run_async
import logging
import time
from signal import signal, SIGINT, SIGTERM, SIGABRT
import settings
from datetime import datetime
import urllib2, json
import store
from geopy.distance import vincenty

from flask import Flask, request, abort

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
worker_callback = Flask(__name__)
updater = None

@worker_callback.route('/',methods=['POST'])
def trigger_alert():
    global updater

    logger.debug("POST request received from %s." % (request.remote_addr))
    data = json.loads(request.data)
    if data['type'] == 'pokemon':
        pokemon_lat = data['message']['latitude']
        pokemon_lng = data['message']['longitude']
        pokemon_id = data['message']['pokemon_id']
        pokemon_encounter = data['message']['encounter_id']
        pokemon_disappear_time = data['message']['disappear_time']
        pokemon = settings.pokemon_id[pokemon_id]
        pokemon_name = settings.pokemons[pokemon]

        pokemon_vanishes = datetime.fromtimestamp(float(pokemon_disappear_time))
        pokemon_vanishesText = pokemon_vanishes.strftime("%H:%M:%S")

        users = store.get_active_users()
        for user in users:
            user_pos = (user.latitude, user.longitude)
            pokemon_pos = (pokemon_lat, pokemon_lng)
            dist = vincenty(user_pos, pokemon_pos).meters

            distance_check = dist < user.normal_distance
            whitelist_check = store.check_user_pokemon_whitelist(user, pokemon)

            if distance_check and whitelist_check:
                ue, created = store.get_or_create_userencounters(user = user, encounter = pokemon_encounter, expires = pokemon_vanishes)
                
                if created:
                    logger.info("Got new pokemon to report: %s with distance of %d" % (pokemon_name, dist, ))
                    msg = "Saw " + pokemon_name + ", vanishes " + pokemon_vanishesText
                    logger.info(msg)

                    bot = updater.bot
                    bot.sendMessage(chat_id=user.id, parse_mode='Markdown', text=msg)
                    bot.send_location(chat_id=user.id, latitude=pokemon_lat, longitude=pokemon_lng)
                else:
                    logger.info("Got already handled pokemon: " + pokemon_name)
            else:
                logger.info("Got pokemon too far away or not on whitelist: %s (%d m)" % (pokemon_name, dist, ))

    return "OK"

@run_async
def job_callback(bot, job):
    worker_callback.run(host='0.0.0.0',port='12344')

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
    
def location(bot, update):
    message = update.message
    location = message.location
    chat = message.chat
    
    logger.info("Got location " + str(location.latitude) + " " + str(location.longitude) + " for user " + str(chat.id))
 
    u, created = store.get_or_create_user(id=chat.id, defaults={'latitude': location.latitude, 'longitude': location.longitude, 'active': True, 'lastupdated': datetime.now() })

    if created:
        update.message.reply_text("Welcome new user, stored your location")
        set_default(u)
    else:
        update.message.reply_text("Updated your location, activating tracking")
        u.latitude = location.latitude
        u.longitude = location.longitude
        u.active = True
        u.save()
    
    url = settings.url % (u.latitude,u.longitude,)
    logging.info("Trying to set new location at %s" % url)
    req = urllib2.Request(url, data="")
    req.add_header('Accept-Encoding', 'gzip, deflate') 
    req.add_header('Accept-Language', 'sv-SE,sv;q=0.8,en-US;q=0.6,en;q=0.4')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36') 
    req.add_header('Accept', '*/*') 
    req.add_header('X-Requested-With', 'XMLHttpRequest') 
    req.add_header('Connection', 'keep-alive') 
    req.add_header('Content-Length', '0')     

    resp = urllib2.urlopen(req)
    content = resp.read()
    logging.info("New position set")
    

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))
   
def ignorelist(bot, update):
    logger.info("ignorelist")
    message = update.message
    chat = message.chat
    update.message.reply_text("Listing pokemons on ignorelist")

    u = store.get_user(chat.id)
    if u is None:
        update.message.reply_text("Please start by setting your location")
        return
    
    il = []
    
    ups = store.get_user_pokemons(chat.id)
    for up in ups:
        il.append(settings.pokemons[up.pokemon])
        
    update.message.reply_text("\n".join(il))
        
def watchlist(bot, update):
    logger.info("watchlist")
    message = update.message
    chat = message.chat
    update.message.reply_text("Listing pokemons on watchlist")
    
    u = store.get_user(chat.id)
    if u is None:
        update.message.reply_text("Please start by setting your location")
        return
        
        
    ups = store.get_user_pokemons(chat.id)
    
    wl = []
    
    for p in settings.pokemons:
        show = True
        for up in ups:
            if p == up.pokemon:
                show = False
                
        if show:
            wl.append(settings.pokemons[p])
            
        
    update.message.reply_text("\n".join(wl))
    
def get_pokemon_by_name(pokemon_to_find):
    for p in settings.pokemons:
        if settings.pokemons[p].lower() == pokemon_to_find.lower():
            return p

    return None
    
def ignore(bot, update, args):
    logger.info("ignore")
    message = update.message
    chat = message.chat
    
    if len(args) != 1:
        update.message.reply_text("Usage: /ignore <pokemon>, i.e. /ignore pidgey")
        return

    u = store.get_user(chat.id)
    if u is None:
        update.message.reply_text("Please start by setting your location")
        return

    pokemon_to_find = args[0]
    
    p = get_pokemon_by_name(pokemon_to_find)
    if p:
        up, created = store.get_or_create_userpokemons(u, p)
        update.message.reply_text("Ignoring " + settings.pokemons[p])
    else:
        update.message.reply_text("Could not find any pokemon named " + pokemon_to_find)
    
def watch(bot, update, args):
    logger.info("watch")
    message = update.message
    chat = message.chat
    
    if len(args) != 1:
        update.message.reply_text("Usage: /watch <pokemon>, i.e. /watch pidgey")
        return

    u = store.get_user(chat.id)
    if u is None:
        update.message.reply_text("Please start by setting your location")
        return
        
    pokemon_to_find = args[0]
    
    p = get_pokemon_by_name(pokemon_to_find)
    if p:
        rows = store.delete_userpokemons(u, p)
        update.message.reply_text("Added " + settings.pokemons[p] + " to watchlist")
    else:
        update.message.reply_text("Could not find any pokemon named " + message.text)
    


def status(bot, update):
    logger.info("status")
    message = update.message
    chat = message.chat
    
    u = store.get_user(chat.id)
    if u is None:
        update.message.reply_text("Please start by setting your location")
        return
        
    if u.active:
        update.message.reply_text("You are active at " + str(u.latitude) + " " + str(u.longitude))
        lastupdated_text = u.lastupdated.strftime("%H:%M:%S")
        update.message.reply_text("Last check for pokemons: " + lastupdated_text)
        
    else:
        update.message.reply_text("You are inactive")
    
def stop(bot, update):
    logger.info("stop")
    message = update.message
    chat = message.chat
    
    u = store.get_user(chat.id)
    if u is None:
        update.message.reply_text("Please start by setting your location")
        return
    
    u.active = False
    rows = u.save()
    
    if rows == 1:
        update.message.reply_text("You are deactivated")
   
def maxdistance(bot, update, args):
    logger.info("maxdistance")
    message = update.message
    chat = message.chat

    u = store.get_user(chat.id)
    if u is None:
        update.message.reply_text("Please start by setting your location")
        return

    if len(args) != 1:
        update.message.reply_text("Usage: /watch <pokemon>, i.e. /watch pidgey")
        return

    u.normal_distance = int(args[0])
    rows = u.save()
    
    if rows == 1:
        update.message.reply_text("maxdistance is set to %s" % args[0])

def catchable(bot, update):
    logger.info("catchable")
    update.message.reply_text("Not yet implemented")    


def set_default(u):
    # delete all in ignorelist
    store.delete_all_userpokemons(u)
    
    for p in settings.ignore_default:
        up, created = store.get_or_create_userpokemons(u,p)
    
def default(bot, update):
    logger.info("default")
    update.message.reply_text("Defaulting your settings, check ignorelist/watchlist")    
    
    message = update.message
    chat = message.chat
    
    u = store.get_user(chat.id)
    if u is None:
        update.message.reply_text("Please start by setting your location")
        return

    set_default(u)
        
        
def gc_callback(bot, job):
    c, t = store.garbage_collect()
    logger.info("Garbage collecting " + str(c) + " of total " + str(t) + " rows in UserEncounter")

def main():
    global updater
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(settings.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("ignorelist", ignorelist))
    dp.add_handler(CommandHandler("watchlist", watchlist))
    dp.add_handler(CommandHandler(command="ignore", callback=ignore, pass_args=True))
    dp.add_handler(CommandHandler(command="watch", callback=watch, pass_args=True))
    dp.add_handler(CommandHandler("maxdistance", maxdistance, pass_args=True))
    dp.add_handler(CommandHandler("catchable", catchable))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("default", default))

    dp.add_handler(MessageHandler([Filters.text], echo))
    dp.add_handler(MessageHandler([Filters.location], location))
    dp.add_handler(MessageHandler([Filters.command], echo))
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    
    users = store.get_all_users()
    
    job = Job(gc_callback, settings.garbage_collect)
    updater.job_queue.put(job)   

    job = Job(job_callback, 0, repeat=False)
    updater.job_queue.put(job)   

    updater.idle()
       

if __name__ == '__main__':
    main()
