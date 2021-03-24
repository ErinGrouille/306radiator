
import sys

def error_message(msg='unknown error', code_error=84):
    sys.stderr.write(msg + '\n')
    sys.exit(code_error)