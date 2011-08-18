from django.shortcuts import render_to_response
from vaquera.models import Milestone, Issue, IssueForm, Vaquerita
import vaquera.settings
import datetime

def issue_index(request):
    issue_list = Issue.objects.all()
    return render_to_response('issues/issue-index.html', {'project_name' : project_name, 'issue_list' : issue_list})
    
def advanced_search(request):
    issue_list = Issue.objects.all()
    return render_to_response('issues/advanced-search.html', {'project_name' : project_name, 'issue_list' : issue_list})

def issue(request, issue_id):
    i = get_object_or_404(Issue, pk=issue_id)
    form = IssueForm(instance=i)
    return render_to_response('issues/issue.html', {'project_name' : project_name, 'form' : form, 'issue' : i})

def people_index(request):
    people_list = Vaquerita.objects.all()
    return render_to_response('issues/people-index.html', {'project_name' : project_name, 'people_list' : people_list})

def milestone_index(request):
    project = Project.objects.get(pk=1)
    Milestone.safe_for_democracy()
    overdue_milestone_list = Milestone.objects.filter(is_past=True).filter(is_complete=False)
    current_milestone =  Milestone.objects.get(end_date__month=datetime.date.today().month)
    future_milestone_list = Milestone.objects.filter(end_date__gt=Milestone.end_of_month(datetime.date.today()))
    unaffiliated_issues = Issue.objects.filter(milestone__isnull=True)
    return render_to_response('milestones/milestone-dashboard.html', {'project_name' : project_name, 'overdue_milestone_list' : overdue_milestone_list, 'current_milestone' : current_milestone, 'future_milestone_list' : future_milestone_list, 'unaffiliated_issues' : unaffiliated_issues })

def current_milestone(request):
    project = Project.objects.get(pk=1)
    Milestone.safe_for_democracy()
    milestone = Milestone.objects.get(end_date__month=datetime.date.today().month)
    return render_to_response('milestones/milestone.html', {'project_name' : project_name, 'milestone' : milestone})

def milestone(request, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    return render_to_response('project_name' : project_name, 'milestones/milestone.html', {'milestone' : milestone})
    
def issues_authored(request, username):
    vaquerita = Vaquerita.objects.get(username=username)
    issue_list = Issue.objects.filter(author=vaquerita)
    return render_to_response('project_name' : project_name, 'vaquerita' : vaquerita, 'issue_list' : issue_list})
    
def issues_assigned(request, username):
    vaquerita = Vaquerita.objects.get(username=username)
    issue_list = Issue.objects.filter(owner=vaquerita)
    return render_to_response('project_name' : project_name, 'vaquerita' : vaquerita, 'issue_list' : issue_list})
    
def issues_followed(request, username):
    vaquerita = Vaquerita.objects.get(username=username)
    issue_list = Issue.objects.filter(followers__contains=vaquerita)
    return render_to_response('project_name' : project_name, 'vaquerita' : vaquerita, 'issue_list' : issue_list})