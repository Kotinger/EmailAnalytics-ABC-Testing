-- Active: 1788868810471@@127.0.0.1@3306@email_abc
-- схема. одна строка = один клиент после pipeline (id в датасете нет)
CREATE DATABASE IF NOT EXISTS email_abc
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE email_abc;

DROP TABLE IF EXISTS clean_users;

CREATE TABLE clean_users (
  recency INT NOT NULL,
  history_segment VARCHAR(32) NOT NULL,
  history DOUBLE NOT NULL,
  mens TINYINT NOT NULL,
  womens TINYINT NOT NULL,
  zip_code VARCHAR(16) NOT NULL,
  newbie TINYINT NOT NULL,
  channel VARCHAR(16) NOT NULL,
  test_group VARCHAR(32) NOT NULL,
  visit TINYINT NOT NULL,
  conversion TINYINT NOT NULL,
  spend DOUBLE NOT NULL,
  INDEX idx_test_group (test_group),
  INDEX idx_channel (channel),
  INDEX idx_zip (zip_code)
) ENGINE=InnoDB;
