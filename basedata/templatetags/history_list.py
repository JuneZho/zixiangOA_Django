from django import template
from basedata import models as mymodel

register = template.Library()


class HisNode(template.Node):
    def __init__(self, limit, varname, user):
        self.limit, self.varname, self.user = limit, varname, user

    def __repr__(self):
        return "<GetHisList Node>"

    def render(self, context):
        if self.user is None:
            entries = mymodel.TodoList.objects.all()
        else:
            user_id = self.user
            if not user_id.isdigit():
                user_id = context[self.user].pk
            entries = mymodel.History.objects.filter(user__pk=user_id)
        context[self.varname] = entries.select_related('project', 'user')[:int(self.limit)]
        return ''


@register.tag
def get_his_list(parser, token):

    tokens = token.contents.split()
    if len(tokens) < 4:
        raise template.TemplateSyntaxError(
            "'get_his_list' statements require two arguments")
    if not tokens[1].isdigit():
        raise template.TemplateSyntaxError(
            "First argument to 'get_his_list' must be an integer")
    if tokens[2] != 'as':
        raise template.TemplateSyntaxError(
            "Second argument to 'get_todo_list' must be 'as'")
    if len(tokens) > 4:
        if tokens[4] != 'for_user':
            raise template.TemplateSyntaxError(
                "Fourth argument to 'get_admin_log' must be 'for_user'")
    return HisNode(limit=tokens[1], varname=tokens[3], user=(tokens[5] if len(tokens) > 5 else None))
