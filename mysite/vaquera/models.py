from django.db import models
from django.contrib.auth.models import User

class Vaquerita(User):
    '''Model for all logged-in users of the bugtracker -- uses Django's built-in user model'''
    is_maintainer = models.BooleanField(default=False)

class Issue(models.Model):
    '''Model for all bugs and feature requests that the tracker tracks'''
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Vaquerita', blank=True, null=True, on_delete=models.SET_NULL)
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
        ('unr', 'unread'),
        ('ch', 'chatting'),
        ('eg', 'needing example'),
        ('pro', 'in progress'),
        ('rev', 'needing review'),
        ('res', 'resolved'),
        ('def', 'deferred'),
        ('ro', 'reopened'),
    )
    # how far the bug is along towards being closed
    status = models.CharField(max_length=3, choices=status_choices,default='unr')
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    milestone = models.ForeignKey('Milestone', blank=True, null=True)
    # for keeping track of dependencies and other relationships between issues -- the exact relation is left to be hashed out in the comments
    also_see = models.ManyToManyField("self", blank=True, null=True)
    
    def __unicode__(self):
        return "Issue" + self.pk
    

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
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True,null=True)
    
    def completion_level(self):
        '''Calculates how complete a milestone is to having all its bugs closed (either resolved or deferred)'''
        total_issues = self.issue_set.count()
        
        # 0.0 makes it a float instead of an int
        closed_issues = self.issue_set.filter(status__exact='res').count() + self.issue_set.filter(status__exact='def').count() + 0.0
        
        # note to self: use floatformat in templates to make this truncate to one decimal place
        percent_complete = (closed_issues / total_issues) * 100
        return percent_complete
        
    def is_complete(self):
        '''Returns a boolean that is True if the milestone's completion level is 100 percent'''
        return self.completion_level == 100.0
            