# from typing import AsyncIterator

# from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, func, select
# from sqlalchemy.orm import DeclarativeBase as Base, Mapped, relationship, mapped_column
# from sqlalchemy.ext.asyncio import AsyncSession


# class Team(Base):
#     '''
#     # bit later...
#     '''
#     __tablename__ = "team"

#     id: Mapped[int] = mapped_column(
#         "id", autoincrement=True, nullable=False, unique=True, primary_key=True
#     )
#     name: Mapped[str] = mapped_column("name", String(length=32), nullable=False)
#     dotabuff_link: Mapped[str] = mapped_column("dotabuff_link", String(length=128), nullable=False)
#     modified_at: Mapped[DateTime] = mapped_column(
#         "modified_at", DateTime("Europe/Moscow"), nullable=False, 
#         server_default=func.now, onupdate=func.now
#     )
#     players: Mapped[list] = relationship('Player', back_populates='team')

#     @classmethod
#     async def read_all(cls, session: AsyncSession) -> AsyncIterator:
#         stmt = select(cls)
#         stream = await session.stream_scalars(stmt.order_by(cls.id))
#         async for row in stream:
#             yield row
        
#     @classmethod
#     async def read_by_id(cls, session: AsyncSession, team_id: int):
#         stmt = select(cls).where(cls.id == team_id)
#         return await session.scalar(stmt.order_by(cls.id))


# class Player(Base):
#     '''
#     # bit later...
#     '''
#     __tablename__ = "player"

#     id: Mapped[int] = mapped_column(
#         "id", autoincrement=True, nullable=False, unique=True, primary_key=True
#     )
#     name: Mapped[str] = mapped_column("name", String(length=32), nullable=False)
#     dotabuff_link: Mapped[str] = mapped_column("dotabuff_link", String(length=128), nullable=False)
#     team_id: Mapped[int] = mapped_column("team_id", ForeignKey('team.id'), nullable=False)
#     created_at: Mapped[DateTime] = mapped_column(
#         "created_at", DateTime("Europe/Moscow"), 
#         server_default=func.now
#     )

#     team: Mapped[Team] = relationship('Team', back_populates='players')


# class Request(Base):
#     '''
#     # bit later...
#     '''
#     __tablename__ = "request"

#     id: Mapped[int] = mapped_column(
#         "id", autoincrement=True, nullable=False, unique=True, primary_key=True
#     )
#     dotabuff_link: Mapped[str] = mapped_column("dotabuff_link", String(length=128), nullable=False)
#     status: Mapped[int] = mapped_column("status", Integer, default=200, nullable=False)
#     created_at: Mapped[DateTime] = mapped_column(
#         "created_at", DateTime("Europe/Moscow"), 
#         server_default=func.now
#     )


# class Hero(Base):
#     '''
#     # bit later...
#     '''
#     __tablename__ = "hero"

#     id: Mapped[int] = mapped_column(
#         "id", autoincrement=True, nullable=False, unique=True, primary_key=True
#     )
#     dotabuff_name: Mapped[str] = mapped_column("dotabuff_name", String(length=64), nullable=False)
#     gif_link: Mapped[str] = mapped_column("gif_link", String(length=128), nullable=False)


# class Match(Base):
#     '''
#     # bit later...
#     '''
#     __tablename__ = "match"

#     id: Mapped[int] = mapped_column(
#         "id", autoincrement=True, nullable=False, unique=True, primary_key=True
#     )
#     win_percentage: Mapped[Float] = mapped_column(
#         "win_percentage", Float(precision=3), nullable=False
#     )
#     created_at: Mapped[DateTime] = mapped_column(
#         "created_at", DateTime("Europe/Moscow"), 
#         server_default=func.now
#     )


# class PlayerHeroChance(Base):
#     '''
#     # bit later...
#     '''
#     __tablename__ = "player_hero_chance"
    
#     id: Mapped[int] = mapped_column(
#         "id", autoincrement=True, nullable=False, unique=True, primary_key=True
#     )
#     player_id: Mapped[int] = mapped_column("player_id", ForeignKey('player.id'), nullable=False)
#     hero_id: Mapped[int] = mapped_column("hero_id", ForeignKey('hero.id'), nullable=False)    
#     win_percentage: Mapped[Float] = mapped_column(
#         "win_percentage", Float(precision=3), nullable=False
#     )
#     modified_at: Mapped[DateTime] = mapped_column(
#         "modified_at", DateTime("Europe/Moscow"), nullable=False, 
#         server_default=func.now, onupdate=func.now
#     )

#     player: Mapped[Player] = relationship('Player', back_populates='player_hero_chances')
#     hero: Mapped[Hero] = relationship('Hero', back_populates='player_hero_chances')


# class MatchPlayer(Base):
#     '''
#     # bit later...
#     '''
#     __tablename__ = "match_player"

#     id: Mapped[int] = mapped_column(
#         "id", autoincrement=True, nullable=False, unique=True, primary_key=True
#     )
#     player_id: Mapped[int] = mapped_column("player_id", ForeignKey('player.id'), nullable=False)
#     hero_id: Mapped[int] = mapped_column("hero_id", ForeignKey('hero.id'), nullable=False)
#     chance_id: Mapped[int] = mapped_column("chance_id", ForeignKey('player_hero_chance.id'), nullable=False)
#     match_id: Mapped[int] = mapped_column("match_id", ForeignKey('match.id'), nullable=False)

#     player: Mapped[Player] = relationship('Player', back_populates='match_players')
#     hero: Mapped[Hero] = relationship('Hero', back_populates='match_players')
#     chance: Mapped[PlayerHeroChance] = relationship('PlayerHeroChance', back_populates="match_players")
#     match: Mapped[Match] = relationship('Match', back_populates='match_players')
