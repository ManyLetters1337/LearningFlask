CREATE TABLE projects
( id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  uuid VARCHAR(36) NOT NULL UNIQUE,
  user_id INT UNSIGNED,
  title VARCHAR(50) NOT NULL,
  description VARCHAR(500),
  created_on DATETIME NOT NULL,
  CONSTRAINT `fk_projects_user_id` FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

ALTER TABLE notes ADD CONSTRAINT `fk_notes_project_id` FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE;

