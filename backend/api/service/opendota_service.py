import os
import asyncio
import json
from typing import List, Dict

import aiohttp
from dotenv import load_dotenv
from sqlalchemy import select

from backend.api.util import get_or_create
from backend.api.model import Team, TeamPlayer, Player, Hero, PlayerHeroChance
from backend.api.service.db_service import TaskAsyncSessionFactory

env = os.environ.get
load_dotenv('./.env')

PROXY = env('PROXY')
HEADERS = {
    "user_agents": [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538 "\
            "(KHTML, like Gecko) Chrome/36 Safari/538",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 " \
            "(KHTML, like Gecko) Chrome/49.0.2599.0 Safari/537.36"
    ]
}


async def get_response(link: str) -> list | None:
    '''
    Function returns list object from provided link

    :param link : any http/https link
    :type link : str
    :returns : raw html object
    :rtype : html.HtmlElement | None
    '''
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=link,
            proxy=PROXY,
            headers={'user-agent': HEADERS['user_agents'][1]} if HEADERS else {}
        ) as response:
            if response.status != 200:
                print(response, response.status, sep='\n')
                return None
            content = await response.json()
            return content


async def populate_db_from_opendota():
    '''
    Function stores data from opendota into database
    '''
    with open('backend/config/data.json', 'r', encoding='utf-8') as record_file:
        data = json.load(record_file)

    async with TaskAsyncSessionFactory() as session:
        heroes: Dict[str, Hero] = {
            hero.opendota_name: hero async for hero in Hero.read_all(session)
        }
        for row in data:
            team_instance = await get_or_create(
                session, Team, name=row["name"],
                opendota_link=f'https://www.opendota.com/teams/{row["team_id"]}'
            )

            for player in row["players"]:
                player_instance = await get_or_create(
                    session, Player, defaults={"name": player["name"]},
                    steamid=int(player["steamid"]),
                    opendota_link=f'https://www.opendota.com/players/{player["account_id"]}'
                )
                team_player_instance = await get_or_create(
                    session, TeamPlayer, player_id=player_instance.id, is_active=True,
                    team_id=team_instance.id
                )
                player_hero_chances: List[PlayerHeroChance] = []
                existing_player_hero_chances: List[PlayerHeroChance] = []
                existing_phc_instances = {phc.hero_id: phc for phc in (await session.execute(
                    select(PlayerHeroChance).where(
                        PlayerHeroChance.player_id == player_instance.id,
                    )
                )).scalars()}
                for hero_winrate in player["hero_winrates"]:
                    hero_name = hero_winrate["hero"][14:]
                    win_percentage = round((float(hero_winrate["winrate"])*100), 2)

                    if hero_name not in [
                        hero_instance.opendota_name for hero_id, hero_instance in heroes.items()
                    ]:
                        hero_instance = await get_or_create(
                            session, Hero, opendota_name=hero_name
                        )
                        heroes[hero_name] = hero_instance
                    else:
                        hero_instance = heroes[hero_name]

                    if hero_instance.id in existing_phc_instances.keys():
                        existing_phc_instance = existing_phc_instances[hero_instance.id]
                        if existing_phc_instance.win_percentage != win_percentage:
                            existing_phc_instance.win_percentage = win_percentage
                            existing_player_hero_chances.append(existing_phc_instance.__dict__)
                    else:
                        player_hero_chances.append(PlayerHeroChance(
                            player_id=player_instance.id,
                            hero_id=hero_instance.id,
                            win_percentage=win_percentage
                        ).__dict__)

                if player_hero_chances:
                    await session.execute(
                        PlayerHeroChance.__table__.insert(),
                        player_hero_chances
                    )
                if existing_player_hero_chances:
                    for phc in existing_player_hero_chances:
                        await session.execute(
                            PlayerHeroChance.__table__.update()
                                .where(PlayerHeroChance.id == phc['id'])
                                .values(win_percentage=phc['win_percentage'])
                        )


async def get_data_from_opendota():
    '''
    Function collects data from opendota and save in data.json file
    '''
    with open('backend/config/opendota_links.json', 'r', encoding='utf-8') as link_file:
        opendota_link = json.load(link_file)

    teams = await get_response(opendota_link['fast_link'])
    for i in range(3, 99, 3):
        await asyncio.sleep(5)
        group_of_teams = await get_response(
            opendota_link['fast_link'].replace('OFFSET%200', f'OFFSET%20{i}')
        )
        if group_of_teams:
            teams['rows'] += group_of_teams['rows']

    if teams:
        with open('backend/config/data.json', 'w', encoding='utf-8') as record_file:
            json.dump(teams['rows'], record_file, indent=4)


# asyncio.run(populate_db_from_opendota())
