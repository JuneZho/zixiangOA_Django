from django import template
from basedata import models as mymodel

register = template.Library()


class ProjectNode(template.Node):
    def __init__(self, limit, varname, user):
        self.limit, self.varname, self.user = limit, varname, user

    def __repr__(self):
        return "<GetProjectList Node>"

    def render(self, context):
        entries = mymodel.Project.objects.all()
        context[self.varname] = entries.select_related('project')[:int(self.limit)]
        return ''


@register.tag
def get_project_list(parser, token):

    tokens = token.contents.split()
    if len(tokens) < 4:
        raise template.TemplateSyntaxError(
            "'get_project_list' statements require two arguments")
    if not tokens[1].isdigit():
        raise template.TemplateSyntaxError(
            "First argument to 'get_todo_list' must be an integer")
    if tokens[2] != 'as':
        raise template.TemplateSyntaxError(
            "Second argument to 'get_todo_list' must be 'as'")
    if len(tokens) > 4:
        if tokens[4] != 'for_user':
            raise template.TemplateSyntaxError(
                "Fourth argument to 'get_admin_log' must be 'for_user'")
    return ProjectNode(limit=tokens[1], varname=tokens[3], user=(tokens[5] if len(tokens) > 5 else None))
