from asgiref.sync import async_to_sync

from celery import shared_task

from backend.api.service.opendota_service import populate_db_from_opendota, get_data_from_opendota

@shared_task
def populate_db():
    '''
    Populate DB from parsed OpenDota stats
    '''
    async_to_sync(populate_db_from_opendota)()

@shared_task
def parse_opendota():
    '''
    Parse OpenDota stats
    '''
    async_to_sync(get_data_from_opendota)()
