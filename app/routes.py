from flask import Blueprint, render_template, request, redirect, url_for, flash
from .extensions import db
from datetime import datetime
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