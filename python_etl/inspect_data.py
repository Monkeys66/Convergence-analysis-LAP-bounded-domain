from pathlib import Path
import pandas as pd

script_path = Path(__file__).resolve()
script_directory = script_path.parent
project_root = script_directory.parent

data_path = (
    project_root
    / "data_generation"
    / "ellipse_convergence.csv"
)

output_path = script_directory / "data.xlsx"

data_file = pd.read_csv(data_path)

data_file.head(8)
data_file.tail(10)
data_file.dtypes
data_file.info()
print(data_file.describe())

data_file.to_excel(
    output_path,
    sheet_name="data",
    index=False
)



