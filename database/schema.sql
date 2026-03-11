CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE,
  mobile VARCHAR(20) UNIQUE,
  password_hash VARCHAR(255),
  field_of_study VARCHAR(120),
  learning_interest VARCHAR(120),
  streak_days INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) UNIQUE NOT NULL,
  description TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS modules (
  id SERIAL PRIMARY KEY,
  course_id INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  title VARCHAR(150) NOT NULL,
  sequence INT DEFAULT 1
);

CREATE TABLE IF NOT EXISTS lessons (
  id SERIAL PRIMARY KEY,
  module_id INT NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
  title VARCHAR(150) NOT NULL,
  video_url VARCHAR(255) DEFAULT '',
  notes TEXT DEFAULT '',
  revision TEXT DEFAULT '',
  practice_questions TEXT DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS quiz_results (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  course_id INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  score FLOAT DEFAULT 0,
  time_taken INT DEFAULT 0,
  skipped_questions INT DEFAULT 0,
  attempts INT DEFAULT 1,
  payload TEXT DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learner_profile (
  id SERIAL PRIMARY KEY,
  user_id INT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  learning_speed VARCHAR(50) DEFAULT 'moderate',
  knowledge_level VARCHAR(50) DEFAULT 'beginner',
  strong_topics TEXT DEFAULT '[]',
  weak_topics TEXT DEFAULT '[]',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS practice_attempts (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  lesson_id INT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  score FLOAT DEFAULT 0,
  attempts INT DEFAULT 1,
  weak BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS code_submissions (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  course_id INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
  language VARCHAR(30) DEFAULT 'python',
  code TEXT NOT NULL,
  result TEXT DEFAULT '{}',
  syntax_errors INT DEFAULT 0,
  logic_errors INT DEFAULT 0,
  attempts INT DEFAULT 1,
  execution_success BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS progress_stats (
  id SERIAL PRIMARY KEY,
  user_id INT UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  weekly_progress TEXT DEFAULT '[]',
  topic_mastery TEXT DEFAULT '{}',
  strong_topics TEXT DEFAULT '[]',
  weak_topics TEXT DEFAULT '[]',
  progress_level VARCHAR(50) DEFAULT 'Level 1',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO courses (name, description)
VALUES
('Mathematics', 'Numbers, algebra, and problem solving'),
('Python', 'Programming from basics to advanced'),
('Machine Learning', 'Models, evaluation, deployment'),
('Crash Course', 'Quick fundamentals'),
('Test Mode', 'Assessment only mode')
ON CONFLICT (name) DO NOTHING;
