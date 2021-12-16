from __future__ import print_function
from os import listdir
from os.path import isfile, join
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from scipy import stats
import math

verbose = False
verboseprint = print if verbose else lambda *a, **k: None


class data_post_processing:

    def __init__(self, csv_list=[], all_massflow=[], totalmassintube=0.15):
        self.path = r'C:\Users\Graphite\PycharmProjects\GranuFlowDigitalTwin\DEM_data'
        self.csv_list = csv_list
        self.all_massflow = all_massflow
        self.totalmassintube = totalmassintube
        self.d = {}
        self.lr_gradient = {}  # Linear regression gradient values
        self.lr_rvalue = {}  # Linear regression gradient values
        self.orifice_size = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
        self.dem_mass_flow_vals = {}

    def get_csv_file_list(self):        # Default path is current directory

        file_list = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        verboseprint(file_list)
        self.csv_list = [x for x in file_list if "csv" in x]
        verboseprint(self.csv_list)

    def plot_mass_flow(self):  # TODO: Separate function into two functions one for plot and one for extracting values.

        n = len(self.csv_list)
        colours = pl.cm.jet(np.linspace(0, 1, n))

        for i in range(len(self.csv_list)):

            col_name2 = self.csv_list[i]
            col_name2 = col_name2[12:-6]
            col_name = ['Time', col_name2]

            data = pandas.read_csv(self.path + '/' + self.csv_list[i], names=col_name, skiprows=[0])
            verboseprint(data.head())
            data = data.to_numpy()
            data = np.delete(data, 0, 0)

            time_raw = data[:, 0]
            time_adj = time_raw-time_raw[0]
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

            plt.scatter(time_adj, massflow, label='Orifice size: ' + col_name2 + ' mm', color=colours[i], s=1)  # Plot all mass flows

        plt.xlabel("Time (sec)")
        plt.ylabel("Mass Leaving GranuFlow Tube (Kg)")
        plt.legend()
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
            orifice_size = int(key)
            cutoff_massflow = values[(values >= lowerbound) & (values <= upperbound)]  # remove low and high values

            number_of_test_points = 20

            if len(cutoff_massflow) <= number_of_test_points:

                self.dem_mass_flow_vals[orifice_size] = [0]

            else:

                for i in range(len(cutoff_massflow)-number_of_test_points):

                    test_range = cutoff_massflow[i:i+number_of_test_points]
                    time = np.arange(0, 0.01*number_of_test_points, 0.01)

                    gradient, intercept, r_value, p_value, std_err = stats.linregress(time, test_range)

                    self.lr_gradient[i] = gradient*1000  # x1000 is to convert from kg to g.
                    self.lr_rvalue[i] = r_value  # R squared value.

                max_value = max(self.lr_gradient.values())  # Find max r squared (or gradient) value for eqn with best fit.

                for key, value in self.lr_gradient.items():
                    if value == max_value:
                        index = key
                        self.dem_mass_flow_vals[orifice_size] = [self.lr_gradient[index]]
                        # print(str(self.lr_gradient[index]) + ' g/sec')

        print(self.dem_mass_flow_vals)

    def beverloo_law_comparison(self):

        # 0.5 mm Particles
        # c = 0.58                # c and k are empirical constants in the Beverloo law.
        # k = 1.4
        # bulk_density = 0.6*1460*1000  # g/m3 (x1000 convert from kg to g, 0.6 is the packing density to get bulk density)
        # c_plus_dens = c*bulk_density
        # d_particle = 0.5/1000   # Particle size (metres)

        # MCC
        c_plus_dens = 0.0005
        k = 1
        d_particle = 1.2  # Particle diameter (meters)

        sqrtg = math.sqrt(9810)  # m/s2

        for i in range(len(self.orifice_size)):

            d_zero = self.orifice_size[i]  # Orifice size (m)
            beverloo_mass_flow_rate = c_plus_dens*sqrtg*(d_zero-(k*d_particle))**(5/2)  # Beverloo Law eqn g/s

            print(beverloo_mass_flow_rate)

            plt.scatter(self.orifice_size[i], beverloo_mass_flow_rate, color='b')

        for key, value in self.dem_mass_flow_vals.items():

            orifice_size = key
            dem_mass_flow_rate = value

            plt.scatter(orifice_size, dem_mass_flow_rate, marker='x', color='r')

        plt.scatter([2, 4, 8, 12, 18, 22, 28], [0, 0, 4.19, 14.27, 46.13, 81.01, 159.94], marker='v', color='g')

        plt.xlabel("Orifice size (mm)")
        plt.ylabel("Mass Flow Rate (g/sec)")
        plt.show()


run = data_post_processing()
run.get_csv_file_list()
run.plot_mass_flow()
run.get_mass_flow_rate()
run.beverloo_law_comparison()
