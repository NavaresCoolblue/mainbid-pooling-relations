import numpy as np
import pandas as pd
import logging
from pygam import LinearGAM

import settings_r as rs
import settings_m as ms
import utils as utils


# TODO: WHY DO WE NEED logging_input_data AS ARGUMENT?
def get_maxcpc_position(data):

    logger = logging.getLogger(ms.LOGNAME)
    logger.info("msg=get relations")

    fields_check = rs.FILTER + ['avgposition', 'maxcpc']
    check = [i for i in fields_check if i in list(data.columns)]
    if len(fields_check) != len(check):
        logger.error('error=cannot find all records in data')
        raise ValueError("Error get_position_cpc: I cannot find all records in data")

    groups = data[rs.FILTER].drop_duplicates().values


    df_ret = pd.DataFrame()  # initialization to avoid PEP8 warning
    for i in range(0, groups.shape[0]):

        selected, _ = utils.selection(data=data, group=groups[i], metric='maxcpc')

        selected = selected[pd.notnull(selected['maxcpc'])]


        if selected.shape[0] >= 2:
            selected_avgposition = list(selected['avgposition']) + [rs.MCPCPOS_MAX_CONVERGENCE] * 20
            selected_maxcpc = list(selected['maxcpc']) + [0] * 20

            x = list(1 / selected['avgposition'])
            x = x + [1/rs.MCPCPOS_MAX_CONVERGENCE] * 20
            y = list(selected['maxcpc'])
            y = y + [0] * 20

            coeffs = np.polyfit(x, y, deg=1)
            max_cpc = list((coeffs[0] * 1 / np.linspace(1.0, rs.MCPCPOS_MAX_POS, rs.MCPCPOS_N_POINTS)) + coeffs[1])
        else:
            selected_avgposition = list(selected['avgposition'])
            selected_maxcpc = list(selected['maxcpc'])
            max_cpc = [np.nan] * rs.MCPCPOS_N_POINTS

        avg_position = [round(x, 1) for x in list(np.linspace(1.0, rs.MCPCPOS_MAX_POS, rs.MCPCPOS_N_POINTS))]

        feed_dict, feed_dict_input_data = utils.format_output(group=groups[i],
                                                              metric='maxcpc',
                                                              metric_data=max_cpc,
                                                              position=avg_position,
                                                              selected_metric_data=selected_maxcpc,
                                                              selected_position=selected_avgposition)

        df_aux = pd.DataFrame(feed_dict)
        df_aux_input_data = pd.DataFrame(feed_dict_input_data)


        if i == 0:
            df_ret = df_aux
        else:
            df_ret = df_ret.append(df_aux)

    logger.info("msg=finish")
    # TODO: WHY COPY???
    return df_ret


def get_position_avgcpc(data):

    logger = logging.getLogger(ms.LOGNAME)
    logger.info("msg=get relations")

    fields_check = rs.FILTER + ['avgposition', 'avgcpc']
    check = [i for i in fields_check if i in list(data.columns)]
    if len(fields_check) != len(check):
        logger.error('error=cannot find all records in data')
        raise ValueError("Error get_position_cpc: I cannot find all records in data")

    groups = data[rs.FILTER].drop_duplicates().values

    df_ret = pd.DataFrame()  # initialization to avoid PEP8 warning
    for i in range(0, groups.shape[0]):

        selected, _ = utils.selection(data=data, group=groups[i], metric='maxcpc')
        selected = selected[pd.notnull(selected['avgcpc'])]

        if selected.shape[0] >= 2:
            x = list(selected['avgposition'])
            y = list(selected['avgcpc'])

            # force the logarithm to be 0 at position 5
            x = x + [rs.ACPCPOS_MAX_CONVERGENCE] * 20
            y = y + [0] * 20

            coeffs = np.polyfit(np.log(x), y, deg=1)
            avg_cpc = list(coeffs[0] * np.log(np.linspace(1.0, rs.ACPCPOS_MAX_POS, rs.ACPCPOS_N_POINTS)) + coeffs[1])
        else:
            avg_cpc = [np.nan] * rs.ACPCPOS_N_POINTS

        avg_position = [round(x, 1) for x in list(np.linspace(1.0, rs.ACPCPOS_MAX_POS, rs.ACPCPOS_N_POINTS))]

        feed_dict, _ = utils.format_output(group=groups[i],
                                           metric='avgcpc',
                                           metric_data=avg_cpc,
                                           position=avg_position)

        df_aux = pd.DataFrame(feed_dict)

        if i == 0:
            df_ret = df_aux
        else:
            df_ret = df_ret.append(df_aux)

    logger.info("msg=finish")

    return df_ret


