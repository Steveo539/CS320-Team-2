import MySQLdb
import uuid
from passlib.handlers.sha2_crypt import sha256_crypt

from src.utility import list_to_string


def get_questions(mysql, form_id):
    try:
        form_id = int(form_id)
    except ValueError:  # Use this to prevent anything but integers being passed to SQL query
        return ""
    cur = mysql.connection.cursor()

    try:  # If there is an exception with the query, fail silently
        cur.execute("SELECT * FROM form_%s", [form_id])
    except (MySQLdb.Error, MySQLdb.Warning):
        return ""

    questions = cur.fetchall()
    cur.close()
    return questions


def add_question(mysql, form_id, question):
    cur = mysql.connection.cursor()
    statement = "INSERT INTO form_" + str(form_id)
    statement += "(type, text, options) VALUES(%s, %s, %s)"
    cur.execute(statement, (question['type'], question['text'], list_to_string(question['options'])))
    mysql.connection.commit()
    cur.close()


def remove_question(mysql, form_id, question_id):
    cur = mysql.connection.cursor()
    statement = "DELETE FROM form_" + str(form_id)
    statement += " WHERE id=%s"
    cur.execute(statement, [question_id])
    mysql.connection.commit()
    cur.close()


def generate_hash(mysql, survey):
    link_hash = uuid.uuid1().int
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO hashes(hash, surveyID) VALUES(%s, %s)", (str(link_hash), survey))
    mysql.connection.commit()
    cur.close()
    return link_hash


def create_admin(mysql):
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT * FROM users WHERE username=%s", ["admin"])
    if res < 1:
        print("Creating admin account...")
        password = sha256_crypt.encrypt("password1")
        cur.execute("INSERT INTO users(name, username, password, positionTitle, email, startDate) VALUES(%s, %s, %s, %s, %s, %s)", ("admin", "admin", password, "Admin", "admin@email.com", "1/1/1970"))
        mysql.connection.commit()
    cur.close()


def get_companies(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM companies")
    companies = cur.fetchall()
    cur.close()
    return companies


def delete_company(mysql, company):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE companyID=%s", [company])
    cur.execute("DELETE FROM companies WHERE companyID=%s", [company])
    mysql.connection.commit()
    cur.close()


def add_company(mysql, company):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO companies(companyName) VALUES(%s)", [company])
    mysql.connection.commit()
    cur.close()
