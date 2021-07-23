import discord
from discord.ext import commands
from imdb import IMDb
import config as cf


imdb = IMDb()
bot = commands.Bot(command_prefix = cf.PREFIX)


@bot.event
async def on_ready():		
	print("Bot online.")
	await bot.change_presence(activity=discord.Game(name = cf.STATUS)) # Controls bot's Discord status
	
bot.remove_command("help")	# Removes default help embed, adds new one
help_embed = discord.Embed(title = "Bot Commands", description = "List of commands.")
help_embed.add_field(name = "ping", value = "Displays the current latency in ms", inline = False)
help_embed.add_field(name = "imdb <movie name>", value = "Searches IMDb for movie info", inline = False)
help_embed.add_field(name = "help", value = "Displays a list of commands", inline = False)


@bot.command() # Displays help embed message
async def help(ctx):
	await ctx.send(embed = help_embed)

 
@bot.command() # Displays the current latency in ms
async def ping(ctx):
	await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command() # Main command for finding movie information
async def imdb(ctx,*,args):
	await ctx.send(f"searching IMDb for: {args}...")

	movie = imdb.search_movie(args)
	ID = movie[0].movieID
	movie = imdb.get_movie(ID)

	embed_title = (movie['long imdb title'])
	

	try:
		x = []
		actors = movie['cast']
		for actor in actors[:4]:
			x.append(actor['name'])
			embed_cast = ", ".join(x)
	except:
		embed_cast = "No cast found"


	try:
		x = []
		for director in movie['director']:
			x.append(director['name'])
			embed_dir = ", ".join(x)
	except:
		embed_dir = "No director found."


	try:
		embed_plot = (movie['plot outline'])
		if len(embed_plot)<1024:
			embed = discord.Embed(title = "IMDb Search Results", color = 0xdd0e0e)
			embed.add_field(name = "Plot", value = embed_plot, inline = False)
		else:
			embed = discord.Embed(description = embed_plot,title = "IMDb Search Results", color = 0xdd0e0e)
	except:
		embed = discord.Embed(title = "IMDb Search Results", color = 0xdd0e0e)
	

	try:
		embed_poster = (movie['full-size cover url'])
	except:
		embed_poster = "https://img2.pngio.com/documentation-screenshotlayer-api-default-png-250_250.png" # Placeholder image for when poster not found


	embed.set_image(url = embed_poster)
	embed.add_field(name = "Title", value = embed_title, inline = False)
	embed.add_field(name = "Director", value = embed_dir, inline = False)
	embed.add_field(name = "Cast", value = embed_cast, inline = False)
	embed.set_footer(text = "powered by IMDbPY")

	await ctx.send(embed = embed)
	
token = cf.TOKEN
bot.run(token)
