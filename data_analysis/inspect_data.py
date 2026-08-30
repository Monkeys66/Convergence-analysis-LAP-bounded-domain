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

#transfer data from csv to panda dataframe
data_file = pd.read_csv(data_path)

#information of the data file
data_file.dtypes
data_file.info()
summary = data_file.describe()
summary.to_csv(
    script_directory 
    / "summary.csv",
    index=True
)

#transfer data from panda dataframe to excel file
data_file.to_excel(
    output_path,
    sheet_name="data",
    index=False
)




