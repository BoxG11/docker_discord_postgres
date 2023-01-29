CREATE TABLE IF NOT EXISTS users (
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
    time TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS session (
    user_id INT NOT NULL UNIQUE,
    start TIMESTAMP DEFAULT NOW(),
    stop TIMESTAMP DEFAULT NULL,
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
