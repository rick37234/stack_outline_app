from flask import Blueprint, render_template, request, redirect, url_for, flash
from .extensions import db
from datetime import datetime
from sqlalchemy import func
from .models import Team, Player, Game, PlayerStats

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")

#teams
@main.route("/teams")
def teams():
    all_teams = Team.query.order_by(Team.name).all()
    return render_template("teams/list.html", teams=all_teams)


@main.route("/teams/add", methods=["GET", "POST"])
def add_team():
    if request.method == "POST":
        name       = request.form.get("name", "").strip()
        location   = request.form.get("location", "").strip()
        conference = request.form.get("conference", "").strip()
        coach      = request.form.get("coach", "").strip()

        # server-side validation
        if not name or not location or not conference or not coach:
            flash("All fields are required.", "danger")
            return redirect(url_for("main.add_team"))

        if Team.query.filter_by(name=name).first():
            flash("A team with that name already exists.", "danger")
            return redirect(url_for("main.add_team"))

        team = Team(name=name, location=location, conference=conference, coach=coach)
        db.session.add(team)
        db.session.commit()
        flash("Team added!", "success")
        return redirect(url_for("main.teams"))

    return render_template("teams/add.html")


@main.route("/teams/edit/<int:team_id>", methods=["GET", "POST"])
def edit_team(team_id):
    team = Team.query.get_or_404(team_id)

    if request.method == "POST":
        name       = request.form.get("name", "").strip()
        location   = request.form.get("location", "").strip()
        conference = request.form.get("conference", "").strip()
        coach      = request.form.get("coach", "").strip()
        wins       = request.form.get("wins", 0)
        losses     = request.form.get("losses", 0)

        if not name or not location or not conference or not coach:
            flash("All fields are required.", "danger")
            return redirect(url_for("main.edit_team", team_id=team_id))

        try:
            wins   = int(wins)
            losses = int(losses)
            if wins < 0 or losses < 0:
                raise ValueError
        except ValueError:
            flash("Wins and losses must be non-negative numbers.", "danger")
            return redirect(url_for("main.edit_team", team_id=team_id))

        team.name       = name
        team.location   = location
        team.conference = conference
        team.coach      = coach
        team.wins       = wins
        team.losses     = losses
        db.session.commit()
        flash("Team updated!", "success")
        return redirect(url_for("main.teams"))

    return render_template("teams/edit.html", team=team)


@main.route("/teams/delete/<int:team_id>", methods=["POST"])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    flash("Team deleted.", "success")
    return redirect(url_for("main.teams"))

#players

@main.route("/players")
def players():
    all_players = Player.query.order_by(Player.name).all()
    return render_template("players/list.html", players=all_players)


@main.route("/players/add", methods=["GET", "POST"])
def add_player():
    teams = Team.query.order_by(Team.name).all()

    if request.method == "POST":
        name       = request.form.get("name", "").strip()
        team_id    = request.form.get("team_id")
        position   = request.form.get("position", "").strip()
        height_in  = request.form.get("height_in")
        weight_lbs = request.form.get("weight_lbs")
        salary     = request.form.get("salary")

        if not name or not team_id or not position or not height_in or not weight_lbs or not salary:
            flash("All fields are required.", "danger")
            return redirect(url_for("main.add_player"))

        try:
            height_in  = int(height_in)
            weight_lbs = int(weight_lbs)
            salary     = int(salary)
            if height_in <= 0 or weight_lbs <= 0 or salary < 0:
                raise ValueError
        except ValueError:
            flash("Height and weight must be positive. Salary must be non-negative.", "danger")
            return redirect(url_for("main.add_player"))

        player = Player(name=name, team_id=team_id, position=position,
                        height_in=height_in, weight_lbs=weight_lbs, salary=salary)
        db.session.add(player)
        db.session.commit()
        flash("Player added!", "success")
        return redirect(url_for("main.players"))

    return render_template("players/add.html", teams=teams)


