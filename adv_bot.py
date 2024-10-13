
import numpy as np
import requests
import json
import inspect
import sys
import discord  # Make sure to import discord to use discord.Member

from colorama import Fore, Style, just_fix_windows_console

just_fix_windows_console()

# Make sure that the user is running Python 3.8 or higher
if sys.version_info < (3, 8):
    exit("Python 3.8 or higher is required to run this bot!")

# Now make sure that the discord.py library is installed or/and is up to date
try:
    from discord import app_commands, Intents, Client, Interaction
except ImportError:
    exit(
        "Either discord.py is not installed or you are running an older and unsupported version of it."
        "Please make sure to check that you have the latest version of discord.py! (try reinstalling the requirements?)"
    )

# ASCII logo, uses Colorama for coloring the logo.
logo = f"""
{Fore.LIGHTBLUE_EX}       {Fore.GREEN}cclloooooooooooooo.
{Fore.LIGHTBLUE_EX},;;;:{Fore.GREEN}oooooooooooooooooooooo.
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}oooooo{Fore.WHITE}kKXK{Fore.GREEN}ooo{Fore.WHITE}NMMWx{Fore.GREEN}ooooo:..
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}oooooo{Fore.WHITE}XMMN{Fore.GREEN}oooo{Fore.WHITE}XNK0x{Fore.GREEN}dddddoo
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}looo{Fore.WHITE}kNMMWx{Fore.GREEN}ooood{Fore.BLUE}xxxxxxxxxxxxxo
{Fore.LIGHTBLUE_EX};;;;{Fore.GREEN}ld{Fore.WHITE}kXXXXK{Fore.GREEN}ddddd{Fore.BLUE}xxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.LIGHTBLUE_EX};;{Fore.BLUE}xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
{Fore.BLUE}ldxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx{Fore.RESET}
"""

print(logo + inspect.cleandoc(f"""
    Hey, welcome to the active developer badge bot.
    Please enter your bot's token below to continue.

    {Style.DIM}Don't close this application after entering the token
    You may close it after the bot has been invited and the command has been run{Style.RESET_ALL}
"""))

try:
    with open("config.json") as f:
        config = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    config = {}

while True:
    token = config.get("token", None)
    if token:
        print(
            f"\n--- Detected token in {Fore.GREEN}./config.json{Fore.RESET} "
            "(saved from a previous run). Using stored token. ---\n"
        )
    else:
        token = input("> ")

    try:
        r = requests.get(
            "https://discord.com/api/v10/users/@me",
            headers={"Authorization": f"Bot {token}"}
        )
        data = r.json()
    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.ConnectionError):
            exit(
                f"{Fore.RED}ConnectionError{Fore.RESET}: "
                "Discord is commonly blocked on public networks, "
                "please make sure discord.com is reachable!"
            )

        elif isinstance(e, requests.exceptions.Timeout):
            exit(
                f"{Fore.RED}Timeout{Fore.RESET}: "
                "Connection to Discord's API has timed out "
                "(possibly being rate limited?)"
            )

        exit(f"Unknown error has occurred! Additional info:\n{e}")

    if data.get("id", None):
        break

    print(
        f"\nSeems like you entered an {Fore.RED}invalid token{Fore.RESET}. "
        "Please enter a valid token (see Github repo for help)."
    )

    config.clear()

with open("config.json", "w") as f:
    config["token"] = token
    json.dump(config, f, indent=2)

class FunnyBadge(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()

client = FunnyBadge(intents=Intents.default())

@client.event
async def on_ready():
    if not client.user:
        raise RuntimeError("on_ready() somehow got called before Client.user was set!")

    print(inspect.cleandoc(f"""
        Logged in as {client.user} (ID: {client.user.id})

        Use this URL to invite {client.user} to your server:
        {Fore.LIGHTBLUE_EX}https://discord.com/api/oauth2/authorize?client_id={client.user.id}&scope=applications.commands%20bot{Fore.RESET}
    """), end="\n\n")

@client.tree.command()
async def cat(interaction: Interaction):
    """Sends a random cat GIF"""
    url = "https://api.thecatapi.com/v1/images/search?mime_types=gif"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            cat_gif_url = data[0]['url']
            
            # Send the cat GIF as a message in Discord
            await interaction.response.send_message(cat_gif_url)

# The /dog command to get a random dog GIF
@client.tree.command()
async def dog(interaction: Interaction):
    """Sends a random dog GIF"""
    url = "https://api.thedogapi.com/v1/images/search?mime_types=gif"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            dog_gif_url = data[0]['url']
            
            # Send the dog GIF as a message in Discord
            await interaction.response.send_message(dog_gif_url)



@client.tree.command()
@app_commands.describe(message='The first value you want to add something to')
async def hello(interaction: Interaction, message: str):
    """ Says hello or something """
    print(f"> {Style.BRIGHT}{interaction.user}{Style.RESET_ALL} used the command.")
    await interaction.response.send_message(inspect.cleandoc(f"""
        Hi **{interaction.user}**, Your Message Was {message}"""))

@client.tree.command()
@app_commands.describe(
    exp='Enter your expression'
)
async def calc(interaction: Interaction, exp: str):
    """Performs Basic Maths"""
    try:
        result = eval(exp)
        await interaction.response.send_message(f"The result of `{exp}` is: {result}")
    except Exception as e:
        await interaction.response.send_message(f"Error: Invalid expression - {str(e)}")

@client.tree.command()
@app_commands.describe(user="The user you want to rename", new_name="The new name for the user")
async def rename(interaction: Interaction, user: discord.Member, new_name: str):
    """Renames a user (admin only)"""
    # Check if the person who invoked the command has admin permissions
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    try:
        # Rename the user with the provided new name
        await user.edit(nick=new_name)
        await interaction.response.send_message(f"Successfully changed {user.mention}'s nickname to `{new_name}`.")
    except Exception as e:
        # Catch any error (e.g., insufficient permissions, higher role, etc.)
        await interaction.response.send_message(f"Failed to rename {user.mention}. Error: {str(e)}")

#new function


@client.tree.command()
@app_commands.describe(users="The users you want information about (optional)")
async def info(interaction: Interaction, users: discord.Member = None):
    """Displays information about the mentioned users or the command invoker if none is mentioned."""
    if users is None:
        users = [interaction.user]  # Default to the command invoker

    # If the user is not passed as a parameter, get the mentioned users
    elif isinstance(users, list):
        users = users if len(users) > 0 else [interaction.user]

    user_info = []

    for user in users:
        user_data = {
            "Account Name": str(user),
            "Nickname": user.nick if user.nick else "None",
            "User ID": user.id,
            "Server Join Date": user.joined_at.strftime("%Y-%m-%d %H:%M:%S") if user.joined_at else "N/A",
            "Account Creation Date": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Create a formatted string for each user's information
        user_info.append(
            f"**User Information for {user.mention}:**\n" +
            "\n".join([f"{key}: {value}" for key, value in user_data.items()]) +
            "\n"
        )

    # Join all user info strings and send as a single message
    await interaction.response.send_message("\n".join(user_info))



client.run(token)