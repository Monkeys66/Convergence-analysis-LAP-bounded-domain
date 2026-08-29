from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

project_root = Path(__file__).resolve().parent.parent

data_path = (
    project_root
    / "data_generation"
    / "ellipse_convergence.csv"
)

# Transfer data from CSV to a pandas DataFrame.
data_file = pd.read_csv(data_path)

epsilons = data_file["epsilon"].to_numpy()
relative_errors = data_file["relative_error"].to_numpy()
ratios = data_file["ratio"].to_numpy()

# Check for positive and finite values.
if not np.all(epsilons > 0):
    raise ValueError("All epsilon values must be positive.")
if not np.all(relative_errors > 0):
    raise ValueError("All relative error values must be positive.")
if not np.all(ratios > 0):
    raise ValueError("All ratio values must be positive.")

if not np.all(np.isfinite(epsilons)):
    raise ValueError("All epsilon values must be finite.")
if not np.all(np.isfinite(relative_errors)):
    raise ValueError("All relative error values must be finite.")
if not np.all(np.isfinite(ratios)):
    raise ValueError("All ratio values must be finite.")

log_epsilons = np.log(epsilons)
log_relative_errors = np.log(relative_errors)

length = len(log_epsilons)
a_1 = np.ones(length)
A = np.vstack((a_1, log_epsilons)).T
a, p = np.linalg.lstsq(A, log_relative_errors, rcond=None)[0]

# Calculate fitted values and residuals in log space.
fitted_log_errors = a + p * log_epsilons
residuals = log_relative_errors - fitted_log_errors

# Calculate the coefficient of determination.
residual_sum_squares = np.sum(residuals ** 2)
total_sum_squares = np.sum(
    (log_relative_errors - np.mean(log_relative_errors)) ** 2
)
r_squared = 1 - residual_sum_squares / total_sum_squares

C = np.exp(a)

print(f"C = {C:.8f}")
print(f"p = {p:.8f}")
print(f"R^2 = {r_squared:.10f}")
print(f"Maximum absolute residual = {np.max(np.abs(residuals)):.3e}")

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Relative_error and ratio')

ax1.plot(
    log_epsilons,
    log_relative_errors,
    'ko',
    label='Original data',
    markersize=3,
)
ax1.plot(log_epsilons, fitted_log_errors, 'b', label='Fitted line')
ax1.set_xlabel('log(epsilon)')
ax1.set_ylabel('log(relative error)')
_ = ax1.legend()

ax2.plot(
    epsilons,
    ratios,
    'ko',
    markersize=3,
)
ax2.set_xlabel('epsilon')
ax2.set_ylabel('ratio')

plt.show()

