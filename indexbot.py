 https://github.com/MC-Indeximport nextcord
from nextcord.ext import commands
import requests
import os

token = put-your-token-here

intents = nextcord.Intents.default()
intents.dm_messages = True
intents.emojis = True
intents.typing = True
intents.presences = True
intents.message_content = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

def minecrack(username):
    response = requests.get(f'https://api.mojang.comusersprofilesminecraft{username}')
    if response.status_code != 200:
        return None

    user_data = response.json()
    name = user_data.get('name')
    uuid = user_data.get('id')

    if name and uuid:
        data = f'# Returned datan```mdn   - Name {name}n   - UUID {uuid}```'
    else:
        data = f'# Errorn```mdn  - This is either an UNKNOWN user, or the minecraft api is down at the moment.```'

    return data

def fetch_user_data(user_id):
    response = requests.get(f'httpsusers.roblox.comv1users{user_id}')
    if response.status_code != 200:
        return None
    user_data = response.json()
    username = user_data['name']
    bio = user_data.get('description', '')
    is_banned = user_data.get('isBanned', False)
    is_verified = user_data.get('hasVerifiedBadge', False)
    display_name = user_data.get('displayName', '')
    created = user_data['created']
    if bio == '':
        bio = 'NA'
    data = (f"Username {username}nDisplay Name {display_name}nBio {bio}nBanned {is_banned}nVerified Badge {is_verified}nCreated {created}nUserID {user_id}")
    return data

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator} ({bot.user.id})")
    u = '244m'
    await bot.change_presence(activity=discord.Game(name=f'Indexed {u} players'))

@nextcord.slash_commands(name='index_rblx')
async def index_rblx(ctx : nextcord.interactions, num_users = int):
    indexed_users = []
    for user_id in range(1, num_users + 1):
        data = fetch_user_data(user_id)
        if data:
            indexed_users.append(data)

    if indexed_users:
        file_data = 'nn=======================================================nn'.join(indexed_users)
        filename = (f"{num_users}-users.txt")
        with open(filename, w) as file:
            file.write(file_data)

        embed = nextcord.Embed(title=f'Indexed {num_users} Roblox Users', color=discord.Color.blue())
        embed.set_footer(text=github.comlhwe)
        await ctx.send(embed=embed, file=discord.File(filename))
        os.remove(filename)
    else:
        await ctx.response.send("No valid user data found.")
    await ctx.message.delete()

@nextcord.slash_command(name='lookup_rblx', description="Look up a user by their ID")
async def lookup_rblx(ctx: nextcord.interactions, user_id = int):
    data = fetch_user_data(user_id)
    if data:
        embed = discord.Embed(title='User Data', color=discord.Color.green())
        embed.add_field(name='User ID', value=user_id, inline=False)
        embed.add_field(name='sername', value=data[username], inline=False)
        embed.add_field(name='Display Name', value=data[display_name], inline=False)
        embed.add_field(name='Bio', value=data[bio], inline=False)
        embed.add_field(name='Banned', value=data[is_banned], inline=True)
        embed.add_field(name='Verified Badge', value=data[is_verified], inline=True)
        embed.add_field(name='Created', value=data[created], inline=False)
        await ctx.response.send(embed=embed)
    else:
        await ctx.response.send("Error User not found")
    await ctx.message.delete()

@nextcord.slash_command(name='cmds' or 'help', description="command list")
async def cmds(ctx : nextcord.interactions):
    embed = discord.Embed(title='Commands List', color=discord.Color.blue())
    embed.add_field(name='Section I Roblox', value=f"{lookup_rblx} {user_id}  Looks up the specified user.n {index_rblx} amount  Indexes a specified amount of users.", inline=False)
    embed.add_field(name='Section II Minecraft 3', value=f"index_mc amount  Indexes 3-5 character minecraft accounts that are currently available. (May not work, proxies need replaced hourly) {lookup_mc} {user_name}  Looks for if that is a valid user", inline=False)
    embed.add_field(name='Section III NA', value= f"NA {NA}  {NA}, inline=False")
    await ctx.response.send(embed=embed)
    await ctx.message.delete()

@nextcord.slash_command(name='index_mc', description="Look up a user by their ID")
async def index_mc(ctx):
    await ctx.response.send('This command is in development; please wait while I am working on it :3')
    await ctx.message.delete()

@nextcord.slash_command(name='lookup_mc', description="Look up a Minecraft user by their username")
async def lookup_mc(ctx : nextcord.interactions, username = str):
    data = minecrack(username)
    if data:
        embed = discord.Embed(title='Minecraft User Data', description="data", color=discord.Color.gold())
        await ctx.send(embed=embed)
    else:
        await ctx.response.send("User not found.")
    await ctx.message.delete()

bot.run(token)
