# Basketball Stats App

A full-stack web application for tracking basketball teams, players, games, and player statistics. Built for coaches, analysts, or fans who want a simple way to manage and view game data and player performance.

## Tech Stack

- Python 3
- Flask
- SQLite (via SQLAlchemy ORM)
- Jinja2 Templates
- Bootstrap 5
- Git

## Project Structure

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/rick37234/stack_outline_app.git
   cd stack_outline_app
```

2. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

## Database Setup

The database is created automatically on first run using SQLAlchemy's `db.create_all()`.
If you prefer to set up the schema manually, run the provided SQL file:

```bash
sqlite3 app.db < schema.sql
```

## Usage

1. Start the server:
```bash
   python run.py
```

2. Open your browser and go to `http://127.0.0.1:5000`

3. Use the navbar to navigate:
   - **Dashboard** — view team standings and top player stats
   - **Teams** — add, edit, and delete teams
   - **Players** — add, edit, and delete players
   - **Games** — record game results (automatically updates team win/loss records)
   - **Stats** — log individual player stats for each game

## Features

- Full CRUD across Teams, Players, Games, and Player Stats
- Transaction logic — recording a game atomically updates both teams' win/loss records
- Server-side data validation on all forms
- Dashboard with standings and top performers using aggregate queries

## Normalization Report
   Functional Dependancies
   - `team_id → name, location, conference, coach, wins, losses, updated_at`
   - `player_id → name, team_id, position, height_in, weight_lbs, salary, updated_at`
   - `game_id → date, home_team_id, away_team_id, home_score, away_score, created_at`
   - `(player_id, game_id) → points, rebounds, assists, steals, blocks, turnovers, minutes_played, field_goals_attempted, field_goals_made, three_pointers_attempted, three_pointers_made, created_at`

   Anomalies
      Main issue was that there was no unique constraint to team name so I added that to prevent duplicates

   No decomposition was necessary, my original schema satisfied 3nf

