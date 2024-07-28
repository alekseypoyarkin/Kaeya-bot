import random
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import weather


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

token = os.getenv('BOT_TOKEN')
config = {
    'token': token,
    'prefix': '$',
}
bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())


@bot.command()
async def talk(ctx, *arg):
    if ctx.author != bot.user:
        arr = [f'Сегодня солнечно в Анапе, неправда ли, {ctx.author}?', 
          f'С тобой приятно есть самсу, {str(ctx.author)}!',
          f'Розы красные, фиалки цветут, пойду выпью вина и посплю!',
          f'Я слышал Каминаши недавно покинул Анапу... интересно почему он так поступил?',
          f'Любишь вино? Очень рекомендую одуванчиковое... Ох, ты ещё ребёнок? Тогда тебе непременно нужно попробовать яблочный сидр, я знаю отличное место.',
          f'Есть самсу - это искусство, а самса Анапы - это подарок богов, поэтому непременно нужно научиться ценить её.'
          ]
        await ctx.reply(random.choice(arr))


@tasks.loop(seconds = 86400)
async def weather_making():
    channel = bot.get_channel(1194668095785152542)  # доска: 1194668095785152542  тест: 1266010062086864956
    surf_temp, sea_temp, wind_power = weather.generate_weather()
    await weather.DiscordEvents.create_weather_event(surf_temp, sea_temp, wind_power, config['token']) 
    await channel.send(weather.struct_weather_message(surf_temp, sea_temp, wind_power))


@bot.listen()
async def on_ready():
    weather_making.start()


if __name__ == '__main__':
    bot.run(config['token'])