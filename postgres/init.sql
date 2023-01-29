CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(25) PRIMARY KEY,
    tokens INTEGER NOT NULL DEFAULT 0,
    last_played TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS commands (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(25) NOT NULL,
    command TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(25) NOT NULL,
    message TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS responses (
    message_id INTEGER NOT NULL,
    response TEXT NOT NULL,
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

CREATE TABLE IF NOT EXISTS pickers (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(25) NOT NULL,
    picker TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS queue (
    queue_id SERIAL PRIMARY KEY,
    user_id VARCHAR(25) NOT NULL,
    song_name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS session (
    session_id SERIAL PRIMARY KEY,
    user_id VARCHAR(25) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
