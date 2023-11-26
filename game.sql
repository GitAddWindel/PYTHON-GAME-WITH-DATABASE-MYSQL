

-- this is your database name (stack_game_db)
CREATE DATABASE stack_game_db;
USE stack_game_db;

-- this is your tablename (scores)
CREATE TABLE scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    score INT NOT NULL
);
