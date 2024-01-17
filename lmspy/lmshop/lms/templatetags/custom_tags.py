from django import template
register = template.Library()


class VariableNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return ""


@register.tag(name='set')
def set_variable(_, token):
    parts = token.split_contents()
    if len(parts) != 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")
    return VariableNode(parts[1], parts[3])
