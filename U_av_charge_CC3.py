# Finding average voltage of CC CHARGING process
# With normalisation graph and elimintating anomalies which affect graph
# making as a function and getting data for all cycles


import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sohcharge import sohcharge1

# import dataframes
from pandas6 import load_df
dfs = load_df()



print('test')


# Nearest value function
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def charge_data(dataset):
    ab, charge_cycle = sohcharge1(dataset)

    # number of dataset using - 0,1,2 for 3 battery datasets

    x = dfs[dataset]
    print(x)

    # number of charge cycles:
    no_cc = len(x.columns)

    # Cycle range
    cc = list(range(0, no_cc))

    # create new empty lists which data will be added to from main dictionary, for graphs
    time = []
    charge_CC_voltage = []
    av = []
    chargetime = []
    fixedtime = []

    # loop to create graph:
    for i, column in x.items():
        # i is the discharge cycle number
        print('i: ', i)

        # print('Column 7 (time): ', column[7])

        # print('Column 2 (charge voltage): ', column[2])

        time.append(column[7])

        charge_CC_voltage.append(column[2])



        # apply below if above 4.2V and remove these values from charge_CC_voltage and time lists - need to create loop to eliminate not just first value
        # result = next(k for k, value in enumerate(charge_CC_voltage[i]) if value > 4.2 or value < 1)
        # del charge_CC_voltage[i][result]
        # del time[i][result]


        # finding the average voltage for each line before it reaches 4.2V
        nu = [n for n in charge_CC_voltage[i] if n < 4.2]
        # print('Voltages for current cycle: ', nu)

        test = charge_CC_voltage[i]
        # average voltage for current cycle
        av.append(sum(nu)/len(nu))
        print('Average voltage for current cycle: ', av[i])


        # time taken to charge: find index of the first value which reaches 4.2V
        result = next(k for k, value in enumerate(charge_CC_voltage[i]) if 4.2 < value < 8.0)
        print(charge_CC_voltage[i][result])

        # print('Time taken to reach full charge: ', time[i][result])
        chargetime.append(time[i][result])


        # voltage increment in fixed time: find index of value around generic time of 1000s
        # print('Closest time: ', time[i][find_nearest(time[i], value = 1000)])
        # print('Closest voltage: ', charge_CC_voltage[i][find_nearest(time[i], value = 1000)])
        fixedtime.append(charge_CC_voltage[i][find_nearest(time[i], value = 1000)])


        # plot graph
        plt.plot(time[i], charge_CC_voltage[i])
        print('test')



    # average time taken to charge
    t_av = sum(chargetime)/len(chargetime)
    print('Average time for all cycles (charge): ', t_av)

    # Average voltage increment in fixed time
    deltau_av = sum(fixedtime)/len(fixedtime)
    print('Average voltage increment in fixed time: ', deltau_av)


    plt.plot(time[i], charge_CC_voltage[i])
    plt.xlabel('Time (s)')
    plt.ylabel('Average voltage of CC charge process (V)')
    plt.xlim(0, 3500)
    plt.ylim(3.4, 4.3)
    # plt.show()


    # Normalising charge time data

    # Create an instance of the scaler
    scaler = MinMaxScaler()



    # deleting values which are affecting normalised data - any time values below 1000s
    # also deleting for the average voltage charge dataset and fixedtime voltage increment so that the combined table will have same no. cycles
    for value in chargetime:
        print(value)
        if value < 1000:
            val = chargetime.index(value)
            # idx.append(chargetime.index(value))
            print('aff')
            del chargetime[val]
            del cc[val]
            del av[val]
            del fixedtime[val]



    # Create numpy array of data
    chargetime_np = np.array(chargetime)


    # Reshape the array to have two dimensions
    chargetime_np = chargetime_np.reshape(-1, 1)

    # Normalize the data
    normalized_data = scaler.fit_transform(chargetime_np)



    # Convert back to list, to plot
    nd = normalized_data.tolist()
    plt.figure(2)
    plt.plot(cc, nd)
    plt.xlabel('Cycle')
    plt.ylabel('Normalised Feature 3')
    plt.show()

    # return average charge voltage, charge time, fixed time and cycles used for
    return av, nd, fixedtime, cc, ab, charge_cycle

