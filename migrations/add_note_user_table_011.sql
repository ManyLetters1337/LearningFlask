CREATE TABLE notes_users
(
    note_id INT UNSIGNED,
    user_id INT UNSIGNED,
    CONSTRAINT `fk_notes_users_id` FOREIGN KEY (note_id) REFERENCES notes (id) ON DELETE CASCADE,
    CONSTRAINT `fk_users_notes_id` FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
)
CHARACTER SET utf8;