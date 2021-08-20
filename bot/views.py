from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from jira import JIRA
from simple_colors import *
from .models import *
from .tbot import TBot



bot = TBot()

options = {'server': 'https://alphabots.atlassian.net'}

jira = JIRA(options, basic_auth=("bohdan.konon@gmail.com", "tPvWj5MaMvUE8dJtEXDFC9EF"))


@csrf_exempt
def get_hook(request):
    if request.META['CONTENT_TYPE'] == 'application/json':
        json_data = request.body.decode('utf-8')
        update = bot.update(json_data)
        bot.bot.process_new_updates([update])
        return HttpResponse(status=200)
    else:
        raise PermissionDenied


@bot.bot.message_handler(commands=['start'])
def send_notification(message):
    size = 100
    initial = 0
    while True:
        try:
            start = initial * size
            issues = jira.search_issues('project = INJT', start, size)
            if len(issues) == 0:
                break
            initial += 1
            for iss in issues:
                issue = jira.issue(str(iss), expand='changelog')
                changelog = issue.changelog

                for history in changelog.histories:
                    try:
                        if not IssueId.objects.filter(id=int(history.id)):
                            for item in history.items:
                                if item.field:
                                    IssueId.objects.create(id=int(history.id))
                                    bot.bot.send_message(chat_id=message.chat.id,
                                                         text=f'' + str(iss.fields.summary) + '    ' + str(iss) +
                                                              '\nAssignee: ' + str(iss.fields.assignee.displayName) +
                                                              '\nReporter: ' + str(iss.fields.reporter.displayName) +
                                                              '\nEpic Link: ' +
                                                              'https://alphabots.atlassian.net/browse/' + str(iss) +
                                                              '\n' + str(history.author.displayName) +
                                                              ' updated the ' + item.field +
                                                              '\n' + str(item.fromString) +
                                                              '  →  ' + str(item.toString))
                    except Exception as e:
                        print(e)

        except Exception as e:
            print(e)


