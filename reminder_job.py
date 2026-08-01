import sqlite3
from datetime import datetime, timedelta

from email_service import send_email

connection = sqlite3.connect("database.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

cursor.execute("""
    SELECT
        tasks.id,
        tasks.title,
        tasks.due_date,
        users.email

    FROM tasks
    JOIN users
    ON tasks.user_id = users.id

    WHERE
        tasks.status = 'Pending'
        AND tasks.reminder_sent = 0
        AND DATE(tasks.due_date) = ?
""", (tomorrow,))

reminders = cursor.fetchall()

emails_sent = 0

for reminder in reminders:

    subject = "⏰ Task Reminder"

    body = f"""
Hello!

This is a reminder that your task:

{reminder['title']}

is due tomorrow ({reminder['due_date']}).

Log into TaskHub to complete it.

Have a productive day!

- TaskHub
"""

    send_email(
        reminder["email"],
        subject,
        body
    )

    cursor.execute("""
        UPDATE tasks
        SET reminder_sent = 1
        WHERE id = ?
    """, (reminder["id"],))

    emails_sent += 1

connection.commit()
connection.close()

print(f"Emails sent: {emails_sent}")