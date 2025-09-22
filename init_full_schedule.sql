DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS rooms;

CREATE TABLE groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'participant',
    group_id INT,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    stage VARCHAR(100),
    user_id INT NOT NULL,
    subject_id INT,
    teacher_id INT,
    room_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE SET NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Группы (олимпиады)
INSERT INTO groups (name) VALUES
('Олимпиада по информатике'),
('Олимпиада по математике'),
('Олимпиада по физике');

-- Пользователи (3 роли)
INSERT INTO users (username, password, role, group_id) VALUES
('admin', 'admin_hashed', 'admin', 1),
('organizer', 'organizer_hashed', 'organizer', 1),
('participant', 'participant_hashed', 'participant', 2);

-- Дисциплины
INSERT INTO subjects (name) VALUES
('Информатика'),
('Математика'),
('Физика');

-- Преподаватели / Жюри
INSERT INTO teachers (name) VALUES
('Иванов И.И.'),
('Петров П.П.'),
('Сидоров С.С.');

-- Аудитории
INSERT INTO rooms (number) VALUES
('Ауд. 101'),
('Ауд. 202'),
('Ауд. 303');

-- События (этапы олимпиад)
INSERT INTO events (title, date, time, stage, user_id, subject_id, teacher_id, room_id) VALUES
('Отборочный тур по информатике', '2025-09-30', '10:00:00', 'Отборочный', 3, 1, 1, 1),
('Полуфинал по информатике', '2025-10-02', '11:00:00', 'Полуфинал', 3, 1, 1, 2),
('Финал по информатике', '2025-10-05', '12:00:00', 'Заключительный', 3, 1, 1, 3),

('Отборочный тур по математике', '2025-09-28', '09:00:00', 'Отборочный', 3, 2, 2, 1),
('Консультация по математике', '2025-09-29', '14:00:00', 'Консультация', 3, 2, 2, 2),
('Финал по математике', '2025-10-06', '13:00:00', 'Заключительный', 3, 2, 2, 3),

('Отборочный тур по физике', '2025-09-27', '15:00:00', 'Отборочный', 3, 3, 3, 1),
('Полуфинал по физике', '2025-10-01', '16:00:00', 'Полуфинал', 3, 3, 3, 2),
('Финал по физике', '2025-10-07', '10:00:00', 'Заключительный', 3, 3, 3, 3);
