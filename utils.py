import logging
import pandas as pd

import settings_r as rs
import settings_m as ms


# for impressions
def get_filter_condition(df):
    dat = pd.DataFrame({'AvgPosition': round(df['avgposition'], 0),
                        'Impressions': df['impressions']})
    agg_condition = dat.groupby('AvgPosition').sum().reset_index()
    available_pos = list(agg_condition[agg_condition['Impressions'] > 0]['AvgPosition'])

    cond = sum([1 for x in available_pos if x in [1, 2, 3, 4]])

    if cond == 4:
        return True
    else:
        return False


def fallback_impressions(df, groups):
    logger = logging.getLogger(ms.LOGNAME)
    # logger.info("msg=impressions fallback")

    if 'device' in ms.GRANULARITY:
        selected = df.loc[(df[rs.FILTER[0]] == groups[0]) &  # CAMPAIGN
                          (df[rs.FILTER[1]] == groups[1]) &  # CRITERION
                          (df[rs.FILTER[2]] == groups[2]) &  # ADGROUP
                          (df[rs.FILTER[3]] == groups[3]) &  # DEVICE
                          (df[rs.FILTER[5]] == groups[5]) &  # PRODUCTTYPE
                          (df[rs.FILTER[6]] == groups[6])    # COUNTRY
                          ]
    else:
        selected = df.loc[(df[rs.FILTER[0]] == groups[0]) &  # CAMPAIGN
                          (df[rs.FILTER[1]] == groups[1]) &  # CRITERION
                          (df[rs.FILTER[2]] == groups[2]) &  # ADGROUP
                          (df[rs.FILTER[4]] == groups[4]) &  # PRODUCTTYPE
                          (df[rs.FILTER[5]] == groups[5])    # COUNTRY
                          ]

    if get_filter_condition(selected):
        return {'data': selected, 'aggregation': "criterion"}

    if 'device' in ms.GRANULARITY:
        selected = df.loc[(df[rs.FILTER[0]] == groups[0]) &  # CAMPAIGN
                          (df[rs.FILTER[2]] == groups[2]) &  # ADGROUP
                          (df[rs.FILTER[3]] == groups[3]) &  # DEVICE
                          (df[rs.FILTER[5]] == groups[5]) &  # PRODUCTTYPE
                          (df[rs.FILTER[6]] == groups[6])    # COUNTRY
                          ]
    else:
        selected = df.loc[(df[rs.FILTER[0]] == groups[0]) &  # CAMPAIGN
                          (df[rs.FILTER[2]] == groups[2]) &  # ADGROUP
                          (df[rs.FILTER[4]] == groups[4]) &  # PRODUCTTYPE
                          (df[rs.FILTER[5]] == groups[5])    # COUNTRY
                          ]
    if get_filter_condition(selected):
        return {'data': selected, 'aggregation': "adgroup"}

    if 'device' in ms.GRANULARITY:
        selected = df.loc[(df[rs.FILTER[0]] == groups[0]) &  # CAMPAIGN
                          (df[rs.FILTER[3]] == groups[3]) &  # DEVICE
                          (df[rs.FILTER[5]] == groups[5]) &  # PRODUCTTYPE
                          (df[rs.FILTER[6]] == groups[6])    # COUNTRY
                          ]
    else:
        selected = df.loc[(df[rs.FILTER[0]] == groups[0]) &  # CAMPAIGN
                          (df[rs.FILTER[4]] == groups[4]) &  # PRODUCTTYPE
                          (df[rs.FILTER[5]] == groups[5])    # COUNTRY
                          ]
    if get_filter_condition(selected):
        return {'data': selected, 'aggregation': "campaign"}

    if 'device' in ms.GRANULARITY:
        selected = df.loc[(df[rs.FILTER[3]] == groups[3]) &  # DEVICE
                          (df[rs.FILTER[5]] == groups[5]) &  # PRODUCTTYPE
                          (df[rs.FILTER[6]] == groups[6])    # COUNTRY
                          ]
    else:
        selected = df.loc[(df[rs.FILTER[4]] == groups[4]) &  # PRODUCTTYPE
                          (df[rs.FILTER[5]] == groups[5])    # COUNTRY
                          ]
    if get_filter_condition(selected):
        return {'data': selected, 'aggregation': "producttype"}
    else:
        msg = "Impression filter not passed, but continued using producttypes aggregation for producttype: "
        msg = msg + str(groups[4]) + " and criterionid " + str(groups[1])
        logger.info("msg=" + msg)
        return {'data': selected, 'aggregation': "producttype"}


