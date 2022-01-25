import discord
import os
import datetime
from discord.ext import commands, tasks
import asyncio
from keep_alive import keep_alive

client = commands.Bot(command_prefix="!z ")
client.remove_command('help')

sleeprem = {}

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.idle, activity=discord.Game('Type !z help'))

	time_delay = (datetime.datetime.now() - datetime.timedelta(seconds=datetime.datetime.now().second) + datetime.timedelta(minutes=1)) - 	datetime.datetime.now()
	print("Waiting to recover from offset of: " + str(time_delay.total_seconds()) + "...")
	await asyncio.sleep(time_delay.total_seconds())
	check_time.start()
	print("Timer Started!")

@client.command()
async def help(ctx):
	embed = discord.Embed(
		title="COMMANDS",
		description="!z sleep [24h time]\nSets a time for you to sLeEp\n\n!z cancel\nCancels any sleep reminder you have\n\n!z current\nLists all ongoing sleep reminders\n\n!z about\nLearn about me :D", color=discord.Colour.purple())
	await ctx.send(embed=embed)

@client.command()
async def about(ctx):
    embed = discord.Embed(
        title="ABOUT",
        description=
        "I made this bot to force me to sleep and have no intention rn to make it usable to anyone but me but I might add timezones and such later 0-0",
        color=discord.Colour.purple())
    await ctx.send(embed=embed)

@client.command()
async def current(ctx):
  sleeprems = ""
  for k,v in sleeprem.items():
	  esttime = v[0] - datetime.timedelta(hours=4)
	  esttime = esttime.strftime("%H:%M")
	  sleeprems += k.display_name + " @ " + esttime + "\n"
  embed = discord.Embed(title="CURRENT SLEEP REMINDERS", description=sleeprems, color=discord.Colour.purple())
  await ctx.send(embed=embed)

@client.command()
async def sleep(ctx, arg):
	try:
		target = datetime.datetime.strptime(arg,"%H:%M")
		now = datetime.datetime.now()
		target = datetime.datetime(now.year,now.month,now.day,target.hour,target.minute)
		target += datetime.timedelta(hours=4)
		sleeprem[ctx.author] = [target, ctx]
		await ctx.send(f"{ctx.author.mention} Ok. I will put you to sleep at {arg}.")
	except ValueError:
		await ctx.send("Please enter a valid time, type !z help for commands")

@client.command()
async def cancel(ctx):
	user = ctx.author
	if user in sleeprem:
		del sleeprem[user]
		await ctx.send(f"{user.mention} Ok. I won't put you to sleep anymore.")

async def kill(user):
	voice_state = user.voice
	if voice_state is not None:
		await user.edit(voice_channel=None)

@tasks.loop(seconds=60)
async def check_time():
	# go through each person in the dictionary and see if they need to be killed
	now = datetime.datetime.now()
	for k,v in sleeprem.items():
		if v[0].hour == now.hour and v[0].minute == now.minute:
			await kill(k)
			await v[1].send(f"{k.mention} GO TO SLEEP SLUMBERRRR")

keep_alive()
client.run(os.environ['TOKEN'])
