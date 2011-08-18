# Run this file to create seed data for development purposes. 
# Uses faker 0.0.4 and Factory Boy.

from faker import Faker
import factory
import random
import datetime

from django.contrib.auth.models import User
from vaquera.models import Vaquerita, Milestone, Issue

random.seed()

tags = ["usability", "bitesize", "design", "ruby", "css", "asynchronous", "super awesome"]
    
class IssueFactory(factory.Factory)
    i = Faker()
    name = i.lorem()[:random.randint(40,80)]
    author = get_random_model_instance(Vaquerita)
    priority = random.randint(1,5)
    status = random.randint(1,9)
    owner = get_random_model_instance_or_null(Vaquerita,3)
    milestone = get_random_model_instance_or_null(Milestone,5)

def create_fake_data():
    num_issues = 100
    num_vaqueritas = 20
    
    # make one old milestone
    m = Milestone(name="1.70",description="Really ancient milestone", end_date=datetime.date(1970,1,1))
    m.save()
    # make four other milestones using Milestone's update script -- one current, three future
    Milestone.safe_for_democracy()
    
    v = Faker()
    while num_vaqueritas > 0:
        vaquerita = Vaquerita.objects.create_user(username=v.username(),email=v.email())
        vaquerita.is_maintainer = dice_roll(8)
        vaquerita.save()
        num_vaqueritas = num_vaqueritas - 1
        
    while num_issues > 0:
        issue = IssueFactory()
        num_issues = num_issues - 1

def dice_roll(n):
    '''Random boolean generator. Returns True about 1/n of the time.'''
    return random.randint(1,n) == n
    
def get_random_model_instance(Model)
    total = Model.objects.count()
    return Model.objects.get(pk=random.randint(1,total))
    
def get_random_model_instance_or_null(Model,n)
    instance = get_random_model_instance(Model)
    if dice_roll(n):
        return null
    else:
        return instance