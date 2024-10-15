import discord
import json
from discord import app_commands, Intents, Client, Interaction

# Load bot token and other configuration from config.json
with open('config.json', 'r') as f:
    config = json.load(f)

token = config["token"]  # Fetch token from config.json

# Invite tracking dictionary loaded from file
invite_tracker = {}

# Load existing invite data from the JSON file
def load_invites():
    global invite_tracker
    try:
        with open('invite_data.json', 'r') as f:
            invite_tracker = json.load(f)
    except FileNotFoundError:
        invite_tracker = {}

# Save updated invite data to the JSON file
def save_invites():
    with open('invite_data.json', 'w') as f:
        json.dump(invite_tracker, f, indent=4)

# Custom bot class to handle setup hook and command registration
class FunnyBadge(Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync(guild=discord.Object(id=config["guild_id"]))  # Sync commands for the specific guild from config.json
        print("Command tree synced.")

# Initialize the bot with intents
client = FunnyBadge(intents=Intents.default())

# Load invites from the file on startup
@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    load_invites()  # Load existing invites from file
    for guild in client.guilds:
        invites = await guild.invites()
        invite_tracker[guild.id] = {
            invite.code: {
                "uses": invite.uses,
                "inviter_id": invite.inviter.id,
                "members": []  # Track members who joined through this invite
            } for invite in invites
        }
    save_invites()  # Save current invites to file
    print(f"Tracking invites for {len(client.guilds)} server(s).")

# Command to check how many users a member has invited
@client.tree.command(name="invites")
@app_commands.describe(user="The user whose invites you want to check")
async def invites(interaction: Interaction, user: discord.Member = None):
    user = user or interaction.user
    invite_count = sum(
        inv["uses"] for inv in invite_tracker.get(interaction.guild_id, {}).values() if inv["inviter_id"] == user.id
    )
    await interaction.response.send_message(f'{user.display_name} has invited {invite_count} users.')

# Command for admins to set the invite role
@client.tree.command(name="inviterole")
@app_commands.describe(number="Number of invites needed", role="Role to assign")
async def inviterole(interaction: Interaction, number: int, role: discord.Role):
    if interaction.user.guild_permissions.administrator:  # Check for admin permissions
        config["invite_roles"][str(interaction.guild_id)] = {
            "required_invites": number,
            "role_id": role.id
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        await interaction.response.send_message(f"Set invite requirement to {number} invites for role {role.name}.")
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

# New /test command that returns "synced"
@client.tree.command(name="test")
async def test(interaction: Interaction):
    await interaction.response.send_message("synced")

# Run the bot with the token
client.run(token)