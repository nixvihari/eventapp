-- This script must be sourced to create and initialize the database schema and tables in MySQL, prior to using the application

CREATE DATABASE IF NOT EXISTS event_management;

USE event_management;

CREATE TABLE IF NOT EXISTS events (
event_id INT AUTO_INCREMENT PRIMARY KEY,
event_name VARCHAR(50) NOT NULL,
description TEXT,
location VARCHAR(50),
event_date DATE
);

CREATE TABLE IF NOT EXISTS tasks (
task_id INT AUTO_INCREMENT PRIMARY KEY,
event_id INT NOT NULL,
task_name varchar(50) NOT NULL,
deadline DATE,
status BOOLEAN,
FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS attendees (
attendee_id INT AUTO_INCREMENT PRIMARY KEY,
attendee_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS assignments (
assignment_id INT AUTO_INCREMENT PRIMARY KEY,
attendee_id INT NOT NULL,
task_id INT NOT NULL,
event_id INT NOT NULL,
FOREIGN KEY (attendee_id) REFERENCES attendees(attendee_id) ON DELETE CASCADE,
FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE
);


ALTER TABLE tasks
ADD COLUMN status_readable VARCHAR(20) 
GENERATED ALWAYS AS (
    CASE 
        WHEN status = 1 THEN 'Completed'
        ELSE 'Pending'
    END
) STORED;