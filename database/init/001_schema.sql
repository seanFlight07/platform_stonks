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


CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user'
        CHECK (role IN ('user', 'admin')),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
