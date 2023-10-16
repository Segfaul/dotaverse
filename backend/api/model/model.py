from tortoise import fields
from tortoise.models import Model

class Team(Model):
    '''
    Dota pro Team model
    '''
    id = fields.BigIntField(pk=True)

    name = fields.CharField(max_length=127)
    dotabuff_link = fields.CharField(max_length=255, null=True, blank=True)

    modified_date = fields.DatetimeField(auto_now=True)


class Player(Model):
    '''
    Dota pro Player model
    '''
    id = fields.BigIntField(pk=True)

    name = fields.CharField(max_length=40)
    dotabuff_link = fields.CharField(max_length=255)
    team_id = fields.ForeignKeyField('models.Team', related_name='team', null=True)

    modified_date = fields.DatetimeField(auto_now=True)

class Request(Model):
    '''
    Dota buff request list
    '''
    id = fields.BigIntField(pk=True)

    dotabuff_link = fields.CharField(max_length=255)
    status = fields.IntField()

    created_date = fields.DatetimeField(auto_now_add=True)
