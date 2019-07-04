import time
import pandas as pd
import pickle as pk

import relations_functions as relfuncs
from threading import Thread
import warnings


def main():
    start_time = time.time()

    f1 = open('standalone_intput.pkl', 'rb')
    input_data = pk.load(f1)
    f1.close()

    f2 = open('product_data.pkl', 'rb')
    product_data = pk.load(f2)
    f2.close()

    maxcpc_aggregation = input_data['maxcpc_aggregation']
    avgcpc_aggregation = input_data['avgcpc_aggregation']
    clickthroughrate_aggregation = input_data['clickthroughrate_aggregation']
    conversionrate_aggregation = input_data['conversionrate_aggregation']

    position_maxcpc = relfuncs.get_maxcpc_position(maxcpc_aggregation)
    position_avgcpc = relfuncs.get_position_avgcpc_based_on_maxcpc(data=avgcpc_aggregation,
                                                                   maxcpc_relation=position_maxcpc)
    position_clickthroughrate = relfuncs.get_position_ctr(clickthroughrate_aggregation)
    position_conversionrate = relfuncs.get_position_cr(conversionrate_aggregation)
    position_impressions = relfuncs.get_position_impressions(product_data)

    return time.time() - start_time


if __name__ == '__main__':
    main()
