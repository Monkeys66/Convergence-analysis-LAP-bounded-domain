BEGIN;

INSERT INTO ellipse_convergence (
    epsilon, 
    relative_error
) 
VALUES
    (0.1,0.5), 
    (0.01,0.05), 
    (0.001,0.005), 
    (0.0001,0.0005)
;

SELECT 
    result_id,
    epsilon,
    relative_error,
    relative_error / epsilon AS ratio
FROM ellipse_convergence
ORDER BY epsilon DESC;

SELECT COUNT(*) AS total_rows 
FROM ellipse_convergence;

ROLLBACK;

SELECT COUNT(*) AS total_rows
FROM ellipse_convergence;