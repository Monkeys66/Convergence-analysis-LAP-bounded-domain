from pathlib import Path
import pandas as pd
import numpy as np

project_root = Path(__file__).resolve().parent.parent

data_path = (
    project_root
    / "data_generation"
    / "ellipse_convergence.csv"
)

#transfer data from csv to panda dataframe
data_file = pd.read_csv(data_path)

epsilons = data_file["epsilon"].to_numpy()
relative_errors = data_file["relative_error"].to_numpy()
ratios = data_file["ratio"].to_numpy()

#check for positive and finite values
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
print(A.shape)