# TODO: WHY DO WE NEED logging_input_data AS ARGUMENT?
def get_position_avgcpc_based_on_maxcpc(data, maxcpc_relation):

    logger = logging.getLogger(ms.LOGNAME)
    logger.info("msg=get relations")

    fields_check = rs.FILTER + ['avgposition', 'avgcpc']
    check = [i for i in fields_check if i in list(data.columns)]
    if len(fields_check) != len(check):
        logger.error('error=cannot find all records in data')
        raise ValueError("Error get_position_cpc: I cannot find all records in data")

    groups = data[rs.FILTER].drop_duplicates().values

    df_ret = pd.DataFrame()  # initialization to avoid PEP8 warning
    for i in range(0, groups.shape[0]):

        selected, selected_maxcpc = utils.selection(data=data,
                                                    group=groups[i],
                                                    metric='maxcpc_avgcpc',
                                                    maxcpc_relation=maxcpc_relation)

        selected = selected[pd.notnull(selected['avgcpc'])]

        if selected.shape[0] >= 2:
            x = np.array(selected['maxcpc'])
            x = np.log(x[:, np.newaxis]+1)
            y = np.array(selected['avgcpc'])
            coeffs, _, _, _ = np.linalg.lstsq(x, y, rcond=None)
            avg_cpc = list(coeffs[0] * np.log(selected_maxcpc['maxcpc']+1))

        else:
            avg_cpc = [np.nan] * rs.ACPCPOS_N_POINTS

        avg_position = [round(x, 1) for x in list(np.linspace(1.0, rs.ACPCPOS_MAX_POS, rs.ACPCPOS_N_POINTS))]

        feed_dict, feed_dict_input_data = utils.format_output(group=groups[i],
                                                              metric='maxcpc_avgcpc',
                                                              metric_data=avg_cpc,
                                                              position=avg_position,
                                                              selected_metric_data=selected['maxcpc'],
                                                              selected_position=selected['avgposition'],
                                                              selected_data=selected)

        df_aux = pd.DataFrame(feed_dict)
        df_aux_input_data = pd.DataFrame(feed_dict_input_data)


        if i == 0:
            df_ret = df_aux
        else:
            df_ret = df_ret.append(df_aux)

    logger.info("msg=finish")
    # TODO: WHY COPY???
    return df_ret


# TODO: WHY DO WE NEED logging_input_data AS ARGUMENT?
def get_position_cr(data):
    logger = logging.getLogger(ms.LOGNAME)
    logger.info("msg=get relations")

    fields_check = rs.FILTER + ['avgposition', 'conversionrate']
    check = [i for i in fields_check if i in list(data.columns)]
    if len(fields_check) != len(check):
        logger.error('error=cannot find all records in data')
        raise ValueError("Error get_position_cpc: I cannot find all records in data")

    groups = data[rs.FILTER].drop_duplicates().values

    df_ret = pd.DataFrame()  # initialization to avoid PEP8 warning
    for i in range(0, groups.shape[0]):

        selected, _ = utils.selection(data=data, group=groups[i], metric='cr')

        selected = selected[pd.notnull(selected['conversionrate'])]

        if selected.shape[0] >= 10:
            selected_avgposition = list(selected['avgposition']) + [rs.CR_MAX_CONVERGENCE] * 20
            selected_conversionrate = list(selected['conversionrate']) + [0] * 20

            x = list(selected['avgposition'])
            y = list(selected['conversionrate'])

            # force the logarithm to be 0 at position 0.5
            x = x + [rs.CR_MAX_CONVERGENCE] * 20
            y = y + [0] * 20

            coeffs = np.polyfit(np.log(x), y, deg=1)
            cr = list(coeffs[0] * np.log(np.linspace(1.0, rs.CR_MAX_POS, rs.CR_N_POINTS)) + coeffs[1])

        else:
            cr = [np.nan] * rs.CR_N_POINTS
            selected_avgposition = list(selected['avgposition'])
            selected_conversionrate = list(selected['conversionrate'])

        avg_position = [round(x, 1) for x in list(np.linspace(1.0, rs.CR_MAX_POS, rs.CR_N_POINTS))]

        feed_dict, feed_dict_input_data = utils.format_output(group=groups[i],
                                                              metric='cr',
                                                              metric_data=cr,
                                                              position=avg_position,
                                                              selected_data=selected,
                                                              selected_metric_data=selected_conversionrate,
                                                              selected_position=selected_avgposition)

        df_aux = pd.DataFrame(feed_dict)
        df_aux_input_data = pd.DataFrame(feed_dict_input_data)


        if i == 0:
            df_ret = df_aux
        else:
            df_ret = df_ret.append(df_aux)

    logger.info("msg=finish")

    return df_ret


