import json
import aiohttp
import datetime
import random


def generate_weather():
    surf_temp = random.randint(10, 40)  # температура в градусах Цельсия
    sea_temp = surf_temp - 7  # температура морской воды в градусах Цельсия
    wind_power = random.choice([random.randint(0, 10)]*7 + [random.randint(10, 21)])  # сила ветра в м/с
    return surf_temp, sea_temp, wind_power


def struct_weather_message(surf_temp, sea_temp, wind_power):
    today = datetime.date.today().strftime('%d.%m.%Y')

    cold = f"прохладно **+{surf_temp}**. Лучше остаться дома."
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



class DiscordEvents:
    async def get_list_events(base_api_url, guild_id, auth_headers):
        get_event = f'{base_api_url}/guilds/{guild_id}/scheduled-events'
        async with aiohttp.ClientSession(headers=auth_headers) as session:
            try:
                async with session.get(get_event) as response:
                    response.raise_for_status()
                    assert response.status == 200
                    response_list = json.loads(await response.read())
                    return response_list
            except Exception as e:
                    print(f'EXCEPTION: {e}')
            finally:
                    await session.close()


    async def create_new_event(base_api_url, guild_id, auth_headers, surf_temp, wind_power):
        today = datetime.datetime.now()
        iso8601_date = today.isoformat()
        channel_id = 1194667877140271134
        event_create_url = f'{base_api_url}/guilds/{guild_id}/scheduled-events'
        event_data = json.dumps({
                'name': f'Температура: +{surf_temp}, Ветер: {wind_power} м/с',
                'privacy_level': 2,
                'scheduled_start_time': iso8601_date,
                'description': f'Погода в Анапе',
                'entity_type': 2,
                'channel_id': channel_id,
        })
        async with aiohttp.ClientSession(headers=auth_headers) as session:
            try:
                async with session.post(event_create_url, data=event_data) as response:
                    response.raise_for_status()
                    assert response.status == 200
            except Exception as e:
                    print(f'EXCEPTION: {e}')
            finally:
                    await session.close()


    async def delete_old_event(base_api_url, guild_id, auth_headers, events):
        try:
            old_guild_scheduled_event = events[len(events)-2]['id']
            event_delete_url = f'{base_api_url}/guilds/{guild_id}/scheduled-events/{old_guild_scheduled_event}'
            async with aiohttp.ClientSession(headers=auth_headers) as session:
                try:
                    async with session.delete(event_delete_url) as response:
                        response.raise_for_status()
                        assert response.status == 204
                except Exception as e:
                    print(f'EXCEPTION: {e}')
                finally:
                    await session.close()
        except:
            pass


    async def start_new_event(base_api_url, guild_id, auth_headers, events):
        new_guild_scheduled_event = events[len(events)-1]['id']
        event_start_url = f'{base_api_url}/guilds/{guild_id}/scheduled-events/{new_guild_scheduled_event}'
        event_patch_data = json.dumps({
            'status': '2'
        })
        async with aiohttp.ClientSession(headers=auth_headers) as session:
            try:
                async with session.patch(event_start_url, data=event_patch_data) as response:
                    response.raise_for_status()
                    assert response.status == 200
            except Exception as e:
                print(f'EXCEPTION: {e}')
            finally:
                await session.close()


    async def create_weather_event(surf_temp, sea_temp, wind_power, token):
        base_api_url = 'https://discord.com/api/v9'
        auth_headers = {
            'Authorization':f'Bot {token}',
            'User-Agent':'DiscordBot (https://discord.com/oauth2/authorize?client_id=1194945746278039612) Python/3.10 aiohttp/3.8.1',
            'Content-Type':'application/json'
        }
        guild_id = 1194667510847520798
        await DiscordEvents.create_new_event(base_api_url, guild_id, auth_headers, surf_temp, wind_power)
        events = await DiscordEvents.get_list_events(base_api_url, guild_id, auth_headers)
        if(len(events) == 2):
            await DiscordEvents.delete_old_event(base_api_url, guild_id, auth_headers, events)
        await DiscordEvents.start_new_event(base_api_url, guild_id, auth_headers, events)

