import discord
import datetime
from discord import embeds
from discord.colour import Color
import requests
import random
import os
import json
from discord import channel
from discord.ext import commands, tasks
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound

#--------------------------------------------------------------------------

#esconder o token
#if os.path.exists(os.getcwd() + "/config.json"):

    #with open("./config.json") as f:
        #configData = json.load(f)
#else:
    #configTemplate = {"Token": "", "Prefix": "!"}

    #with open(os.getcwd() + "/config.json", "w+") as f:
        #json.dump(configTemplate, f)

#token = configData["Token"]
#prefix = configData["Prefix"]

#--------------------------------------------------------------------------

bot = commands.Bot("!")



@bot.event
async def on_ready():
    print(f"imperador do universo ta on, todos saudam o {bot.user}")
    current_time.start()

# --------------------------------------------------------------------------

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "palavrão" in message.content:
        await message.channel.send(f"por favor seja respeitoso, {message.author.name}")

        await message.delete()

    await bot.process_commands(message)

# --------------------------------------------------------------------------

#adicionar cargo a partir de reacões
@bot.event
async def on_reaction_add(reaction, user):
    print(reaction.emoji)
    if reaction.emoji == "✅":
        role = user.guild.get_role(898980112094068737)
        #o python reconhece os servidores do discord como "guild"
        await user.add_roles(role)

    elif reaction.emoji == "💩":
        role = user.guild.get_role(898981918652121169)
        await user.add_roles(role)

# --------------------------------------------------------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,MissingRequiredArgument):
        await ctx.send("favor enviar todos os argumentos. digite !help para ver os parametros de cada comando")

    elif isinstance(error,CommandNotFound):
        await ctx.send("comando nao existe. digite !help para ver os parametros de cada comando")
    else:
        raise error

# --------------------------------------------------------------------------

@bot.command(name="oi", help="enviar um oi(não requer argumento).")
async def send_hello(ctx):
    name = ctx.author.name

    response = "ola, " + name

    await ctx.send(response)

# --------------------------------------------------------------------------

@bot.command(name="calcular", help="calcula uma expressã. argumentos: expressoes (sinal de mais + e tals...)")
async def calculate_expression(ctx, *expression):
    expression = "".join(expression)

    print(expression)

    response = eval(expression)

    await ctx.send("a resposta é: " + str(response))

# --------------------------------------------------------------------------

#pedir para verificar algo em um site como exemplo abaixo verificar bit coin
@bot.command(help= "vertifica o preço de uma par na binance. argumentos: moeda base")
async def binance(ctx, coin, base ):
    try:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}{base.upper()}")

        data = response.json()
        price = data.get("price")

        if price:
            await ctx.send(f"o valor do par {coin}/{base} é {price}")

        else:
            await ctx.send(f"o par {coin}/{base} é invalido")
    except Exception as error:
        await ctx.send("ops ... deu algum erro!")
        print(error)

# --------------------------------------------------------------------------

#mensagem via pv
@bot.command(name="dm" , help="enviar uma mensagem no privado(não requer argumento).")
async def dm(ctx):
    try:
        await ctx.author.send("salve irmão")
        await ctx.author.send("tranquilo ?")
    except discord.errors.Forbidden:
        await ctx.send("desabilita essa merda ai pra poder te mandar dm")

# --------------------------------------------------------------------------

@bot.command(name="horas", help="retorna a hora atual(não requer argumento).")
async def send_hello(ctx):
    now = datetime.datetime.now()

    now = now.strftime("%H:%M:%S")

    await ctx.send("agora são "+ now)

# --------------------------------------------------------------------------

@bot.command(name="sorte" , help="retorna se vc tirou impar ou par(não requer argumento).")
async def ran_dom(ctx):
    number = random.randint (1, 2)

    if number == 1:
        await ctx.send("impar")
    if number == 2:
        await ctx.send("par" )

# --------------------------------------------------------------------------

#exibe um card mostrado uma foto e algumas informações
@bot.command(name="fotos", help="enviar uma foto aleatoria(não requer argumento).")
async def get_random_image(ctx):
    url_image = "https://picsum.photos/1920/1080"

    embed = discord.Embed(
        title = "resultado da busca de imagem",
        description = "PS: a busca é totalmente aleatoria",
        color = 0x0000FF,
    )

    embed.set_author(name = bot.user.name, icon_url = bot.user.avatar_url)
    embed.set_footer(text="feito por" + bot.user.name, icon_url = bot.user.avatar_url)

    embed.add_field(name= "API", value="usamos a API do https://picsum.photos")
    embed.add_field(name="parametros", value="{largura}/{altura}")

    embed.add_field(name="exemplo", value=url_image, inline=False)

    embed.set_image(url=url_image)

    await ctx.send(embed=embed)

# --------------------------------------------------------------------------

@bot.command(name="comandos", help="apresenta a lista de comandos(não requer argumento).")
async def comandos(ctx):
    embed = discord.Embed(
        title = "Lista de Comandos",
        description = "!comandos   !oi   !calcular (aqui adicione a operação matematica sem os parenteses)   !binance btc usdt   !dm   !horas   !sorte   !fotos",
        color = 0x0000FF,
    )

    await ctx.send(embed=embed)

# --------------------------------------------------------------------------

# aqui é uma tarefa onde o bot fica mandando de tempo em tempo
@tasks.loop(minutes=30)
async def current_time():
    now = datetime.datetime.now()

    now = now.strftime("%d/%m/%Y às %H:%M:%S")

    channel = bot.get_channel(898575454741610536)

    await channel.send("Data atual: "+ now)

# --------------------------------------------------------------------------
bot.run("aqui vai o token do bot")