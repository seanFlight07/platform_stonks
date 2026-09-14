CREATE TABLE company (
  code VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255),
  exchange VARCHAR(255)
  active BOOLEAN
);

CREATE TABLE price(
  code VARCHAR(255),
  date date,
  open DECIMAL,
  high DECIMAL,
  low DECIMAL,
  close DECIMAL,
  change_dollar DECIMAL,
  change_pct DECIMAL,
  volume BIGINT,
  PRIMARY KEY (code,date),
    REFERENCES company(code)
);
