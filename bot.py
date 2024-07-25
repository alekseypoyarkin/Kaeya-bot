import random
import discord
import datetime
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv


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


def generate_weather():
    surf_temp = random.randint(10, 40)  # температура в градусах Цельсия
    sea_temp = surf_temp - 7  # температура морской воды в градусах Цельсия
    wind_power = random.choice([random.randint(0, 10)]*7 + [random.randint(10, 21)])  # сила ветра в м/с

    return surf_temp, sea_temp, wind_power

def struct_weather_message(surf_temp, sea_temp, wind_power):
    today = datetime.date.today().strftime('%d.%m.%Y')

    cold = f"прохладно **+{surf_temp}**.  Лучше остаться дома."
    warm = f"тепло **+{surf_temp}**, можно погулять на свежем воздухе."
    hot = f"**+{surf_temp}** жара! Идём купаться в море!"
    if (surf_temp < 20):
        temp = cold
    
    if ((surf_temp >= 20) and (surf_temp < 30)):
        temp = warm
    
    if (surf_temp >= 30):
        temp = hot

    still = f"штиль {wind_power} м/с. Спокойствие..."
    weak = f"слабый {wind_power} м/с. Легкий бриз!"
    ok = f"{wind_power} м/с."
    strong = f"сильный {wind_power} м/с. Придерживайте ваши шляпы!"

    if (wind_power == 0):
        wind = still

    if ((wind_power >= 1) and (wind_power < 6)):
        wind = weak
    
    if ((wind_power >= 6) and (wind_power < 14)):
        wind = ok
    
    if (wind_power >= 14):
        wind = strong

    return f"Прогноз погоды в Анапе от Кейи на {today}! \nСегодня {temp} Ветер {wind} \nПриятного дня!"


@tasks.loop(seconds = 86400)
async def weather_making():
    channel = bot.get_channel(1266010062086864956)  # доска: 1194668095785152542  тест: 1266010062086864956
    surf_temp, sea_temp, wind_power = generate_weather()
    await channel.send(struct_weather_message(surf_temp, sea_temp, wind_power))


@bot.listen()
async def on_ready():
    weather_making.start()



bot.run(config['token'])