def selection(data, group, metric=None, maxcpc_relation=None):

    logger = logging.getLogger(ms.LOGNAME)

    if metric is None:
        logger.error('error=metric not defined')
        raise ValueError("Error selection: metric not defined")

    if 'device' in ms.GRANULARITY:
        selected = data.loc[(data[rs.FILTER[0]] == group[0]) &
                            (data[rs.FILTER[1]] == group[1]) &
                            (data[rs.FILTER[2]] == group[2]) &
                            (data[rs.FILTER[3]] == group[3]) &
                            (data[rs.FILTER[4]] == group[4]) &
                            (data[rs.FILTER[5]] == group[5]) &
                            (data[rs.FILTER[6]] == group[6])
                            ]
    else:
        selected = data.loc[(data[rs.FILTER[0]] == group[0]) &
                            (data[rs.FILTER[1]] == group[1]) &
                            (data[rs.FILTER[2]] == group[2]) &
                            (data[rs.FILTER[3]] == group[3]) &
                            (data[rs.FILTER[4]] == group[4]) &
                            (data[rs.FILTER[5]] == group[5])
                            ]

    if metric == 'maxcpc_avgcpc':
        # TODO: DEVICE?????
        selected_metric = maxcpc_relation.loc[(maxcpc_relation['campaignid'] == group[0]) &
                                              (maxcpc_relation['criterionid'] == group[1]) &
                                              (maxcpc_relation['adgroupid'] == group[2]) &
                                              (maxcpc_relation['producttype'] == group[4]) &
                                              (maxcpc_relation['country'] == group[5])]\
            .sort_values(by=['avgposition'])
    else:
        selected_metric = None

    return selected, selected_metric


