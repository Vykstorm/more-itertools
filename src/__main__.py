

from code import InteractiveConsole, compile_command
import rlcompleter
import readline

import builtins, sys, functools, itertools, moreitertools, operator, typing
from itertools import *
from functools import *
from moreitertools import *
from operator import *
from typing import *


# Description shown at start-up
DESCRIPTION =\
'''This is an interactive prompt designed to test iterators.
All the functions defined by moreitertools, as well as functools, itertools, operator are already imported and ready to use.
You can visualize and debug part of the contents of an iterator by typing it in the console.
'''



class IterShell(InteractiveConsole):
    def __init__(self):
        super().__init__(globals(), '<console>')

    def runsource(self, source, *args, **kwargs):
        try:
            code = compile_command(source, *args, **kwargs)
        except (SyntaxError, OverflowError):
            self.showsyntaxerror()
            return False

        if code is None:
            return True

        try:
            out = eval(source)
            # If user typed a module, do help(module)
            try:
                module = first(filter(partial(is_, out), (builtins, itertools, functools, operator, moreitertools)))
                return help(module)
            except ValueError:
                pass

            # If user type a iterator, parse it with debugiter
            if isinstance(out, (Iterator, range)) and not isinstance(out, moreitertools._DebugIterator):
                out = debugiter(out)

            # Print the result of the evaluation
            print(repr(out))

            # Define the variable '_' with the given result
            globals()['_'] = out

        except SyntaxError:
            self.runcode(code)

        except SystemExit as e:
            # Re-raise system exit exceptions
            raise e
        except:
            # Show traceback of the last exception
            self.showtraceback()


        return False


if __name__ == '__main__':
    # Print python version & description
    print(sys.version)
    print(DESCRIPTION)

    # Enable tab autocomplete
    readline.parse_and_bind("tab: complete")
    # Activate console interactive mode
    IterShell().interact(banner='', exitmsg='')
