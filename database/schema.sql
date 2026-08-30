CREATE TABLE ellipse_convergence (
    result_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    epsilon DOUBLE PRECISION NOT NULL,
    relative_error DOUBLE PRECISION NOT NULL,

    CONSTRAINT epsilon_positive CHECK (epsilon > 0),
    CONSTRAINT relative_error_nonnegative CHECK (relative_error >= 0),
    CONSTRAINT epsilon_unique UNIQUE (epsilon)
);

