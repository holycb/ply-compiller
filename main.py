import sys
import ply.lex as lex
from initialdata import *
from rofl_parser import *
import pandas
import io
import utils as utils
import ply.yacc as yacc
from semantic_analysis import *

def findErrors(data):
    errordata = []

    # redundant repeating
    for i in range(len(data) - 1):
        if data[i][0] == "CONST_INTEGER" and (abs(int(data[i][1])) > (2 ** 32) - 1):
            errordata.append("Integer type overflow at line " +
                             str(data[i][2]) + " pos " + str(data[i][3]))
            # addError("Integer type overflow", data[i])
    return errordata

if __name__ == "__main__":
    filename = 'program.rofl'

    if (len(sys.argv) > 1):
        filename = sys.argv[1]

    lexer = lex.lex()

    with io.open(filename, "r", encoding="utf8") as f:
        text = f.read()
        ## print tokens
        # data = []
        # for token in lexer:
        #     data.append([token.type, token.value, token.lineno])
        # errors = findErrors(data)
        # for error in errors:
        #     print(error)
        # print(pandas.DataFrame([row for row in data], columns=["token_type", "token_value", "line_no"]))

        parser = yacc.yacc(debug=0)
        result = parser.parse(text)
        show_tree_with_errors = True
        if not result is None and \
                (len(result.get('ERROR', nest=True)) == 0 and show_tree_with_errors):

            print(result)

            # please add errors to that list of tuples
            # type: [('message', lineno), ...]
            errors = check_var_definition(
                result) + check_expression_results(result) + check_funcs_have_returns(result)
            errors = check_var_definition(result) + check_expression_results(result) + check_funcs_have_returns(result) \
                     + check_arguments_of_func_calls(result)
            for error in sorted(errors, key=lambda tup: tup[1]):
                print(error[0])

            check_unexpected_keywords(result)
        else:
            print("There are some syntax errors detected in source code.")
