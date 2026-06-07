-- Очистка
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS groups;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS rooms;

-- Группы
CREATE TABLE groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Пользователи
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'participant',
    group_id INT,
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Предметы
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Преподаватели
CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Аудитории
CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    number VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- События
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

-- Данные: группы
INSERT INTO groups (name) VALUES
('Олимпиада по информатике'),
('Олимпиада по математике'),
('Олимпиада по физике'),
('Олимпиада по химии'),
('Олимпиада по биологии'),
('Олимпиада по русскому языку'),
('Олимпиада по английскому языку'),
('Олимпиада по истории'),
('Олимпиада по обществознанию'),
('Олимпиада по географии');

-- Данные: пользователи
INSERT INTO users (username, password, role, group_id) VALUES
('admin', 'pbkdf2:sha256:1000000$6jbzMmAo$b3a288f6ac4684aa24181dbd85a41ddbabcb402fefd18a474d3a43abf89e303d', 'admin', 1),
('bob', 'pbkdf2:sha256:1000000$U5QLQ9wD$8fcb8b0ef293794e566476ab88d1f67769923f5314532a86029d5a156d74708b', 'organizer', 1),
('svetlana', 'pbkdf2:sha256:1000000$tmKoIWU5$4e05353d8b5852ba085a6485e93de0e665579b0119d90322aa1814907b6e514b', 'organizer', 2),
('alice', 'pbkdf2:sha256:1000000$ojTyKrwV$b95388925e122985996f96ab673628c0b5df4cadfc6c19de7aa3c2d626eddd1e', 'participant', 1),
('ivan', 'pbkdf2:sha256:1000000$SZXpHHQY$fbaac85fe132cfbbd7f00d9391b3da7e08e6dbfb81ff7a1fa44d4ac7569f7650', 'participant', 2),
('maria', 'pbkdf2:sha256:1000000$092wopKt$682bc24b2a0dbd948203f1179b11003957909468d88a06b6712789459f4b0f1b', 'participant', 3),
('sergey', 'pbkdf2:sha256:1000000$v0ae9Vwm$df361aec3664d863d2bd0a98f556e527c16cefd555e1f7a0fd6e49e3d36c62b1', 'participant', 4),
('elena', 'pbkdf2:sha256:1000000$aZyLXnLf$b3bce15163440218e832c9634d287101346d7f3c2c155e3e348dceaa00454132', 'participant', 5),
('dmitry', 'pbkdf2:sha256:1000000$e5o2ZMIJ$c5c07b8459c84c4e41129925e772457d8395a2ad825aff724d89bdf453becfe6', 'participant', 6),
('anna', 'pbkdf2:sha256:1000000$EMxbxvs3$1882c0e97c1fc9718e11e61b4253e75b3e15cb636a4b9808a4a7b1cf4d93c2f0', 'participant', 7);

-- Данные: предметы
INSERT INTO subjects (name) VALUES
('Информатика'),
('Математика'),
('Физика'),
('Химия'),
('Биология'),
('Русский язык'),
('Английский язык'),
('История'),
('Обществознание'),
('География');

-- Данные: преподаватели
INSERT INTO teachers (name) VALUES
('Иванов И.И.'),
('Петров П.П.'),
('Сидоров С.С.'),
('Смирнова О.А.'),
('Кузнецова Н.В.'),
('Морозов Д.А.'),
('Васильева Е.С.'),
('Николаев А.П.'),
('Федорова М.М.'),
('Волкова Т.И.');

-- Данные: аудитории
INSERT INTO rooms (number) VALUES
('Ауд. 101'),
('Ауд. 102'),
('Ауд. 201'),
('Ауд. 202'),
('Ауд. 203'),
('Ауд. 301'),
('Ауд. 302'),
('Ауд. 303'),
('Ауд. 401'),
('Актовый зал');

-- Данные: события
INSERT INTO events (title, date, time, stage, user_id, subject_id, teacher_id, room_id) VALUES
('Регистрация участников олимпиады', '2025-09-25', '09:00:00', 'Консультация', 4, 1, 1, 1),
('Отборочный тур по информатике', '2025-09-30', '10:00:00', 'Отборочный', 4, 1, 1, 2),
('Разбор задач по информатике', '2025-10-01', '15:00:00', 'Консультация', 4, 1, 2, 3),
('Отборочный тур по математике', '2025-10-02', '09:30:00', 'Отборочный', 4, 2, 2, 4),
('Консультация по математике', '2025-10-03', '14:00:00', 'Консультация', 4, 2, 3, 5),
('Полуфинал по физике', '2025-10-04', '11:00:00', 'Полуфинал', 4, 3, 3, 6),
('Практический тур по химии', '2025-10-05', '10:30:00', 'Полуфинал', 4, 4, 4, 7),
('Теоретический тур по биологии', '2025-10-06', '12:00:00', 'Полуфинал', 4, 5, 5, 8),
('Полуфинал по английскому языку', '2025-10-07', '13:00:00', 'Полуфинал', 4, 7, 7, 9),
('Финал олимпиады по информатике', '2025-10-08', '10:00:00', 'Заключительный', 4, 1, 1, 10),
('Апелляция по математике', '2025-10-09', '16:00:00', 'Консультация', 5, 2, 8, 4),
('Награждение победителей', '2025-10-10', '12:30:00', 'Заключительный', 6, 9, 9, 10);
