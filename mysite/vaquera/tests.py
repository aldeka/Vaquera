from django.test import TestCase
from vaquera.models import Milestone
import datetime

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class MilestoneTest(TestCase):
    def test_end_of_month(self):
        self.average_month = datetime.date(2011,6,1)
        self.leap_year = datetime.date(2004,2,1)
        self.already_at_month_end = datetime.date(2011,8,31)
        
        self.assertEqual(Milestone.end_of_month(self.average_month), datetime.date(2011,6,30))
        self.assertEqual(Milestone.end_of_month(self.leap_year), datetime.date(2004,2,29))
        self.assertEqual(Milestone.end_of_month(self.already_at_month_end), datetime.date(2011,8,31))
        
    def test_generate_enddate(self):
        self.date = datetime.date(2011,6,1)
        self.other_date = datetime.date(2011,7,31)
        
        self.assertEqual(Milestone.generate_enddate(self.date,1),datetime.date(2011,7,31))
        self.assertEqual(Milestone.generate_enddate(self.date,14),datetime.date(2012,8,31))
        self.assertEqual(Milestone.generate_enddate(self.other_date,2),datetime.date(2011,9,30))