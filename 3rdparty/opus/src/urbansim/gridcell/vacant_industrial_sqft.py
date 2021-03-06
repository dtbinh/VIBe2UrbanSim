# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from opus_core.misc import clip_to_zero_if_needed

class vacant_industrial_sqft(Variable):
    """ The industrial_sqft - sqft_of_industrial_jobs. """
    _return_type="float32"
    sqft_of_industrial_jobs = "sqft_of_industrial_jobs"
    industrial_sqft = "industrial_sqft"

    def dependencies(self):
        return [my_attribute_label(self.sqft_of_industrial_jobs), 
                my_attribute_label(self.industrial_sqft)]

    def compute(self, dataset_pool):
        indsqft = self.get_dataset().get_attribute(self.industrial_sqft)
        return clip_to_zero_if_needed(indsqft - 
                    self.get_dataset().get_attribute(self.sqft_of_industrial_jobs),
                                          'vacant_industrial_sqft')
   
    def post_check(self, values, dataset_pool):
        global_max = self.get_dataset().get_attribute(self.industrial_sqft).max()
        self.do_check("x >= 0 and x <= %s" % global_max, values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array
from numpy import ma
class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        sqft_of_industrial_jobs = array([1225, 5000, 7500])
        industrial_sqft = array([1995, 10000, 7500])

        tester = VariableTester(
            __file__,
            package_order=['urbansim'],
            test_data={
                "gridcell":{ 
                    "grid_id":array([1,2,3]),
                    "sqft_of_industrial_jobs":sqft_of_industrial_jobs, 
                    "industrial_sqft":industrial_sqft
                }
            }
        )
        
        should_be = array([770, 5000, 0])
        tester.test_is_equal_for_variable_defined_by_this_module(self, should_be)


if __name__=='__main__':
    opus_unittest.main()