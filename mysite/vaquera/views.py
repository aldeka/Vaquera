from django.shortcuts import render_to_response
from vaquera.models import Milestone, Issue, IssueForm, Vaquerita, Project
import datetime

project = Project.objects.get(pk=1)

def issue_index(request):
    issue_list = Issue.objects.all()
    return render_to_response('issues/issue-index.html', {'project' : project, 'issue_list' : issue_list})

def issue(request, issue_id):
    i = get_object_or_404(Issue, pk=issue_id)
    form = IssueForm(instance=i)
    return render_to_response('issues/issue.html', {'project' : project, 'form' : form, 'issue' : i})

def people_index(request):
    people_list = Vaquerita.objects.all()
    return render_to_response('issues/people-index.html', {'project' : project, 'people_list' : people_list})

def milestone_index(request):
    project = Project.objects.get(pk=1)
    Milestone.safe_for_democracy(project)
    overdue_milestone_list = Milestone.objects.filter(is_past=True).filter(is_complete=False)
    current_milestone =  Milestone.objects.get(end_date__month=datetime.date.today().month)
    future_milestone_list = Milestone.objects.filter(end_date__gt=Milestone.end_of_month(datetime.date.today()))
    unaffiliated_issues = Issue.objects.filter(milestone__isnull=True)
    return render_to_response('milestones/milestone-dashboard.html', {'project' : project, 'overdue_milestone_list' : overdue_milestone_list, 'current_milestone' : current_milestone, 'future_milestone_list' : future_milestone_list, 'unaffiliated_issues' : unaffiliated_issues })

def current_milestone(request):
    project = Project.objects.get(pk=1)
    Milestone.safe_for_democracy(project)
    milestone = Milestone.objects.get(end_date__month=datetime.date.today().month)
    return render_to_response('milestones/milestone.html', {'project' : project, 'milestone' : milestone})

def future_milestones(request):
    pass

def past_milestones(request):
    pass

def milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    return render_to_response('project' : project, 'milestones/milestone.html', {'milestone' : milestone})
    
def issues_authored(request, username):
    vaquerita = Vaquerita.objects.get(username=username)
    issue_list = Issue.objects.filter(author=vaquerita)
    return render_to_response('project' : project, 'vaquerita' : vaquerita, 'issue_list' : issue_list})
    
def issues_assigned(request, username):
    vaquerita = Vaquerita.objects.get(username=username)
    issue_list = Issue.objects.filter(assignee=vaquerita)
    return render_to_response('project' : project, 'vaquerita' : vaquerita, 'issue_list' : issue_list})
    
def issues_followed(request, username):
    vaquerita = Vaquerita.objects.get(username=username)
    issue_list = Issue.objects.filter(followers__contains=vaquerita)
    return render_to_response('project' : project, 'vaquerita' : vaquerita, 'issue_list' : issue_list})