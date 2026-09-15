-- разница vs No E-Mail в pp / $ (z/p и Welch в report)
-- плюс срезы channel и zip_code
USE email_abc;

SELECT
  ROUND(100 * (
    AVG(CASE WHEN test_group = 'Mens E-Mail' THEN visit END)
    - AVG(CASE WHEN test_group = 'No E-Mail' THEN visit END)
  ), 2) AS visit_mens_diff_pp,
  ROUND(100 * (
    AVG(CASE WHEN test_group = 'Womens E-Mail' THEN visit END)
    - AVG(CASE WHEN test_group = 'No E-Mail' THEN visit END)
  ), 2) AS visit_womens_diff_pp,
  ROUND(100 * (
    AVG(CASE WHEN test_group = 'Mens E-Mail' THEN conversion END)
    - AVG(CASE WHEN test_group = 'No E-Mail' THEN conversion END)
  ), 2) AS conv_mens_diff_pp,
  ROUND(100 * (
    AVG(CASE WHEN test_group = 'Womens E-Mail' THEN conversion END)
    - AVG(CASE WHEN test_group = 'No E-Mail' THEN conversion END)
  ), 2) AS conv_womens_diff_pp,
  ROUND(
    AVG(CASE WHEN test_group = 'Mens E-Mail' THEN spend END)
    - AVG(CASE WHEN test_group = 'No E-Mail' THEN spend END)
  , 4) AS spend_mens_diff,
  ROUND(
    AVG(CASE WHEN test_group = 'Womens E-Mail' THEN spend END)
    - AVG(CASE WHEN test_group = 'No E-Mail' THEN spend END)
  , 4) AS spend_womens_diff
FROM clean_users;

-- срез channel x visit
SELECT
  test_group,
  channel,
  COUNT(*) AS n,
  SUM(visit) AS visit_n,
  ROUND(100 * AVG(visit), 2) AS visit_pct
FROM clean_users
GROUP BY test_group, channel
ORDER BY test_group, channel;

-- срез zip_code x visit (в данных опечатка Surburban)
SELECT
  test_group,
  zip_code,
  COUNT(*) AS n,
  SUM(visit) AS visit_n,
  ROUND(100 * AVG(visit), 2) AS visit_pct
FROM clean_users
GROUP BY test_group, zip_code
ORDER BY test_group, zip_code;
