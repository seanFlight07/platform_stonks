CREATE TABLE company (
  code VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255),
  exchange VARCHAR(255),
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

  FOREIGN KEY (code)
      REFERENCES company(code)
);

CREATE TABLE exchange (
    exchange VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    blackout_start TIME NOT NULL,
    blackout_end TIME NOT NULL
);

INSERT INTO exchange (
    exchange,
    name,
    timezone,
    blackout_start,
    blackout_end
)
VALUES (
    'AX',
    'Australian Securities Exchange',
    'Australia/Sydney',
    '08:30',
    '18:00'
);
