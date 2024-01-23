import jinja2
environment = jinja2.Environment()
template = environment.from_string("{% if name %}{{name}}{% endif %}")
text = template.render()

print(text)