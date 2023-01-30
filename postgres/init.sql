CREATE TABLE IF NOT EXISTS users (
    user_id TEXT NOT NULL PRIMARY KEY,
    tokens INT DEFAULT NULL,
    last_played TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS commands (
    command_id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    text TEXT DEFAULT NULL,
    time TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS messages (
    message_id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    text TEXT DEFAULT NULL,
    time TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS session (
    user_id TEXT NOT NULL,
    start TIMESTAMP NOT NULL DEFAULT NOW(),
    stop TIMESTAMP,
    session_id SERIAL PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS queue (
    queue_id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    task TEXT NOT NULL DEFAULT NULL,
    taken_by TEXT NULL,
    done BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS responses (
    user_id TEXT NOT NULL,
    message_id SERIAL PRIMARY KEY,
    answer TEXT,
    sent BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
