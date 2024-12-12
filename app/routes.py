import os
import sqlite3
from flask import Blueprint, render_template, redirect, url_for
from datetime import datetime, timedelta

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


def show_appointments(conn, form, year, month, day):
    cur = conn.cursor()

    day = datetime(year, month, day)
    next_day = day + timedelta(days=1)
    params = {
        "day": day,
        "next_day": next_day,
    }
    cur.execute(
        """
        SELECT id, name, start_datetime, end_datetime
        FROM appointments
        WHERE start_datetime BETWEEN :day AND :next_day
        ORDER BY start_datetime;
        """,
        params,
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


@bp.route(
    "/<int:year>/<int:month>/<int:day>", methods=["GET", "POST"]
)
def daily(year, month, day):
    form = AppointmentForm()
    with sqlite3.connect(DB_FILE) as conn:
        if form.validate_on_submit():
            return handle_valid_form(conn, form)
        else:
            return show_appointments(conn, form, year, month, day)


@bp.route("/", methods=["GET", "POST"])
def main():
    now = datetime.now()
    year, month, day = (now.year, now.month, now.day)
    return redirect(
        url_for(".daily", year=year, month=month, day=day)
    )
