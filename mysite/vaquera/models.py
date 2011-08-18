from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
import datetime

class Vaquerita(User):
    '''Model for all logged-in users of the bugtracker -- uses Django's built-in user model'''
    is_maintainer = models.BooleanField(default=False)
    
class Tag(models.Model):
    '''Model for all tags on bugs'''
    name = models.CharField(max_length=100)
    
    def clean(self):
        '''checks if any issue out there is using the tag--if not, it deletes itself'''
        if self.issue__set.all() == []:
            self.delete()
    
    def __unicode__(self):
        return self.name
        
class Milestone(models.Model):
    '''Model for milestones -- a group of bugs with a due date, e.g. a sprint or a release'''
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    end_date = models.DateField()
    
    @staticmethod
    def safe_for_democracy():
        # what's today's date?
        today = datetime.date.today()
        # what's the newest date that ought to have a milestone?
        latest_milestone_date = generate_enddate(today,3)
        
        # check that we're up to date on past milestones
        latest = Milestone.objects.all().order_by('-end_date')[0]
        while latest.end_date < latest_milestone_date:
            # as long as we aren't up-to-date, make a milestone for one month ahead
            new_end_date = generate_enddate(latest.end_date, 1)
            m = Milestone(end_date=new_end_date, name=default_name(new_end_date))
            m.save()
            # then mark the milestone we just created as the latest milestone
            latest = m
        
    @staticmethod
    def generate_enddate(date,n):
        '''adds n months to a given date, and returns the last day of the resulting month'''
        if (date.month + n) / 12 >= 1:
            new_month = (date.month + n) % 12
            new_year = date.year + ((date.month + n) // 12)
            new_date = datetime.date(new_year, new_month, date.day)
            return end_of_month(new_date)
        else:
            new_date = datetime.date(date.year, date.month + n, date.day)
            return end_of_month(new_date)
            
    @staticmethod
    def is_end_of_month(date):
        # get the date for the next day
        new_date = date + datetime.timedelta(days=1)
        # if the month value is different, it's the end of the month
        return date.month != new_date.month
        
    @staticmethod
    def end_of_month(date):
        max_tries = 32
        a_day = datetime.timedelta(days=1)
        while max_tries > 0:
            if is_end_of_month(date):
                return date
            else:
                date = date + a_day
                max_tries = max_tries - 1
        return "Oh crap. Something has gone wrong."
        
    @staticmethod
    def default_name(date):
        '''Returns a default name for a milestone, based on the month and the year'''
        return str(date.month) + '.' + str(date.year)
        
    def is_current(self):
        '''Returns true if this milestone is the current milestone'''
        today = datetime.date.today()
        return today.month == self.end_date.month
        
    def is_past(self):
        '''Returns true if the milestone's end date has passed'''
        today = datetime.date.today()
        return today > self.end_date
    
    def is_empty(self):
        '''Determines if this milestone doesn't have any issues in it'''
        return self.issue_set.count() == 0
    
    def completion_level(self):
        '''Calculates how complete a milestone is to having all its bugs closed (either resolved or deferred)'''
        total_issues = self.issue_set.count()
        
        # 0.0 makes it a float instead of an int
        closed_issues = self.issue_set.filter(status__exact='res').count() + self.issue_set.filter(status__exact='def').count() + 0.0
        
        # note to self: use floatformat in templates to make this truncate to one decimal place
        percent_complete = (closed_issues / total_issues) * 100
        return percent_complete
        
    def is_complete(self):
        '''Returns a boolean that is True if the milestone's completion level is 100 percent and the milestone isn't empty'''
        return self.completion_level == 100.0 and not (self.is_empty and self.is_past)
            

class Issue(models.Model):
    '''Model for all bugs and feature requests that the tracker tracks'''
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Vaquerita', blank=True, null=True, related_name='authored_issue_set', on_delete=models.SET_NULL)
    priority_choices = (
        (1, 'critical'),
        (2, 'urgent'),
        (3, 'bug'),
        (4, 'feature'),
        (5, 'wish'),
        )
    # the importance level of the bug
    priority = models.PositiveIntegerField(choices=priority_choices)
    status_choices = (
        (1, 'unread'),
        (2, 'chatting'),
        (3, 'needing example'),
        (4, 'in progress'),
        (5, 'needing decision'),
        (6, 'needing review'),
        (7, 'done'),
        (8, 'deferred'),
        (9, 'reopened'),
    )
    # how far the bug is along towards being closed
    status = models.PositiveIntegerField(choices=status_choices,default=1)
    owner = models.ForeignKey('Vaquerita', blank=True, null=True, related_name='owned_issue_set')
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    followers = models.ManyToManyField('Vaquerita',blank=True,null=True, related_name='followed_issue_set')
    milestone = models.ForeignKey('Milestone', blank=True, null=True)
    # for keeping track of dependencies and other relationships between issues -- the exact relation is left to be hashed out in the comments
    also_see = models.ManyToManyField("self", blank=True, null=True)
    
    def __unicode__(self):
        return "Issue" + self.pk
        
class IssueForm(ModelForm):
    class Meta:
        model = Issue
        fields = ('title', 'priority', 'status', 'owner', 'milestone', 'tags', 'followers', 'also_see',)
    

class HistoryItem(models.Model):
    '''Base model for comments and file uploads, and a model in itself for things like issue status changes, priority changes, and other sorts of changes'''
    issue = models.ForeignKey(Issue)
    author = models.ForeignKey(Vaquerita, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    history_choices = (
        ('comment','comment'),
        ('upload', 'file upload'),
        ('other', 'other change'),
    )
    change_type = models.CharField(max_length=8,choices=history_choices)
    change_description = models.CharField(max_length=200, blank=True, null=True)
    
    def __unicode__(self):
        return 'history item ' + self.pk + ': ' + change_description
        
class FileUpload(HistoryItem):
    '''Subclass of history item for an uploaded file for an issue. Must have one and only one associated issue'''
    file = models.FileField(upload_to='upload_directory', blank=True, null=True)
    name = models.CharField(max_length=100)
    
class Comment(HistoryItem):
    '''Subclass of history item for comments on an issue'''
    change_type = 'comment'
    content = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return 'Comment by ' + self.author.name
    
def upload_directory(instance, filename):
    '''Helper function to create upload directory paths for FileUpload model'''
    dir = 'issuefiles/'
    dir = dir + 'issue' + str(instance.issue.pk) + '/'