CREATE DATABASE IF NOT EXISTS gam_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;


CREATE USER 'gam_app'@'localhost' IDENTIFIED BY '200520021970@.com';
GRANT SELECT, INSERT, UPDATE ON gam_db.* TO 'gam_app'@'localhost';
FLUSH PRIVILEGES;


USE gam_db;
CREATE TABLE IF NOT EXISTS fraud_case_uploads (
id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
supabase_user_id CHAR(36) NOT NULL,
upload_id CHAR(36) NOT NULL,
inspector_name VARCHAR(150) NOT NULL,
inspector_rank VARCHAR(100) NOT NULL, 
inspector_branch VARCHAR(200) NOT NULL,
created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (id),
UNIQUE KEY uq_upload_id (upload_id),
INDEX idx_supabase_user_id (supabase_user_id),
INDEX idx_created_at (created_at)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;


DESCRIBE fraud_case_uploads;
SHOW CREATE TABLE fraud_case_uploads;



-- complete file upload metadata 
CREATE TABLE IF NOT EXISTS file_upload_sessions (
id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
supabase_user_id CHAR(36) NOT NULL,
upload_id CHAR(36) NOT NULL, 
file_name VARCHAR(500) NOT NULL,
file_size BIGINT UNSIGNED NOT NULL, 
content_type VARCHAR(100) NOT NULL, 
chunk_size INT UNSIGNED NOT NULL,
total_chunks INT UNSIGNED NOT NULL,
file_hash VARCHAR(128) NOT NULL,
status VARCHAR(50) NOT NULL DEFAULT 'pending',
created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP

ON UPDATE CURRENT_TIMESTAMP,
completed_at DATETIME DEFAULT NULL,

PRIMARY KEY (id),
UNIQUE  KEY uq_upload_id (upload_id),
INDEX idx_supabase_user (supabase_user_id),
INDEX idx_status (status),
INDEX idx_created_at (created_at)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;


ALTER TABLE file_upload_sessions
    ADD COLUMN received_chunks JSON NOT NULL DEFAULT (JSON_ARRAY())
    AFTER total_chunks;




-- chunks related metadata
-- CREATE TABLE IF NOT EXISTS file_upload_chunks (
-- id BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT,
-- upload_id CHAR(36) NOT NULL,   
-- chunk_number INT UNSIGNED NOT NULL,
-- chunk_size INT UNSIGNED NOT NULL,   
-- chunk_hash VARCHAR(128) NOT NULL,   
-- created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

-- PRIMARY KEY (id),
-- UNIQUE KEY uq_upload_chunk (upload_id, chunk_number),   
-- CONSTRAINT fk_chunk_upload
-- FOREIGN KEY (upload_id)
-- REFERENCES file_upload_sessions (upload_id)
-- ON DELETE CASCADE
-- ON UPDATE CASCADE

-- ) ENGINE=InnoDB
--   DEFAULT CHARSET=utf8mb4
--   COLLATE=utf8mb4_unicode_ci;

USE gam_db;
show tables;
