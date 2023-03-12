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
    try:
        check_type_mismatches(filename)
    except Exception as e:
        print(f"Error while checking for type mismatch errors: ", e)
        exit(0)

    # 2. check for uninitialized variables
    print("Checking for uninitialized variable errors...")
    try: 
        check_uninitialized_variables(filename)
    except Exception as e:
        print(f"Error while checking for uninitialized variable errors: ", e)
        exit(0)

    # 3. check for unused variables
    print("Checking for unused variable errors...")
    try:
        check_unused_variables(filename)
    except Exception as e:
        print(f"Error while checking for unused variable errors: ", e)
        exit(0)

    # 4. check for division by zero
    print("Checking for division by zero errors...")
    try:
        check_division_by_zero(filename)
    except Exception as e:
        print(f"Error while checking for division by zero errors: ", e)
        exit(0)

    # 5. check for array out of bounds
    print("Checking for array out of bounds errors...")
    try:
        check_array_out_of_bounds(filename)
    except Exception as e:
        print(f"Error while checking for array out of bounds errors: ", e)
        exit(0)
    
    if(len(sys.argv) > 1) and (sys.argv[1] == '--clean'):
        print("Cleaning up...")
        try:
            delete_preprocessed_dir(filename_init)
        except Exception as e:
            print(f"Error while cleaning up: ", e)
            exit(0)
    
