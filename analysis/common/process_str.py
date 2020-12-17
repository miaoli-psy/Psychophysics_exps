import ast


# convert list-like str to list
def str_to_list(string:str) -> list:
    return ast.literal_eval(string)