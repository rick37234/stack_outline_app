from .extensions import db
from datetime import datetime


class Team(db.Model):
    __tablename__ = "team"

    team_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.String(100), nullable=False, unique=True)
    location   = db.Column(db.String(100), nullable=False)
    conference = db.Column(db.String(100), nullable=False)
    coach      = db.Column(db.String(100), nullable=False)
    wins       = db.Column(db.Integer, nullable=False, default=0)
    losses     = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    players = db.relationship("Player", back_populates="team")
    home_games = db.relationship("Game", foreign_keys="Game.home_team_id", back_populates="home_team")
    away_games = db.relationship("Game", foreign_keys="Game.away_team_id", back_populates="away_team")


class Player(db.Model):
    __tablename__ = "player"

    player_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.String(100), nullable=False)
    team_id    = db.Column(db.Integer, db.ForeignKey("team.team_id"), nullable=False)
    position   = db.Column(db.String(10), nullable=False)
    height_in  = db.Column(db.Integer, nullable=False)
    weight_lbs = db.Column(db.Integer, nullable=False)
    salary     = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    team  = db.relationship("Team", back_populates="players")
    stats = db.relationship("PlayerStats", back_populates="player")


class Game(db.Model):
    __tablename__ = "game"

    game_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date         = db.Column(db.Date, nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey("team.team_id"), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey("team.team_id"), nullable=False)
    home_score   = db.Column(db.Integer, nullable=False, default=0)
    away_score   = db.Column(db.Integer, nullable=False, default=0)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    home_team    = db.relationship("Team", foreign_keys=[home_team_id], back_populates="home_games")
    away_team    = db.relationship("Team", foreign_keys=[away_team_id], back_populates="away_games")
    player_stats = db.relationship("PlayerStats", back_populates="game")


class PlayerStats(db.Model):
    __tablename__ = "player_stats"

    player_id               = db.Column(db.Integer, db.ForeignKey("player.player_id"), primary_key=True)
    game_id                 = db.Column(db.Integer, db.ForeignKey("game.game_id"), primary_key=True)
    points                  = db.Column(db.Integer, nullable=False, default=0)
    rebounds                = db.Column(db.Integer, nullable=False, default=0)
    assists                 = db.Column(db.Integer, nullable=False, default=0)
    steals                  = db.Column(db.Integer, nullable=False, default=0)
    blocks                  = db.Column(db.Integer, nullable=False, default=0)
    turnovers               = db.Column(db.Integer, nullable=False, default=0)
    minutes_played          = db.Column(db.Integer, nullable=False, default=0)
    field_goals_attempted   = db.Column(db.Integer, nullable=False, default=0)
    field_goals_made        = db.Column(db.Integer, nullable=False, default=0)
    three_pointers_attempted = db.Column(db.Integer, nullable=False, default=0)
    three_pointers_made     = db.Column(db.Integer, nullable=False, default=0)
    created_at              = db.Column(db.DateTime, default=datetime.utcnow)

    player = db.relationship("Player", back_populates="stats")
    game   = db.relationship("Game", back_populates="player_stats")