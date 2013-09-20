from django import template
from django.core.urlresolvers import reverse


def do_if_active_url(parser, token):
    try:
        tag_name, request, urls = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, ("%r tag requires exactly two arguments, received" %
                                             token.contents.split()[0], len(token.contents.split()[0]))
    if not (urls[0] == urls[-1] and urls[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name

    nodelist_true = parser.parse(('else', 'endif_active_url'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('endif_active_url'))
        parser.delete_first_token()
    else:
        nodelist_false = template.NodeList()

    return IfActiveUrlNode(request, urls, nodelist_true, nodelist_false)


class IfActiveUrlNode(template.Node):
    def __init__(self, request, urls, nodelist_true, nodelist_false):
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.request = template.Variable(request)
        self.urls = template.Variable(urls)

    def render(self, context):
        request = self.request.resolve(context)
        urls = self.urls.resolve(context)
        if request.path in (reverse(url) for url in urls.split()):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

register = template.Library()
register.tag('if_active_url', do_if_active_url)
