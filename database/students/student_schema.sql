CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    name TEXT,
    summary TEXT
);
    -- study_frequency TEXT,
    -- last_study_session TEXT,
    -- long_term_goals TEXT,
    -- test_performance TEXT,
    -- age INTEGER,
    -- major TEXT,
    -- preferred_study_time TEXT,
    -- learning_style TEXT,
    -- preferred_subjects TEXT,
    -- difficulty_levels TEXT,
    -- average_study_duration REAL,
    -- gpa REAL,
    -- topics_mastered TEXT,
    -- topics_struggling TEXT,
    -- progress_score REAL,
    -- favorite_resources TEXT,
    -- short_term_goals TEXT,
    -- motivation_level TEXT

INSERT INTO students (username, name, summary) VALUES ('wondergirl', 'Alice', 'Alice is a quiet girl who wants to get better at math');
INSERT INTO students (username, name, summary) VALUES ('builderboy', 'Bob', 'Bob has trouble remembering his dates in history');
-- INSERT INTO students (name, study_frequency, last_study_session, long_term_goals, test_performance) VALUES ('Alice', 'Once a week', '01/02/24', 'Acing my masters thesis', 'B+');
-- INSERT INTO students (name, study_frequency, last_study_session, long_term_goals, test_performance) VALUES ('Bob', 'Three times a week', '23/04/24', 'Passing biomechanics exam', 'A');
