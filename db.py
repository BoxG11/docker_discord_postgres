import psycopg2

"""CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    tokens INT DEFAULT NULL,
    last_played TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS commands (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    text TEXT DEFAULT NULL,
    time TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    text TEXT DEFAULT NULL,
    time TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS session (
    user_id INT NOT NULL,
    start TIMESTAMP NOT NULL DEFAULT NOW(),
    stop TIMESTAMP,
    session_id SERIAL PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS queue (
    queue_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    task TEXT NOT NULL DEFAULT NULL,
    taken_by TEXT NULL,
    done BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS pickers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL DEFAULT NULL,
    working BOOLEAN,
    time_started TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS responses (
    user_id INT NOT NULL,
    message_id SERIAL PRIMARY KEY,
    answer TEXT,
    sent BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

def insert_user(user_id):
    if not check_user(user_id):
        sql_command = f"INSERT INTO users (user_id) VALUES ('{user_id}');"
        db_action(sql_command)

def check_user(user_id):
    sql_command = f"SELECT user_id FROM users WHERE user_id = '{user_id}';"
    result = db_action(sql_command)
    if result:
        return True
    else:
        return False

def insert_message(user_id, message):
    sql_command = f"INSERT INTO messages (user_id, text) VALUES ('{user_id}', '{message}');"
    db_action(sql_command)

def insert_command(user_id, command):
    sql_command = f"INSERT INTO commands (user_id, text) VALUES ('{user_id}', '{command}');"
    db_action(sql_command)

def insert_session(user_id):
    sql_command = f"INSERT INTO session (user_id) VALUES ('{user_id}');"
    db_action(sql_command)

def update_session(user_id):
    sql_command = f"UPDATE session SET stop = NOW() WHERE user_id = '{user_id}' AND stop IS NULL;"
    db_action(sql_command)

def increase_tokens(user_id, tokens):
    sql_command = f"UPDATE users SET tokens = tokens + {tokens} WHERE user_id = '{user_id}';"
    db_action(sql_command)

def decrease_tokens(user_id, tokens):
    sql_command = f"UPDATE users SET tokens = tokens - {tokens} WHERE user_id = '{user_id}';"
    db_action(sql_command)

def get_tokens(user_id):
    sql_command = f"SELECT tokens FROM users WHERE user_id = '{user_id}';"
    result = db_action(sql_command, first=True)
    return result

def add_task(user_id, task):
    sql_command = f"INSERT INTO queue (user_id, task) VALUES ('{user_id}', '{task}');"
    db_action(sql_command)

def claim_task(picker_id, task):
    sql_command = f"UPDATE queue SET taken_by = {picker_id} WHERE task = '{task}';"
    db_action(sql_command)

def check_my_task(picker_id):
    sql_command = f"SELECT * FROM queue WHERE taken_by = {picker_id} AND done = 0;"
    result = db_action(sql_command)
    return result

def get_tasks():
    sql_command = "SELECT * FROM queue"
    result = db_action(sql_command)
    return result

def finish_task(picker_id):
    sql_command = f"UPDATE queue SET done = 1 WHERE taken_by = {picker_id} AND done = 0;"
    db_action(sql_command)

def get_message():
    sql_command = "SELECT user_id, text FROM messages WHERE sent = 0;"
    result = db_action(sql_command)
    if result:
        return result


# Connect to the database
def db_action(sql_command, first=False):
    conn = psycopg2.connect(
    host="postgres",
    port=5432,
    user="postgres",
    password="changeme",
    database="postgres")
    cur = conn.cursor()

    cur.execute(sql_command)

    if first:
        try:
            result = cur.fetchone()
        except:
            result = False

    else:
        try:
            result = cur.fetchall()
        except:
            result = False
    
    # Commit the changes to the database
    conn.commit()

    cur.close()
    conn.close()

    return result
