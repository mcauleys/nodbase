from nodbase.mongod.search import search_ms
import pandas as pd # For utilization of dataframes


class MS:
    def __init__(self, expID, retentiontime):
        self.expID = expID
        self.retentiontime = retentiontime
        print(self.expID)
        print(self.retentiontime)
        self.find_ms()

    def find_ms(self):
        self.ms = search_ms(self.expID, self.retentiontime)

    def print_csv(self):
        df = pd.DataFrame(self.ms)
        df.to_csv('Testing', sep=",")

    def output(self):
        return self.ms
