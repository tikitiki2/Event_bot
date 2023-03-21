from discord.ext import commands,tasks
from datetime import datetime
from discord.utils import get,utcnow
from discord import CategoryChannel
import discord
import discord.utils
import datetime
import asyncio
import pytz
import os
from discord import app_commands
intents=discord.Intents.all()
client = commands.Bot(command_prefix="!",intents=intents,help_command=None)

global guild_id
#the id of the guild bot is used for
guild_id=int('your guild ID')

apikey = "your key"



@client.event
async def on_ready():

    print('Logged on as {0.user}!'.format(client))
    #schedule_event.start()
@client.tree.command(name='schedule',guild=discord.Object(id=guild_id),description='schedule a discord event')
async def schedule(interaction: discord.Interaction,event:str,month : int,day:int,start_time24h:int,voicechannelname:str=None,location:str=None,image:discord.Attachment=None,description:str=None):
    startime = datetime.datetime(2023, month, day, start_time24h, tzinfo=pytz.UTC)
    endtime = datetime.datetime(2023, month, day, start_time24h+1, tzinfo=pytz.UTC)
    if image:
        filename = 'temp.png'
        path = os.path.join(os.getcwd(), filename)
        await image.save(path)
        file_extension = os.path.splitext(filename)[1]
        with open(f'temp{file_extension}','rb') as p:
            image = p.read()
        os.remove(f'temp{file_extension}')

    channel = client.get_channel(guild_id)
    g = client.get_guild(guild_id)
    try:
        #not done some edge cases are not accounted for
        #if image is uploaded
        if image:
            #voicechannel is specified
            if voicechannelname:
                print('1')
                await g.create_scheduled_event(name=event, start_time=startime, image=image,entity_type=discord.EntityType(2),description=description,location=voicechannelname)
            #location is specified not voice channel
            else:
                print('2')
                await g.create_scheduled_event(name=event, start_time=startime, image=image, description=description,location=location)
        # image is not uploaded
        else:
            # voicechannel is specified but no image
            if voicechannelname:
                print('3')
                await g.create_scheduled_event(name=event, start_time=startime,entity_type=discord.EntityType(2), description=description,location=voicechannelname)
            # location is specified not voice channel
            else:
                print('4')
                await g.create_scheduled_event(name=event, start_time=startime, description=description,location=location,end_time=endtime)

    except Exception as e:
        print(e)
        await interaction.response.send_message(f'failed to create event {event}')
        return 1
    await interaction.response.send_message(f'successfully created event {event}')

#syncs command to discord
# use after adding bot to server
@client.command(pass_context=True)
async def sync(ctx):
    try:
        await client.tree.sync(guild=discord.Object(id=guild_id))
    except Exception as e:
        print(e)


client.run('discord run key')