@main.route("/players/edit/<int:player_id>", methods=["GET", "POST"])
def edit_player(player_id):
    player = Player.query.get_or_404(player_id)
    teams  = Team.query.order_by(Team.name).all()

    if request.method == "POST":
        name       = request.form.get("name", "").strip()
        team_id    = request.form.get("team_id")
        position   = request.form.get("position", "").strip()
        height_in  = request.form.get("height_in")
        weight_lbs = request.form.get("weight_lbs")
        salary     = request.form.get("salary")

        if not name or not team_id or not position or not height_in or not weight_lbs or not salary:
            flash("All fields are required.", "danger")
            return redirect(url_for("main.edit_player", player_id=player_id))

        try:
            height_in  = int(height_in)
            weight_lbs = int(weight_lbs)
            salary     = int(salary)
            if height_in <= 0 or weight_lbs <= 0 or salary < 0:
                raise ValueError
        except ValueError:
            flash("Height and weight must be positive. Salary must be non-negative.", "danger")
            return redirect(url_for("main.edit_player", player_id=player_id))

        player.name       = name
        player.team_id    = team_id
        player.position   = position
        player.height_in  = height_in
        player.weight_lbs = weight_lbs
        player.salary     = salary
        db.session.commit()
        flash("Player updated!", "success")
        return redirect(url_for("main.players"))

    return render_template("players/edit.html", player=player, teams=teams)


@main.route("/players/delete/<int:player_id>", methods=["POST"])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    flash("Player deleted.", "success")
    return redirect(url_for("main.players"))

#games

@main.route("/games")
def games():
    all_games = Game.query.order_by(Game.date.desc()).all()
    return render_template("games/list.html", games=all_games)


