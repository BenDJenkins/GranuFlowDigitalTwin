from __future__ import print_function
from os import listdir
from os.path import isfile, join
import pandas

verbose = True
verboseprint = print if verbose else lambda *a, **k: None


class data_post_processing:

    def __init__(self, path='.', csv_list=[]):
        self.path = path
        self.csv_list = csv_list

    def get_csv_file_list(self, path='.'):        # Default path is current directory

        file_list = [f for f in listdir(path) if isfile(join(path, f))]
        verboseprint(file_list)
        self.csv_list = [x for x in file_list if "csv" in x]
        verboseprint(self.csv_list)

    def compile_csv_files_into_one(self):

        for i in range(len(self.csv_list)):

            col_name2 = self.csv_list[i]
            col_name2 = col_name2[:-4]
            col_name = ['Time', col_name2]

            data = pandas.read_csv(self.path + '/' + self.csv_list[i], names=col_name, skiprows=[0])
            verboseprint(data.head())
            data.to_csv('MassFlowrate.csv')


run = data_post_processing()
run.get_csv_file_list()
run.compile_csv_files_into_one()
