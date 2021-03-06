# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

#from urbansim.estimation.config import config
from urbansim_parcel.configs.controller_config import UrbansimParcelConfiguration
from urbansim.configurations.creating_baseyear_cache_configuration import CreatingBaseyearCacheConfiguration
from opus_core.configurations.baseyear_cache_configuration import BaseyearCacheConfiguration
from opus_core.configurations.dataset_pool_configuration import DatasetPoolConfiguration
from numpy import array
import os

class ConfigBuildingsNonResidential(UrbansimParcelConfiguration):
    def __init__(self):
        config = UrbansimParcelConfiguration()

        config_changes = {
            'description':'data preparation for PSRC parcel (buildings)',
            'cache_directory': None,
            'creating_baseyear_cache_configuration': CreatingBaseyearCacheConfiguration(
                #cache_directory_root = r'/Users/hana/urbansim_cache/psrc/parcel',
                cache_directory_root = r'/urbansim_cache/psrc_parcel',
                #cache_directory_root = r'/workspace/urbansim_cache/psrc_parcel',
                cache_from_database = False,
                baseyear_cache = BaseyearCacheConfiguration(
                    #existing_cache_to_copy = r'/Users/hana/urbansim_cache/psrc/cache_source_parcel',
                    existing_cache_to_copy = r'/urbansim_cache/psrc_parcel/cache_source',
                    #existing_cache_to_copy = r'/workspace/urbansim_cache/psrc_parcel/estimation',
                    years_to_cache = [2000]
                    ),
                cache_scenario_database = 'urbansim.model_coordinators.cache_scenario_database',
                ),
            'dataset_pool_configuration': DatasetPoolConfiguration(
                package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim', 'opus_core'],
                ),
            'base_year':2000,
            'years':(2001, 2001),
            'models':[ # models are executed in the same order as in this list
                 "expected_sale_price_model",
                 "development_proposal_choice_model",
                 "building_construction_model",
                ],
            "datasets_to_preload":{
                    'zone':{},
                    'household':{},
                    'building': {},
                   #'development_project_proposal': {}
                },
            "datasets_to_cache_after_each_model": [
                     'parcel', 'building', 'development_project_proposal', 'household', 'job'
                     ]
        }
        #use configuration in config as defaults and merge with config_changes
        config.replace(config_changes)
        self.merge(config)
        self['models_configuration']['development_proposal_choice_model']['controller']["import"] =  {
                       "psrc_parcel.models.development_proposal_sampling_model_by_zones":
                       "DevelopmentProposalSamplingModelByZones"
                       }
        self['models_configuration']['development_proposal_choice_model']['controller']["init"]["name"] =\
                        "DevelopmentProposalSamplingModelByZones"
        self['models_configuration']['development_proposal_choice_model']['controller']['run']['arguments']["zones"] = 'zone'
        self['models_configuration']['development_proposal_choice_model']['controller']['run']['arguments']["type"] = "'non_residential'"
        self['models_configuration']['expected_sale_price_model']['controller']["init"]['arguments']["filter_attribute"] = "'urbansim_parcel.development_project_proposal.is_size_fit'"
        self['models_configuration']['expected_sale_price_model']['controller']["prepare_for_run"]['arguments']["parcel_filter"] = \
            "'numpy.logical_and(numpy.logical_or(numpy.logical_not(urbansim_parcel.parcel.is_residential_land_use_type), numpy.logical_and(parcel.land_use_type_id==26, urbansim_parcel.parcel.is_non_residential_plan_type)), urbansim_parcel.parcel.vacant_land_area > 0)'"
                #"'numpy.logical_or(parcel.land_use_type_id==26, numpy.logical_and(urbansim_parcel.parcel.is_residential_land_use_type, urbansim_parcel.parcel.vacant_land_area > 0))'"
        self['models_configuration']['building_construction_model']['controller']["run"]['arguments']["consider_amount_built_in_parcels"] = False
        self['models_configuration']['building_construction_model']['controller']['run']['arguments']["current_year"] = 2000
                