# TODO: optimize this function for readability
def format_output(group, metric=None, metric_data=None,
                  position=None, selected_data=None,
                  selected_metric_data=None, selected_position=None):

    logger = logging.getLogger(ms.LOGNAME)

    if metric is None:
        logger.error('error=metric not defined')
        raise ValueError("Error selection: metric not defined")

    n_points = None
    if metric == 'maxcpc':
        n_points = rs.MCPCPOS_N_POINTS

    if metric == 'avgcpc':
        n_points = rs.ACPCPOS_N_POINTS

    if metric == 'maxcpc_avgcpc':
        n_points = rs.ACPCPOS_N_POINTS

    if metric == 'cr':
        n_points = rs.CR_N_POINTS

    if metric == 'ctr':
        n_points = rs.CTR_N_POINTS

    if metric == 'impressions':
        n_points = rs.IMP_N_POINTS

    if n_points is None:
        logger.error('error=' + str(metric) + 'not found')
        raise ValueError

    # needed to porperly map group fields
    aggregation_index = None

    if 'device' in ms.GRANULARITY:
        feed_dict = {'producttype': [group[5]] * n_points,
                     'campaignid': [group[0]] * n_points,
                     'adgroupid': [group[2]] * n_points,
                     'criterionid': [group[1]] * n_points,
                     'country': [group[6]] * n_points,
                     'device': [group[3]] * n_points,
                     'avgposition': position
                     }
        aggregation_index = 4
    else:
        feed_dict = {'producttype': [group[4]] * n_points,
                     'campaignid': [group[0]] * n_points,
                     'adgroupid': [group[2]] * n_points,
                     'criterionid': [group[1]] * n_points,
                     'country': [group[5]] * n_points,
                     'avgposition': position
                     }
        aggregation_index = 3

    # feed specific dict fields
    if metric == 'maxcpc':
        feed_dict['maxcpc'] = metric_data
        feed_dict['aggregation_maxcpc_relation'] = [group[aggregation_index]] * n_points

    if metric == 'avgcpc':
        feed_dict['avgcpc'] = metric_data
        feed_dict['aggregation_avgcpc_relation'] = [group[aggregation_index]] * n_points

    if metric == 'maxcpc_avgcpc':
        feed_dict['avgcpc'] = metric_data
        feed_dict['aggregation_avgcpc_relation'] = [group[aggregation_index]] * n_points

    if metric == 'cr':
        feed_dict['conversionrate'] = metric_data
        feed_dict['aggregation_conversionrate_relation'] = [group[aggregation_index]] * n_points

    if metric == 'ctr':
        feed_dict['clickthroughrate'] = metric_data
        feed_dict['aggregation_clickthroughrate_relation'] = [group[aggregation_index]] * n_points

    if metric == 'impressions':
        feed_dict['impressions'] = metric_data
        feed_dict['aggregation_impressions_relation'] = [group[aggregation_index]] * n_points

    if metric in ['maxcpc', 'maxcpc_avgcpc', 'cr', 'ctr', 'impressions']:
        if 'device' in ms.GRANULARITY:
            feed_dict_input_data = {'producttype': [group[5]] * len(selected_data),
                                    'campaignid': [group[0]] * len(selected_data),
                                    'adgroupid': [group[2]] * len(selected_data),
                                    'criterionid': [group[1]] * len(selected_data),
                                    'country': [group[6]] * len(selected_data),
                                    'device': [group[3]] * len(selected_data),
                                    'avgposition': selected_position
                                    }
        else:
            feed_dict_input_data = {'producttype': [group[4]] * len(selected_metric_data),
                                    'campaignid': [group[0]] * len(selected_metric_data),
                                    'adgroupid': [group[2]] * len(selected_metric_data),
                                    'criterionid': [group[1]] * len(selected_metric_data),
                                    'country': [group[5]] * len(selected_position),
                                    'avgposition': selected_position
                                    }

        # feed specific dict fields
        if metric == 'maxcpc':
            feed_dict_input_data['maxcpc'] = selected_metric_data
            feed_dict_input_data['aggregation_maxcpc_relation'] = [group[aggregation_index]] * len(selected_position)

        if metric == 'avgcpc':
            feed_dict['avgcpc'] = selected_metric_data
            feed_dict['aggregation_avgcpc_relation'] = [group[aggregation_index]] * len(selected_position)

        if metric == 'maxcpc_avgcpc':
            feed_dict_input_data['avgcpc'] = selected_data['avgcpc']
            feed_dict_input_data['maxcpc'] = selected_metric_data
            feed_dict_input_data['aggregation_avgcpc_relation'] =\
                [group[aggregation_index]] * len(selected_position)

        if metric == 'cr':
            feed_dict_input_data['conversionrate'] = selected_metric_data
            feed_dict_input_data['aggregation_conversionrate_relation'] = \
                [group[aggregation_index]] * len(selected_position)

        if metric == 'ctr':
            feed_dict_input_data['clickthroughrate'] = selected_metric_data
            feed_dict_input_data['aggregation_clickthroughrate_relation'] = \
                [group[aggregation_index]] * len(selected_position)

        if metric == 'impressions':
            feed_dict_input_data['impressions'] = selected_metric_data
            feed_dict_input_data['aggregation_impressions_relation'] = \
                [group[aggregation_index]] * len(selected_position)

    else:
        feed_dict_input_data = None

    return feed_dict, feed_dict_input_data
