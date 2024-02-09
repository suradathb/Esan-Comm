USE esandb;

CREATE TABLE IF NOT EXISTS test (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO test (name) VALUES ('John'), ('Jane'), ('Doe');

CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255),
    email VARCHAR(255),
    auth_method VARCHAR(50),
    password_hash VARCHAR(255)
);

CREATE TABLE Login (
    login_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    provider VARCHAR(50),
    provider_user_id VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE Address (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    address VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE PrivateKey (
    key_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    private_key TEXT,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE UserActivityLog (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);