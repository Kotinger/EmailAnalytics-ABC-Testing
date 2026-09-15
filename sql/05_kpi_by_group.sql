-- по группам: n / visit / conversion / spend - те же цифры что в report
-- No 11.52% visit | Mens 19.39% | Womens 16.08%
USE email_abc;

SELECT
  test_group,
  COUNT(*) AS n,
  SUM(visit) AS visit_n,
  ROUND(100 * AVG(visit), 2) AS visit_pct,
  SUM(conversion) AS conversion_n,
  ROUND(100 * AVG(conversion), 2) AS conversion_pct,
  ROUND(AVG(spend), 4) AS spend_mean
FROM clean_users
GROUP BY test_group
ORDER BY test_group;
