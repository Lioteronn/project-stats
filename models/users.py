from enum import Enum

from tortoise import fields
from tortoise.models import Model


class Rank(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"
    MASTER = "master"
    ELITE = "elite"


class RankDivision(str, Enum):
    DIVISION_I = "I"
    DIVISION_II = "II"
    DIVISION_III = "III"
    UNRANKED = "unranked"


class UserStatsInfo(Model):
    user = fields.ForeignKeyField("models.User", related_name="stats")
    user_steam_id = fields.CharField(max_length=20)
    user_steam_url = fields.CharField(max_length=200)
    level = fields.IntField()
    current_rank = fields.CharField(max_length=20, choices=Rank)
    current_rank_division = fields.CharField(max_length=20, choices=RankDivision)
    wins = fields.IntField()
    goals = fields.IntField()
    shots = fields.IntField()
    assists = fields.IntField()
    saves = fields.IntField()
    steals = fields.IntField()
    tackles = fields.IntField()
    mvps = fields.IntField()
    total_wins = fields.IntField()
    total_losses = fields.IntField()


class User(Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
