import sys

sys.path.append('src/')

from typeMismatch import * 
from uninitVar import * 
from unusedVar import * 
from divByZero import * 
from arrayOutofBounds import * 

from preProcess import *

# main
if __name__=='__main__':
    # take the name of input file from stdin
    filename_init = input("Enter the name/path of the file: ")

    # preprocess to remove all comments and includes
    print("Removing comments and includes...")
    filename = pre_process(filename_init)

    # 1. check for type mismatch
    print("Checking for type mismatch errors...")
    check_type_mismatches(filename)

    # 2. check for uninitialized variables
    print("Checking for uninitialized variable errors...")
    check_uninitialized_variables(filename)

    # 3. check for unused variables
    print("Checking for unused variable errors...")
    check_unused_variables(filename)

    # 4. check for division by zero
    print("Checking for division by zero errors...")
    check_division_by_zero(filename)

    # 5. check for array out of bounds
    print("Checking for array out of bounds errors...")
    check_array_out_of_bounds(filename)
    
    if(len(sys.argv) > 1) and (sys.argv[1] == '--clean'):
        delete_preprocessed_dir(filename_init)
    
