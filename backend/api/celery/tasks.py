import asyncio

from celery import shared_task

from backend.api.service.opendota_service import populate_db_from_opendota, get_data_from_opendota

@shared_task
def populate_db():
    '''
    Populate DB from parsed OpenDota stats
    '''
    asyncio.run(populate_db_from_opendota())

@shared_task
def parse_opendota():
    '''
    Parse OpenDota stats
    '''
    asyncio.run(get_data_from_opendota())