def get_position_ctr(data):
    logger = logging.getLogger(ms.LOGNAME)
    logger.info("msg=get relations")

    fields_check = rs.FILTER + ['avgposition', 'clickthroughrate']
    check = [i for i in fields_check if i in list(data.columns)]
    if len(fields_check) != len(check):
        logger.error('error=cannot find all records in data')
        raise ValueError("Error get_position_cpc: I cannot find all records in data")

    groups = data[rs.FILTER].drop_duplicates().values

    df_ret = pd.DataFrame()  # initialization to avoid PEP8 warning
    for i in range(0, groups.shape[0]):

        selected, _ = utils.selection(data=data, group=groups[i], metric='ctr')

        if selected.shape[0] >= 2:
            selected_avgposition = list(selected['avgposition']) + [rs.CTR_MAX_CONVERGENCE] * 20
            selected_clickthroughrate = list(selected['clickthroughrate']) + [0] * 20

            x = list(1 / selected['avgposition']) + [1 / rs.CTR_MAX_CONVERGENCE] * 20
            y = list(selected['clickthroughrate']) + [0] * 20
            w = list(selected['impressions']) + [np.mean(selected['impressions'])] * 20

            coeffs = np.polyfit(x, y, deg=1)
            ctr = list((coeffs[0] * 1 / np.linspace(1.0, rs.CTR_MAX_POS, rs.CTR_N_POINTS)) + coeffs[1])

            check_decreasing = all(x1 >= x2 for x1, x2 in zip(ctr, ctr[1:]))

            if not check_decreasing:
                coeffsw = np.polyfit(x, y, w=w, deg=1)
                ctr = list((coeffsw[0] * 1 / np.linspace(1.0, rs.CTR_MAX_POS, rs.CTR_N_POINTS)) + coeffsw[1])

                check_decreasing2 = all(x1 >= x2 for x1, x2 in zip(ctr, ctr[1:]))
                if not check_decreasing2:
                    logger.info("msg=NON DECREASING SHAPE FOR CLICKTHROUGHRATE")

            check_negatives = [1 for xi in ctr if xi < 0]
            if len(check_negatives) > 0:
                msg = "NON DECREASING SHAPE FOR CLICKTHROUGHRATE: " + str(groups[i][0]) + ' ' + str(groups[i][1])
                logger.info("msg= " + msg)

        else:
            ctr = [np.nan] * rs.CTR_N_POINTS
            selected_avgposition = list(selected['avgposition'])
            selected_clickthroughrate = list(selected['clickthroughrate'])

        avg_position = [round(x, 1) for x in list(np.linspace(1.0, rs.CTR_MAX_POS, rs.CTR_N_POINTS))]

        feed_dict, feed_dict_input_data = utils.format_output(group=groups[i],
                                                              metric='ctr',
                                                              metric_data=ctr,
                                                              position=avg_position,
                                                              selected_data=selected,
                                                              selected_metric_data=selected_clickthroughrate,
                                                              selected_position=selected_avgposition)

        df_aux = pd.DataFrame(feed_dict)
        df_aux_input_data = pd.DataFrame(feed_dict_input_data)


        if i == 0:
            df_ret = df_aux
        else:
            df_ret = df_ret.append(df_aux)

    logger.info("msg=finish")

    return df_ret


