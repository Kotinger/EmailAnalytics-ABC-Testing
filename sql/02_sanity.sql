-- сколько строк и как разбились группы (с pipeline)
-- у меня было: 57438 | No E-Mail 33.2% | Mens 33.4% | Womens 33.4%
USE email_abc;

SELECT COUNT(*) AS rows_n FROM clean_users;

SELECT
  test_group,
  COUNT(*) AS n,
  ROUND(100 * COUNT(*) / (SELECT COUNT(*) FROM clean_users), 2) AS share_pct
FROM clean_users
GROUP BY test_group
ORDER BY test_group;
