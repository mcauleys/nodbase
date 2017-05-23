import pandas as pd # For utilization of dataframes
from nodbase.mongod.search import search_chrom


class Chromatogram:
    """
    Contains a list of retention times stored as strings, base peak intensity stored as float and total ion current
    stored as float.
    """
    def __init__(self, expID):
        self.expID = expID
        self.find_chrom()

    def find_chrom(self):
        self.chrom = search_chrom(self.expID)

    def print_csv(self):
        df = pd.DataFrame(self.chrom)
        df.to_csv('Testing', sep=",")

    def output(self):
        return self.chrom
