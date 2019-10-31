from forms import MainForm


def load_database_info():
    info = {}
    try:
        db_config = open('../db.info', 'r')
    except IOError:
        print('ERROR: Invalid \'db.info\'...exiting')
        return None

    info['secret_key'] = db_config.readline().strip()
    info['host'] = db_config.readline().strip()
    info['user'] = db_config.readline().strip()
    info['password'] = db_config.readline().strip()
    info['db'] = db_config.readline().strip()
    db_config.close()
    return info


def get_questions(mysql, form_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM form_%s", [form_id])
    questions = cur.fetchall()
    cur.close()
    return questions


def build_form(questions):
    form = MainForm()
    #Insert code to build form
    return form