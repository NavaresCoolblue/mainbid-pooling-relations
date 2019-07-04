import time
import pandas as pd
import pickle as pk

import relations_functions as relfuncs
from multiprocessing import Process, Pool
from functools import partial


def func(metric, data_dic):
    if metric == 'avgcpc':
        arg1 = data_dic['avgcpc_aggregation']
        arg2 = data_dic['position_maxcpc']
        return relfuncs.get_position_avgcpc_based_on_maxcpc(data=arg1,
                                                            maxcpc_relation=arg2)
    if metric == 'ctr':
        arg = data_dic['clickthroughrate_aggregation']
        return relfuncs.get_position_ctr(arg)
    if metric == 'cr':
        arg = data_dic['conversionrate_aggregation']
        return relfuncs.get_position_cr(arg)
    if metric == 'imp':
        arg = data_dic['product_data']
        return relfuncs.get_position_impressions(arg)


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
    input_data['product_data'] = product_data
    input_data['position_maxcpc'] = position_maxcpc

    input_pool = ['avgcpc',
                  'ctr',
                  'cr',
                  'imp']

    pool = Pool(processes=4)
    partial_func = partial(func, data_dic=input_data)
    res = pool.map(partial_func, input_pool)
    return time.time() - start_time


if __name__ == '__main__':
    main()
