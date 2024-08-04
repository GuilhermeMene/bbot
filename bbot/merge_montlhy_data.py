"""
Script to prepare the data before using machine learning
"""

import zipfile
import os
import numpy as np

period = "5m"
PATH_DATA = "data"

files = os.listdir(os.path.join(PATH_DATA, period))

column_names = "OpenTime, Open, High, Low, Close, Volume, CloseTime, qAssetVol, Ntrades, TbuybAssetVol, TbuyqAssetVol, Ignore"

#Create a final file with column of the data
with open(os.path.join(PATH_DATA, period,f"Data_{period}.csv"), "w") as file:
    file.write(column_names + "\n")
    for f in files:
        print(f"Reading the file: {f}.\n")
        archive = zipfile.ZipFile(os.path.join(PATH_DATA, period, f))
        fname = f[:-4]
        fname = fname + ".csv"

        file.write(archive.read(fname).decode("utf-8"))

#Close text file
file.close()
