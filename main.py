from os import getenv
from csv import reader
from json import load

from disnake import Intents, Client
from disnake.utils import get
from dotenv import load_dotenv


async def get_role(guild, role_id: int):
    try:
        return guild.get_role(role_id)
    except:
        return None


def parse_csv():
    file = open("./data/members.csv")
    data = reader(file)
    next(data)
    # starts iteration
    for row in data:
        yield row[1].split('#')[0].strip()

    file.close()


intents = Intents.default()
intents.members = True
bot = Client(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is connected to Discord and listening for events.")


@bot.event
async def on_message(message):
    """listen for message event, only from specific member or roles"""

    # if message author is a bot or doesn't have manage_members permissions, return
    if (
        message.author.bot
        or not message.channel.permissions_for(message.author).manage_roles
    ):
        return


    guild = message.guild

    bypassed_members = []

    if message.attachments:
        # if attachments, iterate attachaments and get members.csv
        for a in message.attachments:
            if a.filename == "members.csv":

                # attachment exist, check for role ID in message content
                if message.content:

                    # try to fetch the role object from the role ID included in message
                    role = await get_role(guild, int(message.content))

                    if role:
                        # attachment exists, if role also exists, save the member.csv attachment
                        await a.save("./data/members.csv")

                        # parse the csv and add role to members
                        for row in parse_csv():
                            member = get(
                                guild.members, name=row
                            )
                            # can't get member object with name
                            if not member:
                                member = get(guild.members, display_name=row)

                            # can't get member object with nickname
                            if not member:
                                bypassed_members.append(row)
                            else:
                                if not role in member.roles:
                                    await member.add_roles(role)

                        if bypassed_members:
                            bypassed_count = len(bypassed_members)
                            bypassed_members = "\n".join(bypassed_members)

                            await message.reply(
                                f"The following {bypassed_count} members were skipped during import, all others were given the {role.name} role:\n{bypassed_members}\n"
                            )

                        else:
                            await message.reply(f'All members were updated with the {role.name} role')
                    # error message sent if role not valid
                    else:
                        await message.reply("The submitted role ID is not valid")

                # error message sent if no message included with csv upload
                else:
                    await message.reply(
                        "You must include a role ID when uploading the members.csv file"
                    )


load_dotenv()
bot.run(getenv("TOKEN"))
