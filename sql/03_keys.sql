-- кривые группы - должно быть 0
-- id нет: зерно = строка, full-dup сняты в pipeline
USE email_abc;

SELECT
  COUNT(*) AS bad_group
FROM clean_users
WHERE test_group NOT IN ('No E-Mail', 'Mens E-Mail', 'Womens E-Mail');

SELECT COUNT(*) AS rows_n FROM clean_users;
-- ожидание: 57438
