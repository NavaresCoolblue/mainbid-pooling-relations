from datetime import datetime
from dateutil.relativedelta import relativedelta


LOGNAME = 'root'

#
#  MAINFLOW CONTROL COMMANDS
ab_test = 0  # ab test control(=1 to generate abtest; =0 otherwise)
debug_mode = 1  # in order to run retrospectively
debug_mode_days_back = 1

if debug_mode == 1:
    ed = datetime.today() + relativedelta(days=-1) + relativedelta(days=-debug_mode_days_back)
    ed = ed.strftime('%Y-%m-%d')

    sd = datetime.today() + relativedelta(months=-3)
    sd = sd.strftime('%Y-%m-%d')
else:
    ed = datetime.today() + relativedelta(days=-1)
    ed = ed.strftime('%Y-%m-%d')

    sd = datetime.today() + relativedelta(months=-3)
    sd = sd.strftime('%Y-%m-%d')


sdmr = datetime.today() + relativedelta(weeks=-5)
if sdmr >= datetime.strptime("2019-01-21", "%Y-%m-%d"):
    sdmr = datetime.today() + relativedelta(weeks=-4)
sdmr = sdmr.strftime('%Y-%m-%d')

start_date = "'''" + sd + "'''"
end_date = "'''" + ed + "'''"

start_date_most_recent_data = "'''" + sdmr + "'''"
end_date_most_recent_data = "'''" + ed + "'''"

start_date_ab_test = "20190329"

abtest_campaign_file = './resources/DS ETV Bidding Experiment V3 - Campaigns.csv'

external_customer_id = ['6085496366']

#
# FALLBACK metricsx
fb_metrics = ['maxcpc', 'avgcpc', 'ctr', 'cr']

#
# SETTINGS FOR AGGREGATION SELECTION
MIN_OBSERVATIONS = 10
MIN_AVG_IMPRESSIONS = 10
MIN_AVG_CLICKS = 30 / MIN_OBSERVATIONS
MIN_AVG_ORDERS = 3 / MIN_OBSERVATIONS

MIN_OBSERVATIONS_RECENT_DATA = 7
MIN_IMPRESSIONS_RECENT_DATA = 100
MIN_CLICKS_RECENT_DATA_AVGCPC = 30
MIN_CLICKS_RECENT_DATA_CTR = 1
MIN_CLICKS_RECENT_DATA_CVR = 50
MIN_CLICKS_RECENT_DATA_CVR_WITHOUT_ORDERS = 300
MIN_ORDERS_RECENT_DATA_CVR = 1
MIN_ORDERS_RECENT_DATA_WITHOUT_CLICKS = 6
MIN_ORDERS_RECENT_DATA_TV = 10

MIN_UNIQUE_X = 2
MIN_UNIQUE_Y = 2

## SETTINGS FOR MAXCPC
LOWER_BOUND_BIDS = 0.05
UPPER_BOUND_BIDS = 2.5

RAW_DATA_COLUMNS = ["date",
                    "device",
                    "country",
                    # "slot",
                    "producttype",
                    "campaignid",
                    "adgroupid",
                    "criterionid",
                    "avgposition",
                    "maxcpc",
                    "avgcpc",
                    "impressions",
                    "clickthroughrate",
                    "clicks",
                    "conversionrate",
                    "orders",
                    "transactionvalue",
                    # "qualityscore",
                    # "eligibleimpressions",
                    # "coolbluetraffic",
                    # "coolblueconversionrate",
                    # "priceindextier1"
                    ]

MOST_RECENT_DATA_RAW_COLUMNS = ["date",
                                "device",
                                "country",
                                "channel",
                                "funnel",
                                "matchtype",
                                "producttype",
                                "campaignid",
                                "adgroupid",
                                "criterionid",
                                "avgposition",
                                "maxcpc",
                                "avgcpc",
                                "impressions",
                                "clickthroughrate",
                                "clicks",
                                "conversionrate",
                                "orders",
                                "transactionvalue"]

GRANULARITY = ["country", "producttype",
               "campaignid", "adgroupid",
               "criterionid"]

CONTRIBUTION_CURVES_FIELDS = ['campaignid',
                              'adgroupid',
                              'criterionid',
                              'producttype',
                              'country',
                              'avgposition',
                              'aggregation_maxcpc_relation',
                              'maxcpc',
                              'aggregation_avgcpc_relation',
                              'avgcpc',
                              'aggregation_impressions_relation',
                              'impressions',
                              'aggregation_clickthroughrate_relation',
                              'clickthroughrate',
                              'aggregation_conversionrate_relation',
                              'conversionrate']

product_type = ['24137'
                , '2080'
                , '2065'
                , '17633'
                , '2037'
                , '2041'
                , '12204'
                , '2456'
                , '2301'
                , '2095'
                , '5639'
                , '2797'
                , '2038'
                , '5626'
                , '2275'
                , '2420'
                , '2053'
                , '2109'
                , '2560'
                , '13362'
                , '2556'
                , '2308'
                , '2079'
                , '3390'
                , '2327'
                , '2340'
                , '5600'
                , '2694'
                , '5529'
                , '2102'
                , '5307'
                , '18132'
                , '2442'
                , '2042'
                , '2057'
                , '2558'
                , '5618'
                , '2619'
                , '14325'
                , '7003'
                , '13361'
                , '2419'
                , '11403'
                , '2622'
                , '14408'
                , '12217'
                , '2254'
                , '2307'
                , '3189'
                , '13360'
                , '23438'
                , '5528'
                , '24440'
                , '13353'
                , '13754'
                , '17633'
                , '16124'
                , '18729']
