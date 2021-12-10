from __future__ import print_function
from os import listdir
from os.path import isfile, join
import pandas
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

verbose = False
verboseprint = print if verbose else lambda *a, **k: None


class data_post_processing:

    def __init__(self, path='.', csv_list=[], all_massflow=[], totalmassintube=0.05):
        self.path = path
        self.csv_list = csv_list
        self.all_massflow = all_massflow
        self.totalmassintube = totalmassintube
        self.d = {}
        self.lr_gradient = {}  # Linear regression gradient values
        self.lr_rvalue = {}  # Linear regression gradient values

    def get_csv_file_list(self, path='.'):        # Default path is current directory

        file_list = [f for f in listdir(path) if isfile(join(path, f))]
        verboseprint(file_list)
        self.csv_list = [x for x in file_list if "csv" in x]
        verboseprint(self.csv_list)

    def plot_mass_flow(self):  # TODO: Separate function into two functions one for plot and one for extracting values.

        for i in range(len(self.csv_list)):

            col_name2 = self.csv_list[i]
            col_name2 = col_name2[:-4]
            col_name = ['Time', col_name2]

            data = pandas.read_csv(self.path + '/' + self.csv_list[i], names=col_name, skiprows=[0])
            verboseprint(data.head())
            data = data.to_numpy()
            data = np.delete(data, 0, 0)

            time = data[:, 0]
            massflow = self.totalmassintube-data[:, 1]  # 0.05 is the total mass in the tube at the start.
            # Inverses the mass.

            values = np.ndarray.tolist(massflow)
            name = str(col_name2)
            self.d[name] = [values]

            # if i == 0:
            #     self.all_massflow = massflow
            # else:
            #     self.all_massflow = np.vstack([self.all_massflow, massflow])
            # print(self.all_massflow.shape)

            plt.plot(time, massflow)  # Plot all mass flows
        plt.show()

    def save_csv_file(self):  # TODO: Get this working.

        createcsv = input('Save csv file of all mass flow measurements? y/n')
        # if createcsv == 'y':
        #     if i == 0:
        #         fulldata = data
        #     else:
        #         fulldata = np.c_[fulldata, data[:, 1]]
        # elif createcsv == 'n':
        #
        # else:
        #     print('Please type y or n')

    def get_mass_flow_rate(self, lowerbound=0.05, upperbound=0.95):  # Lower and upper bound in percent.

        lowerbound = self.totalmassintube*lowerbound  # Convert to cutoff mass.
        upperbound = self.totalmassintube*upperbound

        for key, value in self.d.items():

            values = np.array(value)
            cutoff_massflow = values[(values >= lowerbound) & (values <= upperbound)]  # remove low and high values

            for i in range(len(cutoff_massflow)-5):

                test_range = cutoff_massflow[i:i+5]
                time = [0, 0.5, 1, 1.5, 2]
                gradient, intercept, r_value, p_value, std_err = stats.linregress(time, test_range)
                self.lr_gradient[i] = gradient
                self.lr_rvalue[i] = r_value

            max_value = max(self.lr_rvalue.values())
            for key, value in self.lr_rvalue.items():
                if value == max_value:
                    index = key
                    print(str(self.lr_gradient[index]*1000) + ' g/sec')


run = data_post_processing()
run.get_csv_file_list()
run.plot_mass_flow()
run.get_mass_flow_rate()
