CREATE TABLE team (
    team_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name       VARCHAR(100) NOT NULL UNIQUE,
    location   VARCHAR(100) NOT NULL,
    conference VARCHAR(100) NOT NULL,
    coach      VARCHAR(100) NOT NULL,
    wins       INT NOT NULL DEFAULT 0 CHECK (wins >= 0),
    losses     INT NOT NULL DEFAULT 0 CHECK (losses >= 0),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE player (
    player_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name       VARCHAR(100) NOT NULL,
    team_id    INT NOT NULL,
    position   VARCHAR(10) NOT NULL,
    height_in  INT NOT NULL CHECK (height_in > 0),
    weight_lbs INT NOT NULL CHECK (weight_lbs > 0),
    salary     INT NOT NULL CHECK (salary >= 0),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES team(team_id)
);

CREATE TABLE game (
    game_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    date         DATE NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    home_score   INT NOT NULL DEFAULT 0 CHECK (home_score >= 0),
    away_score   INT NOT NULL DEFAULT 0 CHECK (away_score >= 0),
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (home_team_id) REFERENCES team(team_id),
    FOREIGN KEY (away_team_id) REFERENCES team(team_id)
);

CREATE TABLE player_stats (
    player_id                INT NOT NULL,
    game_id                  INT NOT NULL,
    points                   INT NOT NULL DEFAULT 0 CHECK (points >= 0),
    rebounds                 INT NOT NULL DEFAULT 0 CHECK (rebounds >= 0),
    assists                  INT NOT NULL DEFAULT 0 CHECK (assists >= 0),
    steals                   INT NOT NULL DEFAULT 0 CHECK (steals >= 0),
    blocks                   INT NOT NULL DEFAULT 0 CHECK (blocks >= 0),
    turnovers                INT NOT NULL DEFAULT 0 CHECK (turnovers >= 0),
    minutes_played           INT NOT NULL DEFAULT 0 CHECK (minutes_played >= 0),
    field_goals_attempted    INT NOT NULL DEFAULT 0 CHECK (field_goals_attempted >= 0),
    field_goals_made         INT NOT NULL DEFAULT 0 CHECK (field_goals_made >= 0),
    three_pointers_attempted INT NOT NULL DEFAULT 0 CHECK (three_pointers_attempted >= 0),
    three_pointers_made      INT NOT NULL DEFAULT 0 CHECK (three_pointers_made >= 0),
    created_at               TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (player_id, game_id),
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id)
);