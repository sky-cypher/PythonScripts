#!/usr/bin/env python3

file_name = 'tmp.py'
classes = list()

def create_class(class_name: str):
    name = class_name.split('(')[0]
    global classes
    classes.append(name)
    print("creating class",class_name)
    def_class = f"""
class {class_name}:
    def __str__(self):
        return 'Object of {name}'
"""
    with open(file_name, 'a') as f:
        f.write(def_class)

def create_output():
    output = str()
    for _ in range(len(classes)):
        output += f"""
sample = {classes.pop(0)}()
print(sample)
"""
    with open(file_name, 'a') as f:
        f.write(output)

def create_derived_classes(base_class: str,derived_classes: list ):
    for derived_class in derived_classes:
        create_class(f"{derived_class}({base_class})")

def prep_file():
    with open(file_name, 'w') as f:
        f.write('#!/usr/bin/env python3\n')

def main():
    global file_name
    file_name = "program.py"
    prep_file()
    create_class('student')
    student = ['subject', 'forces', 'exercises']
    create_derived_classes('student',student)
    create_output()

if __name__ == '__main__':
    main()
