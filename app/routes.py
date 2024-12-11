import os
import sqlite3
from flask import Blueprint, render_template, redirect
from datetime import datetime

from app.forms import AppointmentForm


bp = Blueprint("main", __name__, "/")


DB_FILE = os.environ.get("DB_FILE") or "set DB_FILE in .env"


def hour_minute(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")


def handle_valid_form(conn, form):
    params = {
        "name": form.name.data,
        "start_datetime": datetime.combine(
            form.start_date.data, form.start_time.data
        ),
        "end_datetime": datetime.combine(
            form.end_date.data, form.end_time.data
        ),
        "description": form.description.data,
        "private": form.private.data,
    }
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO appointments (
            name,
            start_datetime,
            end_datetime,
            description,
            private
        )
        VALUES (
            :name,
            :start_datetime,
            :end_datetime,
            :description,
            :private
        );
        """,
        params,
    )
    conn.commit()
    return redirect("/")


def show_appointments(conn, form):
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


@bp.route("/", methods=["GET", "POST"])
def main():
    form = AppointmentForm()
    with sqlite3.connect(DB_FILE) as conn:
        if form.validate_on_submit():
            return handle_valid_form(conn, form)
        else:
            return show_appointments(conn, form)
