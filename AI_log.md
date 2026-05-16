# AI Assistance Log

## Tool Used
Claude (Anthropic)

---

## Entry 1 — Database Schema Design

**Prompt:** Reviewed my SQL schema and asked for feedback on constraints and normalization.

**AI Output:** Suggested adding a UNIQUE constraint on team name, CHECK constraints for
non-negative values on relevant columns, and AUTOINCREMENT on primary keys.

**My Modification:** Reviewed each suggestion and applied the ones that made sense for
the scope of the project. Kept the UNIQUE on team name after deciding it fit the
real-world use case. Wrote the final schema myself based on the feedback.

---

## Entry 2 — SQLAlchemy Models

**Prompt:** Asked how to translate my SQL schema into SQLAlchemy model classes.

**AI Output:** Provided an explanation of how SQLAlchemy relationships and foreign keys
work, particularly for tables with multiple foreign keys pointing to the same table.

**My Modification:** Used the explanation to write the models myself, adjusting the
relationship definitions to match my specific schema and verifying each model against
my original SQL.

---

## Entry 3 — Flask Routes and Templates

**Prompt:** Asked for help building out the Flask routes and HTML templates for CRUD
operations across all four tables.

**AI Output:** Generated the majority of the route functions and Jinja2 templates
including form handling, flash messages, and Bootstrap styling for teams, players,
games, and player stats.

**My Modification:** Reviewed all generated code and integrated it into the project
structure. Added my own validation rules for basketball-specific logic such as field
goals made not exceeding attempted, three pointers made not exceeding attempted, and
minutes played not exceeding 48. Also made design decisions on which fields to display
and how to organize the templates.
---

## Entry 4 — Transaction Logic

**Prompt:** Asked how to implement a SQL transaction in Flask where recording a game
also updates team win/loss records.

**AI Output:** Explained using try/except with db.session.rollback() to ensure atomicity.

**My Modification:** Implemented the transaction in the add_game and delete_game routes,
including the logic to reverse win/loss records when a game is deleted.

---

## Entry 5 — Dashboard Queries

**Prompt:** Asked about using SQLAlchemy aggregate functions for a summary dashboard.

**AI Output:** Explained how to use func.count, func.avg, func.sum, and func.round
with group_by in SQLAlchemy.

**My Modification:** Designed the dashboard layout and decided which statistics were
meaningful to display. Removed metrics that were not relevant to the use case and added
top rebounders and assisters sections based on my own judgment.