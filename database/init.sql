USE esandb;

CREATE TABLE IF NOT EXISTS test (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

INSERT INTO test (name) VALUES ('John'), ('Jane'), ('Doe');
