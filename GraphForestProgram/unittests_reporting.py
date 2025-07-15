import unittest
from typing import Dict
from classes.sim_reporting_class import SimReporting

""" Unit test class for the SimReporting class (classes/sim_reporting_class). """

class ReportingTest(unittest.TestCase):

    """ Test setup report data. """
    def test_reporting_dir(self):
        sim_report = SimReporting()
        self.assertEqual(sim_report.get_reporting_dir(), 'sim_files/')

    def test_initial_iterations(self):
        sim_report = SimReporting()
        self.assertEqual(sim_report.get_iterations(), 0)

    def test_initial_tree_data(self):
        sim_report = SimReporting()
        self.assertEqual(sim_report.get_tree_iteration_data(), [])

    def test_initial_rock_data(self):
        sim_report = SimReporting()
        self.assertEqual(sim_report.get_rock_iteration_data(), [])

    def test_initial_wildfire_data(self):
        sim_report = SimReporting()
        self.assertEqual(sim_report.get_wildfire_iteration_data(), [])

    def test_initial_sim_data(self):
        sim_report = SimReporting()
        self.assertEqual(isinstance(sim_report.get_sim_data_as_dict(), Dict), True)
        self.assertIn('Tree Population', sim_report.get_sim_data_as_dict().keys())
        self.assertIn('Non-combustible Land', sim_report.get_sim_data_as_dict().keys())
        self.assertIn('Wildfires', sim_report.get_sim_data_as_dict().keys())

    """ Test update data. """
    def test_update_sim_data(self):
        sim_report = SimReporting()
        sim_report.update_sim_data(1,2,3)
        self.assertEqual(sim_report.get_tree_iteration_data(), [1])
        self.assertEqual(sim_report.get_rock_iteration_data(), [2])
        self.assertEqual(sim_report.get_wildfire_iteration_data(), [3])
        sim_report.update_sim_data(3,2,1)
        self.assertEqual(sim_report.get_tree_iteration_data(), [1,3])
        self.assertEqual(sim_report.get_rock_iteration_data(), [2,2])
        self.assertEqual(sim_report.get_wildfire_iteration_data(), [3,1])

if __name__ == '__main__':
    unittest.main()