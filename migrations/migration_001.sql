use base;

CREATE TABLE users
( id INT UNSIGNED AUTO_INCREMENT,
  user_uuid VARCHAR(36) NOT NULL UNIQUE,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(100) NOT NULL UNIQUE,
  PRIMARY KEY (id)
);

CREATE TABLE notes
( id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  note_uuid VARCHAR(36) NOT NULL UNIQUE,
  user_id INT UNSIGNED,
  title VARCHAR(50) NOT NULL,
  description VARCHAR(500),
  status BOOL NOT NULL,
  created_on DATETIME NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);