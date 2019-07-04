import settings_m as ms

if 'device' in ms.GRANULARITY:
    FILTER = ['campaignid', 'criterionid', 'adgroupid', 'device', 'aggregation',
              'producttype', 'country']
else:
    FILTER = ['campaignid', 'criterionid', 'adgroupid', 'aggregation',
              'producttype', 'country']


#  MAX CPC POSITION (MCPCPOS) RELATION FIELDS
MCPCPOS_N_POINTS = 31  # number of position points generated
MCPCPOS_MAX_POS = 4  # maximum position of interest
MCPCPOS_MAX_CONVERGENCE = 20

#  AVG CPC POSITION (ACPCPOS) RELATION FIELDS
ACPCPOS_N_POINTS = 31  # number of position points generated
ACPCPOS_MAX_POS = 4  # maximum position of interest
ACPCPOS_MAX_CONVERGENCE = 20  # at which position should the model should be forced to pass through 0

#  CR AVG POSITION PARAMETERS
CR_N_POINTS = 31  # number of position points generated
CR_MAX_POS = 4  # maximum position of interest
CR_MAX_CONVERGENCE = 0.5  # force curve through (0.5, 0)

#  CTR AVG POSITION PARAMETERS
CTR_N_POINTS = 31  # number of position points generated
CTR_MAX_POS = 4  # maximum position of interest
CTR_MAX_CONVERGENCE = 10

#  IMPRESSIONS AVG POSITION PARAMETERS
IMP_N_POINTS = 31  # number of position points generated
IMP_MAX_POS = 4  # maximum position of interest
IMP_MAX_CONVERGENCE = 7  # at which position should the model should be forced to pass through 0
IMP_N_POINTS_CONVERGENCE = 61  # number of positions in the full range from 1.0 to MAX_CONVERGENCE
IMP_N_SPLINES = 4  # to fit the GAM model
IMP_MIN_NPOINTS = 10  # min num of observations to fit the model
