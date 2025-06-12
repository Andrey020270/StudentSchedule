-- Группы
SELECT * FROM groups;

-- Пользователи
SELECT * FROM users;

-- Дисциплины
SELECT * FROM subjects;

-- Преподаватели
SELECT * FROM teachers;

-- Аудитории
SELECT * FROM rooms;

-- События (с JOIN для человекочитаемости)
SELECT
    e.id AS event_id,
    u.username AS student,
    g.name AS group_name,
    s.name AS subject,
    t.name AS teacher,
    r.number AS room,
    e.date,
    e.time,
    e.title
FROM events e
LEFT JOIN users u ON e.user_id = u.id
LEFT JOIN groups g ON u.group_id = g.id
LEFT JOIN subjects s ON e.subject_id = s.id
LEFT JOIN teachers t ON e.teacher_id = t.id
LEFT JOIN rooms r ON e.room_id = r.id
ORDER BY e.date, e.time;
