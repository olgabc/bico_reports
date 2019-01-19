import re
regex = r"<tr (.+?) \[/P\]+?"
line = "President <tr Barack Obama [/P] met Microsoft founder <tr Bill Gates [/P], yesterday."
person = re.findall(regex, line)
print(person)