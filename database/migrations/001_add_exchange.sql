CREATE TABLE exchange (
    code VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    blackout_start TIME NOT NULL,
    blackout_end TIME NOT NULL
);

INSERT INTO exchange (
    code,
    name,
    timezone,
    blackout_start,
    blackout_end
)
VALUES (
    'ASX',
    'Australian Securities Exchange',
    'Australia/Sydney',
    '08:30',
    '18:00'
);