def get_position_impressions(data):
    logger = logging.getLogger(ms.LOGNAME)
    logger.info("msg=get relations")

    # create the aggregation field
    data['aggregation'] = np.nan

    fields_check = rs.FILTER + ['avgposition', 'impressions']
    check = [i for i in fields_check if i in list(data.columns)]
    if len(fields_check) != len(check):
        logger.error('error=cannot find all records in data')
        raise ValueError("Error get_position_impressions: I cannot find all records in data")

    groups = data[rs.FILTER].drop_duplicates().values

    if ms.ab_test == 1:
        ab_test_file = pd.read_csv(ms.abtest_campaign_file)
        ab_test_file['draft-campaignid'] = ab_test_file['draft-campaignid'].astype('str')
        groups = groups[np.isin(groups[:, 0], list(ab_test_file['draft-campaignid']))]

    df_ret = pd.DataFrame()  # initialization to avoid PEP8 warning
    for i in range(0, groups.shape[0]):

        ret = utils.fallback_impressions(data, groups[i])

        selected = ret['data']

        model_df = pd.DataFrame({'AvgPosition': round(selected['avgposition'], 1),
                                 'Impressions': selected['impressions']})

        # aggregate by position,  add the dummy tail to force the spline
        # pass through 0 at MAX_POS_BID and calculate the CDF
        model_df = model_df.groupby('AvgPosition').agg('mean').reset_index()
        full_range = pd.DataFrame({'AvgPosition': np.linspace(1, rs.IMP_MAX_CONVERGENCE,
                                                              rs.IMP_N_POINTS_CONVERGENCE)})

        # complete the full positions observations
        model_df = pd.merge(full_range,
                            model_df,
                            left_on='AvgPosition',
                            right_on='AvgPosition',
                            how='left')
        model_df = model_df.fillna(0)

        x = list(model_df['AvgPosition'])
        y = list(model_df['Impressions'])

        # get the CDF
        # FIXME: statement #1 was changed for statement #2 possible conflict
        # STETEMENT #1:  probabilities = y / sum(y)
        # STETEMENT #2:  probabilities = [i / sum(y) for i in y]
        probabilities = [i / sum(y) for i in y]
        cdf = np.cumsum(probabilities[::-1])[::-1]

        # scale the cdf
        cdf = cdf * sum(y) / float(len(y))

        # reshape x to meet function requirements
        new_x = np.reshape(np.asarray(x), (np.asarray(x).shape[0], 1))
        gam = LinearGAM(n_splines=rs.IMP_N_SPLINES).fit(new_x, cdf)

        # FIXME: apparently predict() warning is due to PyCharm configuration
        impressions = np.clip(gam.predict(new_x), a_min=0, a_max=float('Inf'))[:rs.IMP_N_POINTS]

        avg_position = [round(x, 1) for x in list(np.linspace(1.0, rs.IMP_MAX_POS, rs.IMP_N_POINTS))]

        # TODO: parametrise (in settings) the indices for aggregation [3 or 4]
        # replace groups nan aggregation by the calculated in the fallback
        if 'device' in ms.GRANULARITY:
            groups[i, 4] = ret['aggregation']
        else:
            groups[i, 3] = ret['aggregation']

        feed_dict, feed_dict_input_data = utils.format_output(group=groups[i],
                                                              metric='impressions',
                                                              metric_data=impressions,
                                                              position=avg_position,
                                                              selected_data=selected,
                                                              selected_metric_data=y,
                                                              selected_position=x)

        df_aux = pd.DataFrame(feed_dict)
        df_aux_input_data = pd.DataFrame(feed_dict_input_data)

        if i == 0:
            df_ret = df_aux
        else:
            df_ret = df_ret.append(df_aux)

    logger.info("msg=finish")

    return df_ret
