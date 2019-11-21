use base;


ALTER TABLE notes ADD COLUMN project_id INT UNSIGNED;

ALTER TABLE notes ADD CONSTRAINT `fk_notes_project_id` FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE;