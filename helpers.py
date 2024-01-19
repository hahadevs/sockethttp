def template(template_name:str):
    with open('templates/'+template_name,"r") as template_file:
        html = template_file.read()
    return html