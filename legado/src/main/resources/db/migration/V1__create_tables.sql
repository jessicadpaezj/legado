DROP INDEX IF EXISTS flyway_schema_history_s_idx;

DROP TABLE IF EXISTS article_favorites;
DROP TABLE IF EXISTS article_tags;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS follows;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS flyway_schema_history;


-- article_favorites definition

CREATE TABLE article_favorites (
  article_id VARCHAR(255) NOT NULL,
  user_id VARCHAR(255) NOT NULL,
  PRIMARY KEY (article_id, user_id)
);

-- article_tags definition

CREATE TABLE article_tags (
  article_id VARCHAR(255) NOT NULL,
  tag_id VARCHAR(255) NOT NULL
);

-- articles definition

CREATE TABLE articles (
  id VARCHAR(255) PRIMARY KEY,
  user_id VARCHAR(255),
  slug VARCHAR(255) UNIQUE,
  title VARCHAR(255),
  description TEXT,
  body TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- comments definition

CREATE TABLE comments (
  id VARCHAR(255) PRIMARY KEY,
  body TEXT,
  article_id VARCHAR(255),
  user_id VARCHAR(255),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- flyway_schema_history definition

CREATE TABLE flyway_schema_history (
    installed_rank INTEGER NOT NULL PRIMARY KEY,
    version VARCHAR(50),
    description VARCHAR(200) NOT NULL,
    type VARCHAR(20) NOT NULL,
    script VARCHAR(1000) NOT NULL,
    checksum INTEGER,
    installed_by VARCHAR(100) NOT NULL,
    installed_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    execution_time INTEGER NOT NULL,
    success BOOLEAN NOT NULL
);

CREATE INDEX flyway_schema_history_s_idx ON flyway_schema_history (success);

-- follows definition

CREATE TABLE follows (
  user_id VARCHAR(255) NOT NULL,
  follow_id VARCHAR(255) NOT NULL
);

-- tags definition

CREATE TABLE tags (
  id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) NOT NULL
);

-- users definition

CREATE TABLE users (
  id VARCHAR(255) PRIMARY KEY,
  username VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  bio TEXT,
  image VARCHAR(511)
);




-- ==========================================================
-- Fichero: consolidated_insert_pruebas.sql
-- Objetivo: Poblar datos de prueba en todas las tablas del esquema PostgreSQL de articles
-- Generado por ChatGPT (OpenAI) a solicitud del usuario
-- ==========================================================

-- 1️⃣ Tabla: users
INSERT INTO users (id, username, password, email, bio, image) VALUES
('u1', 'alice', 'pass123', 'alice@example.com', 'Bio of Alice', 'https://example.com/img/alice.jpg'),
('u2', 'bob', 'pass456', 'bob@example.com', 'Bio of Bob', 'https://example.com/img/bob.jpg'),
('u3', 'carol', 'pass789', 'carol@example.com', 'Bio of Carol', 'https://example.com/img/carol.jpg'),
('u4', 'david', 'pass321', 'david@example.com', 'Bio of David', 'https://example.com/img/david.jpg'),
('u5', 'eve', 'pass654', 'eve@example.com', 'Bio of Eve', 'https://example.com/img/eve.jpg'),
('u6', 'frank', 'pass987', 'frank@example.com', 'Bio of Frank', 'https://example.com/img/frank.jpg'),
('u7', 'grace', 'pass111', 'grace@example.com', 'Bio of Grace', 'https://example.com/img/grace.jpg'),
('u8', 'heidi', 'pass222', 'heidi@example.com', 'Bio of Heidi', 'https://example.com/img/heidi.jpg'),
('u9', 'ivan', 'pass333', 'ivan@example.com', 'Bio of Ivan', 'https://example.com/img/ivan.jpg'),
('u10', 'judy', 'pass444', 'judy@example.com', 'Bio of Judy', 'https://example.com/img/judy.jpg');

-- 2️⃣ Tabla: tags
INSERT INTO tags (id, name) VALUES
('t1', 'java'),
('t2', 'spring'),
('t3', 'aws'),
('t4', 'cloud'),
('t5', 'docker'),
('t6', 'kubernetes'),
('t7', 'graphql'),
('t8', 'react'),
('t9', 'security'),
('t10', 'database');

-- 3️⃣ Tabla: articles
INSERT INTO articles (id, user_id, slug, title, description, body) VALUES
('a1', 'u1', 'spring-boot-guide', 'Spring Boot Guide', 'Guide for Spring Boot', 'Detailed guide on Spring Boot'),
('a2', 'u2', 'aws-ec2-setup', 'AWS EC2 Setup', 'Setup EC2', 'How to setup EC2 on AWS'),
('a3', 'u3', 'docker-basics', 'Docker Basics', 'Basics of Docker', 'Introduction to Docker for beginners'),
('a4', 'u4', 'kubernetes-deployment', 'Kubernetes Deployment', 'Deploy on K8s', 'Steps to deploy apps on Kubernetes'),
('a5', 'u5', 'graphql-intro', 'GraphQL Introduction', 'Intro to GraphQL', 'Learning GraphQL basics'),
('a6', 'u6', 'react-hooks', 'Using React Hooks', 'React Hooks', 'Understanding React Hooks'),
('a7', 'u7', 'java-concurrency', 'Java Concurrency', 'Concurrency in Java', 'Handling concurrency in Java'),
('a8', 'u8', 'postgresql-tuning', 'PostgreSQL Tuning', 'Tuning Postgres', 'Performance tuning PostgreSQL'),
('a9', 'u9', 'api-security', 'API Security Best Practices', 'API Security', 'Best practices for securing APIs'),
('a10', 'u10', 'flyway-migrations', 'Flyway Migrations', 'DB migrations', 'Using Flyway for database migrations');

-- 4️⃣ Tabla: article_tags
INSERT INTO article_tags (article_id, tag_id) VALUES
('a1', 't2'),
('a1', 't1'),
('a2', 't3'),
('a2', 't4'),
('a3', 't5'),
('a4', 't6'),
('a5', 't7'),
('a6', 't8'),
('a7', 't1'),
('a9', 't9');

-- 5️⃣ Tabla: article_favorites
INSERT INTO article_favorites (article_id, user_id) VALUES
('a1', 'u2'),
('a1', 'u3'),
('a2', 'u1'),
('a3', 'u4'),
('a4', 'u5'),
('a5', 'u6'),
('a6', 'u7'),
('a7', 'u8'),
('a8', 'u9'),
('a9', 'u10');

-- 6️⃣ Tabla: comments
INSERT INTO comments (id, body, article_id, user_id) VALUES
('c1', 'Great article on Spring Boot!', 'a1', 'u2'),
('c2', 'Thanks for this EC2 guide.', 'a2', 'u3'),
('c3', 'Docker is awesome!', 'a3', 'u4'),
('c4', 'Very clear Kubernetes steps.', 'a4', 'u5'),
('c5', 'GraphQL explained well.', 'a5', 'u6'),
('c6', 'Hooks are powerful in React.', 'a6', 'u7'),
('c7', 'Concurrency tips are helpful.', 'a7', 'u8'),
('c8', 'Helped me tune Postgres.', 'a8', 'u9'),
('c9', 'API security is important.', 'a9', 'u10'),
('c10', 'Using Flyway now.', 'a10', 'u1');

-- 7️⃣ Tabla: follows
INSERT INTO follows (user_id, follow_id) VALUES
('u1', 'u2'),
('u2', 'u3'),
('u3', 'u4'),
('u4', 'u5'),
('u5', 'u6'),
('u6', 'u7'),
('u7', 'u8'),
('u8', 'u9'),
('u9', 'u10'),
('u10', 'u1');

-- 8️⃣ Tabla: flyway_schema_history
INSERT INTO flyway_schema_history (installed_rank, version, description, type, script, checksum, installed_by, execution_time, success) VALUES
(1, '1', 'Initial setup', 'SQL', 'V1__Initial_setup.sql', 123456, 'postgres', 120, true),
(2, '2', 'Add articles table', 'SQL', 'V2__Add_articles.sql', 234567, 'postgres', 80, true),
(3, '3', 'Add users table', 'SQL', 'V3__Add_users.sql', 345678, 'postgres', 90, true),
(4, '4', 'Add tags table', 'SQL', 'V4__Add_tags.sql', 456789, 'postgres', 70, true),
(5, '5', 'Add comments table', 'SQL', 'V5__Add_comments.sql', 567890, 'postgres', 100, true),
(6, '6', 'Add article_tags table', 'SQL', 'V6__Add_article_tags.sql', 678901, 'postgres', 110, true),
(7, '7', 'Add follows table', 'SQL', 'V7__Add_follows.sql', 789012, 'postgres', 60, true),
(8, '8', 'Add article_favorites table', 'SQL', 'V8__Add_article_favorites.sql', 890123, 'postgres', 75, true),
(9, '9', 'Add flyway schema history', 'SQL', 'V9__Add_flyway_history.sql', 901234, 'postgres', 65, true),
(10, '10', 'Add more constraints', 'SQL', 'V10__Add_constraints.sql', 101234, 'postgres', 85, true);

-- Fin del fichero
