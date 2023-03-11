import re, os

# Define regular expressions for comments and include statements
comment_re = re.compile(r'(/\*.*?\*/|//.*?$)', re.DOTALL | re.MULTILINE)
include_re = re.compile(r'^#include\s.*?$\n', re.MULTILINE)

def pre_process(filename):
    # Read in C program from file
    with open(filename, 'r') as f:
        program = f.read()

    # Remove comments and include statements from program
    program = comment_re.sub('', program)
    program = include_re.sub('', program)

    # access the directory of the input file
    directory = filename[:filename.rfind('/')+1]
    filename = filename[filename.rfind('/')+1:]
    # write the preprocessed program to a file named /preprocessed/filename
    # create a new directory named /preprocessed if it doesn't exist
    os.makedirs(directory+'preprocessed', exist_ok=True)
    new_filename = directory+'preprocessed/'+filename
    with open(new_filename, 'w') as f:
        f.write(program)
    
    return new_filename

def delete_preprocessed_dir(filename):
    directory = filename[:filename.rfind('/')+1]
    os.chdir(directory)
    os.system('rm -rf preprocessed')
