-- общие KPI по всем
-- visit 15.67% | conversion 1.01% | spend mean 1.17
USE email_abc;

SELECT
  COUNT(*) AS users,
  SUM(visit) AS visit_n,
  ROUND(100 * AVG(visit), 2) AS visit_pct,
  SUM(conversion) AS conversion_n,
  ROUND(100 * AVG(conversion), 2) AS conversion_pct,
  ROUND(AVG(spend), 4) AS spend_mean
FROM clean_users;
