def format_string(string):
    string = "".join([x if x.isalpha() else "" if x.isalnum() else " " for x in string]).lower().replace("\t", " ")\
        .replace("\n", " ")
    while "  " in string:
        string = string.replace("  ", " ")
    return string