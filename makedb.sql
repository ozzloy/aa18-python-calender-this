CREATE TABLE appointments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(200) NOT NULL,
  start_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  end_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  description TEXT NOT NULL,
  private BOOLEAN NOT NULL
);

INSERT INTO appointments (
    name,
    start_datetime,
    end_datetime,
    description,
    private
)
VALUES (
    'My appointment',
    '2024-12-11 14:00:00',
    '2024-12-11 15:00:00',
    'An appointment for me',
    false
);
