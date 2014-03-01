from django.conf import settings
from celery import task
import github


@task
def report_issue(summary, details):
    print 'creating an issue "{}"/"{}"'.format(summary, details)
    gh = github.Github(settings.GITHUB_API_KEY)
    repo = gh.get_repo("Nurdok/nextfeed")
    repo.create_issue(summary, details)
