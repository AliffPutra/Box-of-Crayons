# ------------------------------------------------------------
# Discord Trading bot for Sim Companies 
#
# Owner  			:	Aliff Putra
# Version	 		:	1.0.0      
# Update  	 		:	25/5/21
# 
#
# -------------------------Dev notes-------------------------- 
# Testing feature line 45 - 50.
# asyncio module will be removed in the future.
# API is working. It is pulling power data from exchange,
# Data from API however is not sorted.
# Token to be renamed. Adding more items in the future.
# Account feature completed. Em/code.
# Open Account manually feature not implemented.
# Balance feature redundant. Commented for ref. Line 154 - 163. 
# Bag command commented for feature removal. Line 214 - 234.
# 
# ------------------------------------------------------------

import discord
from discord.ext import tasks, commands
from discord.utils import find
from datetime import datetime
import json
import requests
import os
import random
import asyncio
import threading
import numpy as np

#r = requests.get('https://www.simcompanies.com/api/market/1')## Number /1 is power
# r = requests.get('https://spreadsheets.google.com/feeds/cells/13ZLn_1jvbRt6Fghx6Ajqkumpc4wg1S_VpFGS4CFJiiY/4/public/full?alt=json')
# packages_json = r.json()

# price = packages_json['price']

os.chdir("D:\\Work\\Programming\\Sublime Text\\Projects")

bot = commands.Bot(command_prefix = "!", help_command = None)
token = [{"name":"Token","price":1000,"description":"It is a token"}] ##token dictionary

## Testing embeded using !test ##
# @bot.command()
# async def test(ctx):
# 	output = discord.Embed(title = f"{ctx.author.name}'s id", color = discord.Color.green())
# 	output.add_field(name = "User Id", value = ctx.author.id)
# 	await ctx.send(embed = output)

## Dictionary ##

@bot.event 
async def on_ready(): ## Copy & Paste to add multiple channels ##
	 await bot.get_channel(842325268207108106).send("Hello, butler is online. To start using, type `!butler`")	 

async def open_account(user):
	users = await get_bank_data()
	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["Balance"] = 150
	with open("bank.json","w") as f:
		json.dump(users,f)
	return True

async def get_bank_data(): 
	with open("bank.json","r") as f:
		users = json.load(f)
	return users

async def update_bank(): 
	with open("bank.json","r") as f:
		users = json.load(f)
	return users

async def update_bank(user, change = 0, mode ="Balance"):
	users = await get_bank_data()
	users [str(user.id)][mode] += change

	with open("bank.json","w") as f:
		json.dump(users,f)

	bal = [users[str(user.id)]["Balance"]]
	return bal


@bot.command() ##Main page
async def butler(ctx):
	em = discord.Embed(title = "Sim Companies Exchange Trade Fund", description = "Hello, how can I be of service to you?")
	em.add_field(name = "Account", value = "Account related inquries, type `!account`")
	em.add_field(name = "Trade", value = "Trade related inquires, type `!trade`", inline = False)
	em.add_field(name = "Market", value = "Market related inquires, type `!market`", inline = False)
	em.add_field(name = "Language", value = "Work in progress", inline = False)

	await ctx.send(embed = em)

@bot.command()
async def account(ctx):
	em = discord.Embed(title = "Sim Companies Exchange Trade Fund", description = "These are the options for account related inquires")
	em.add_field(name = "Account Information", value = "Latest information on your account information, type `!ainfo`")
	em.add_field(name = "Portfolio", value = "To view your investment portfolio, type `!aport`", inline = False)

	await ctx.send(embed = em)

@bot.command()
async def ainfo(ctx):
	user = ctx.author
	users = await get_bank_data()
	bank_amt = users[str(user.id)]["Balance"]
	em = discord.Embed(title =f"{ctx.author.name}'s Account", description = "These are the options for account related inquires")
	em.add_field(name = "Account number", value = str(user.id))
	em.add_field(name = "Balance amount", value = bank_amt, inline = False)

	await ctx.send(embed = em)

@bot.command()
async def aport(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title =f"{ctx.author.name}'s Portfolio", description = "This is your current investment portfolio.")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)


@bot.command()
async def trade(ctx): ##Trade inquries
	em = discord.Embed(title = "Sim Companies Exchange Trade Fund", description = "These are the availible options for you to trade.")
	em.add_field(name = "Commodities", value = "Latest information on commodities prices, type `!cp`", inline = False)
	em.add_field(name = "Bonds", value = "Latest information on corporate bonds, type `!bonds`", inline = False)

	await ctx.send(embed = em)

@bot.command()
async def cp(ctx): ##KIV value not working due to JSON not sorted.
	em = em = discord.Embed(title = "Sim Companies Exchange Trade Fund", description = "These are the latest information on commodities prices.")
	em.add_field(name = "Power", value = packages_json, inline = False)

	await ctx.send(embed = em)


# @bot.command()
# async def balance(ctx): ##Balance portion
# 	await open_account(ctx.author) ##Open an account if it is not an existing user
# 	user = ctx.author
# 	users = await get_bank_data()
# 	wallet_amt = users[str(user.id)]["Balance"]
# 	em= discord.Embed(title =f"{ctx.author.name}'s balance", color = discord.Color.red())
# 	em.add_field(name = "Balance", value = wallet_amt)

# 	await ctx.send(embed = em)


## Earning portion needs to be reworked.
@bot.command()
async def earn(ctx):
	await open_account(ctx.author)
	user = ctx.author
	users = await get_bank_data()
	earnings = random.randint(0, 1000)
	wallet_amt = users[str(user.id)]["Balance"]

	await ctx.send(f"You made {earnings} dollars")

	users[str(user.id)]["Balance"] += earnings
	with open("bank.json","w") as f:
		json.dump(users,f)

	em= discord.Embed(title =f"{ctx.author.name}'s balance", color = discord.Color.red())
	em.add_field(name = "Balance", value = wallet_amt)

	await ctx.send(emded = em)

## TESTING PORTION
@bot.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in token:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)



@bot.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your bank to buy {amount} {item}")
            return


    await ctx.send(f"You've just bought {amount} {item}")

## BAG COMMAND ##
# @bot.command()
# async def bag(ctx):
#     await open_account(ctx.author)
#     user = ctx.author
#     users = await get_bank_data()

#     try:
#         bag = users[str(user.id)]["bag"]
#     except:
#         bag = []


#     em = discord.Embed(title = "Bag")
#     for item in bag:
#         name = item["item"]
#         amount = item["amount"]

#         em.add_field(name = name, value = amount)    

#     await ctx.send(embed = em)

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in token:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"Balance")

    return [True,"Worked"]


@bot.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("I'm sorry but that item does not exist")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You've just sold {amount} {item}.")

## KIV sell algorithm needs to be complex
async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    ran = np.random.randint(-80,35)
    for item in token:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = ran* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("bank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"Balance")

    return [True,"Worked"]



bot.run('TOKEN')
