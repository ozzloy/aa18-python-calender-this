import os
import sqlite3
from flask import Blueprint, render_template
from datetime import datetime

from app.forms import AppointmentForm


bp = Blueprint("main", __name__, "/")


DB_FILE = os.environ.get("DB_FILE") or "set DB_FILE in .env"


def hour_minute(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")


@bp.route("/")
def main():
    form = AppointmentForm()
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()

        cur.execute(
            """
        SELECT id, name, start_datetime, end_datetime
        FROM appointments
        ORDER BY start_datetime;
        """
        )
        rows = cur.fetchall()

        rows = [
            {
                "id": row[0],
                "name": row[1],
                "start_time": hour_minute(row[2]),
                "end_time": hour_minute(row[3]),
            }
            for row in rows
        ]

        return render_template("main.html", rows=rows, form=form)
