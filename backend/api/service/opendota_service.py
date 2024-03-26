import os
import asyncio
import json

import aiohttp
from dotenv import load_dotenv
from sqlalchemy.orm import joinedload

from backend.api.model import Team, TeamPlayer, Player, Hero, PlayerHeroChance
from backend.api.service.db_service import AsyncSessionFactory
from backend.api.schema import TeamStatsSchema

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
            headers={'user-agent': HEADERS['user_agents'][0]} if HEADERS else {}
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

    async with AsyncSessionFactory() as session:
        teams = [
            TeamStatsSchema(**team.__dict__).model_dump(exclude_unset=True) \
            async for team in Team.read_all(
                session,
                joinedload(Team.team_players)
                    .subqueryload(TeamPlayer.player)
                        .subqueryload(Player.player_hero_chances)
                            .subqueryload(PlayerHeroChance.hero)
            )
        ]
        team_names = [team["name"] for team in teams]
        for row in data:
            if row["name"] not in team_names:
                team_instance = (await Team.create(
                    session, name=row["name"],
                    opendota_link=f'https://www.opendota.com/teams/{row["team_id"]}'
                )).__dict__
            else:
                team_instance = teams[team_names.index(row["name"])]

            for player in row["players"]:
                player_instance = (await Player.create(
                    session, name=player["name"], steamid=int(player["steamid"]),
                    opendota_link=f'https://www.opendota.com/players/{player["account_id"]}'
                )).__dict__
                team_player_instance = (await TeamPlayer.create(
                    session, player_id=player_instance["id"], is_active=1,
                    team_id=team_instance["id"]
                )).__dict__
                heroes = [
                    hero.__dict__ async for hero in Hero.read_all(
                        session
                    )
                ]
                hero_names = [hero["opendota_name"] for hero in heroes]
                for hero_winrate in player["hero_winrates"]:
                    if hero_winrate["hero"][14:] not in hero_names:
                        hero_instance = (await Hero.create(
                            session, opendota_name=hero_winrate["hero"][14:]
                        )).__dict__
                    else:
                        hero_instance = heroes[hero_names.index(hero_winrate["hero"][14:])]

                    phc_instance = await PlayerHeroChance.create(
                        session, player_id=player_instance["id"],
                        hero_id=hero_instance["id"], 
                        win_percentage=round((float(hero_winrate["winrate"])*100), 2)
                    )


async def get_data_from_opendota():
    '''
    Function collects data from opendota and save in data.json file
    '''
    with open('backend/config/opendota_links.json', 'r', encoding='utf-8') as link_file:
        opendota_link = json.load(link_file)

    teams = await get_response(opendota_link['link'])

    with open('backend/config/data.json', 'w', encoding='utf-8') as record_file:
        json.dump(teams['rows'], record_file, indent=4)


# asyncio.run(populate_db_from_opendota())
