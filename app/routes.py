import os
import sqlite3
from flask import Blueprint, render_template
from datetime import datetime


bp = Blueprint("main", __name__, "/")


DB_FILE = os.environ.get("DB_FILE") or "set DB_FILE in .env"


@bp.route("/")
def main():
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

        return render_template(
            "main.html", rows=rows, datetime=datetime
        )
