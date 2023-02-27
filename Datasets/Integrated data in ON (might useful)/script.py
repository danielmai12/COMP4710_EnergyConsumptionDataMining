import pandas as pd
import numpy as np
from openpyxl import load_workbook, Workbook
import re


def runDataSuite():
    file = '2019_final_data_set.csv'
    fileDF = pd.DataFrame(pd.read_csv(file, low_memory=False))


runDataSuite()
