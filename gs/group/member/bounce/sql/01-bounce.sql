SET CLIENT_ENCODING = 'UTF8';
SET CLIENT_MIN_MESSAGES = WARNING;

CREATE TABLE bounce (
    -- When the bounce occurred
    date              TIMESTAMP WITH TIME ZONE  NOT NULL
                                                DEFAULT NOW(),
    -- Whose email is bouncing
    user_id           TEXT                      NOT NULL,
    -- The group that sent the bouncing message
    group_id          TEXT                      NOT NULL,
    site_id           TEXT                      NOT NULL,
    -- The email address that bounced.
    email             TEXT                      NOT NULL        
);
