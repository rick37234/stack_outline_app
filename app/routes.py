from flask import Blueprint, render_template, request, redirect, url_for, flash
from .extensions import db
from .models import Team

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
