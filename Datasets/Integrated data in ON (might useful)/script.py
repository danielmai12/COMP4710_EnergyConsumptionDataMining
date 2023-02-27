import pandas as pd
import numpy as np
from openpyxl import load_workbook, Workbook
import re


def runDataSuite():
    file = 'contracted-embedded-generation-capacity-in-commercial-operation.csv'
    fileDF = pd.DataFrame