@main.route("/games/add", methods=["GET", "POST"])
def add_game():
    teams = Team.query.order_by(Team.name).all()

    if request.method == "POST":
        date         = request.form.get("date", "").strip()
        home_team_id = request.form.get("home_team_id")
        away_team_id = request.form.get("away_team_id")
        home_score   = request.form.get("home_score")
        away_score   = request.form.get("away_score")

        if not date or not home_team_id or not away_team_id or home_score is None or away_score is None:
            flash("All fields are required.", "danger")
            return redirect(url_for("main.add_game"))

        if home_team_id == away_team_id:
            flash("Home and away teams must be different.", "danger")
            return redirect(url_for("main.add_game"))

        try:
            home_score = int(home_score)
            away_score = int(away_score)
            if home_score < 0 or away_score < 0:
                raise ValueError
        except ValueError:
            flash("Scores must be non-negative numbers.", "danger")
            return redirect(url_for("main.add_game"))

        try:
            # ── TRANSACTION: record game and update team records atomically ──
            game = Game(
                date=datetime.strptime(date, "%Y-%m-%d").date(),
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                home_score=home_score,
                away_score=away_score
            )
            db.session.add(game)

            home_team = Team.query.get(home_team_id)
            away_team = Team.query.get(away_team_id)

            if home_score > away_score:
                home_team.wins   += 1
                away_team.losses += 1
            elif away_score > home_score:
                away_team.wins   += 1
                home_team.losses += 1

            db.session.commit()
            flash("Game recorded and team records updated!", "success")
            return redirect(url_for("main.games"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error recording game: {str(e)}", "danger")
            return redirect(url_for("main.add_game"))

    return render_template("games/add.html", teams=teams)


@main.route("/games/delete/<int:game_id>", methods=["POST"])
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)

    try:
        # ── TRANSACTION: reverse team records when deleting a game ──
        home_team = Team.query.get(game.home_team_id)
        away_team = Team.query.get(game.away_team_id)

        if game.home_score > game.away_score:
            home_team.wins   -= 1
            away_team.losses -= 1
        elif game.away_score > game.home_score:
            away_team.wins   -= 1
            home_team.losses -= 1

        db.session.delete(game)
        db.session.commit()
        flash("Game deleted and team records updated.", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting game: {str(e)}", "danger")

    return redirect(url_for("main.games"))

#player stats

@main.route("/stats")
def stats():
    all_stats = db.session.query(PlayerStats)\
        .join(Player, PlayerStats.player_id == Player.player_id)\
        .join(Game, PlayerStats.game_id == Game.game_id)\
        .order_by(Game.date.desc()).all()
    return render_template("stats/list.html", stats=all_stats)


@main.route("/stats/add", methods=["GET", "POST"])
def add_stats():
    players = Player.query.order_by(Player.name).all()
    games   = Game.query.order_by(Game.date.desc()).all()

    if request.method == "POST":
        player_id              = request.form.get("player_id")
        game_id                = request.form.get("game_id")
        points                 = request.form.get("points", 0)
        rebounds               = request.form.get("rebounds", 0)
        assists                = request.form.get("assists", 0)
        steals                 = request.form.get("steals", 0)
        blocks                 = request.form.get("blocks", 0)
        turnovers              = request.form.get("turnovers", 0)
        minutes_played         = request.form.get("minutes_played", 0)
        field_goals_attempted  = request.form.get("field_goals_attempted", 0)
        field_goals_made       = request.form.get("field_goals_made", 0)
        three_pointers_attempted = request.form.get("three_pointers_attempted", 0)
        three_pointers_made    = request.form.get("three_pointers_made", 0)

        if not player_id or not game_id:
            flash("Player and game are required.", "danger")
            return redirect(url_for("main.add_stats"))

        # check for duplicate
        existing = PlayerStats.query.filter_by(
            player_id=player_id, game_id=game_id).first()
        if existing:
            flash("Stats for this player and game already exist.", "danger")
            return redirect(url_for("main.add_stats"))

        if int(field_goals_made) > int(field_goals_attempted):
            flash("Field goals made cannot exceed field goals attempted.", "danger")
            return redirect(url_for("main.add_stats"))

        if int(three_pointers_made) > int(three_pointers_attempted):
            flash("Three pointers made cannot exceed three pointers attempted.", "danger")
            return redirect(url_for("main.add_stats"))

        if int(minutes_played) > 48:
            flash("Minutes played cannot exceed 48.", "danger")
            return redirect(url_for("main.add_stats"))

        try:
            stat = PlayerStats(
                player_id=int(player_id),
                game_id=int(game_id),
                points=int(points),
                rebounds=int(rebounds),
                assists=int(assists),
                steals=int(steals),
                blocks=int(blocks),
                turnovers=int(turnovers),
                minutes_played=int(minutes_played),
                field_goals_attempted=int(field_goals_attempted),
                field_goals_made=int(field_goals_made),
                three_pointers_attempted=int(three_pointers_attempted),
                three_pointers_made=int(three_pointers_made)
            )

            # validate non-negative
            for field in [stat.points, stat.rebounds, stat.assists, stat.steals,
                          stat.blocks, stat.turnovers, stat.minutes_played,
                          stat.field_goals_attempted, stat.field_goals_made,
                          stat.three_pointers_attempted, stat.three_pointers_made]:
                if field < 0:
                    raise ValueError("Stats cannot be negative.")

            db.session.add(stat)
            db.session.commit()
            flash("Stats added!", "success")
            return redirect(url_for("main.stats"))

        except ValueError as e:
            flash(f"Invalid input: {str(e)}", "danger")
            return redirect(url_for("main.add_stats"))

    return render_template("stats/add.html", players=players, games=games)


@main.route("/stats/delete/<int:player_id>/<int:game_id>", methods=["POST"])
def delete_stats(player_id, game_id):
    stat = PlayerStats.query.filter_by(
        player_id=player_id, game_id=game_id).first_or_404()
    db.session.delete(stat)
    db.session.commit()
    flash("Stats deleted.", "success")
    return redirect(url_for("main.stats"))