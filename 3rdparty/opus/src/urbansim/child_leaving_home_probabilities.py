# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.rate_based_probabilities import rate_based_probabilities

class child_leaving_home_probabilities(rate_based_probabilities):
    agent_set = 'person'
    rate_set = 'child_leaving_home_rates'
    