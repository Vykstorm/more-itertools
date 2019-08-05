

from argparse import ArgumentParser, FileType
from itertools import chain
import moreitertools
from moreitertools import first
from types import FunctionType
from functools import lru_cache, partial
from operator import attrgetter, contains
from inspect import getsource, signature, Signature
from re import sub, match, finditer, findall, DOTALL, MULTILINE


@lru_cache(maxsize=32)
def get_function_body(func):
    '''
    Takes one an arbitrary function and return
    the source code of its body (removing the docstring and the header)
    '''
    source = getsource(func)
    # Remove docstring
    source = sub(r"'''.*'''\s*\n\s*", '', source, flags=DOTALL | MULTILINE)

    # Extract only the body
    body = match(r"^[^\n]+\n(.+)", source, flags=DOTALL | MULTILINE).group(1)
    return body


@lru_cache(maxsize=64)
def get_function_header(func, include_annotations=False):
    '''
    Given an arbitary function, return its header definition as a string
    If include_annotations is True, leave the parameter and return annotations.
    '''
    sig = signature(func)
    if not include_annotations:
        sig = sig.replace(
            parameters=[param.replace(annotation=Signature.empty) for param in sig.parameters.values()],
            return_annotation=Signature.empty
        )
    return f"def {func.__name__}{sig}:"


@lru_cache(maxsize=32)
def get_function_dependencies(func):
    '''
    Returns a set of methods defined in moreitertools called from inside the body of
    the given function
    '''
    all_funcnames = frozenset(map(attrgetter('__name__'), get_all_functions()))
    tokens = map(lambda r: r.group(1), finditer(r"(\w+)[\w\.]*[ ]*\(", get_function_body(func)))
    names = (frozenset(tokens) & all_funcnames) - {func.__name__}
    return tuple(filter(lambda f: f.__name__ in names, get_all_functions()))


@lru_cache(maxsize=1)
def get_all_functions():
    '''
    Returns a tuple with all functions defined in the moreitertools library
    '''
    result = []
    for name in dir(moreitertools):
        value = getattr(moreitertools, name)
        if not isinstance(value, FunctionType):
            continue
        if name.startswith('_') or value.__module__ != moreitertools.__name__:
            continue
        result.append(value)
    return tuple(result)



def build_recipes(funcs, include_docstrings=False, include_annotations=False, include_imports=False):
    '''
    Returns all the recipes for the given functions as a string separated by line breaks.
    If include_docstrings is True, docstrings will be printed in the recipes.
    If include_annotations is True, parameters and return value annotations will be shown on the signatures.
    '''

    # Functions to print (include also dependencies)
    dependencies = map(get_function_dependencies, funcs)
    funcs = frozenset(chain(funcs, chain.from_iterable(dependencies)))

    def build_recipe(func):
        # Get the function header
        header = get_function_header(func, include_annotations)

        # Get the function body
        body = sub(r"(\w+)\.unchecked[ ]*\(", r'\1(', get_function_body(func))

        if include_docstrings:
            # Append docstring to the function body (at the beginning)
            docs = func.__doc__
            padding = match('(^\s*)', docs).group(1).replace('\n', '')
            body = f"{padding}'''{docs}'''\n" + body

        # Build the recipe
        return header + '\n' + body

    # Get the recipe for each one and concatenate them by line breaks
    return ('\n' * 2).join(map(build_recipe, funcs))





description =\
'''
This script allows you to generate the source code of the functions
defined in this library (This is useful if you only need to use
an specific recipe and dont want to install moreitertools module)
'''

help = {
    'docs': 'Include docstrings on the generated recipes',
    'annotations': 'If specified, recipes will have annotations in its parameters & return values',
    'no-imports': 'Import statements for dependencies will not be generated',
    'recipes': 'Must be a list of the recipes you want to generate'
}


if __name__ == '__main__':
    parser = ArgumentParser(description=description)

    # Optional arguments
    parser.add_argument('--docs', '--docstrings', action='store_true', help=help['docs'])
    parser.add_argument('--annotations', action='store_true', help=help['annotations'])
    parser.add_argument('--no-imports', action='store_false', help=help['no-imports'])
    parser.add_argument('-o', '--output', nargs=1, type=FileType('w'))

    # Positional arguments
    parser.add_argument('recipes', nargs='*', type=str, help=help['recipes'])

    # Parse arguments
    parsed_args = parser.parse_args()
    include_docstrings, include_annotations, include_imports = parsed_args.docs, parsed_args.annotations, not parsed_args.no_imports

    if len(parsed_args.recipes) > 0:
        recipe_names = frozenset(parsed_args.recipes)

        # Check that all the recipe names are valid
        all_funcnames = frozenset(map(attrgetter('__name__'), get_all_functions()))
        if not recipe_names.issubset(all_funcnames):
            parser.error('Unkown recipes: ' + ', '.join(recipe_names - all_funcnames))

        funcs = tuple(filter(lambda f: f.__name__ in recipe_names, get_all_functions()))
    else:
        funcs = get_all_functions()

    # Generate the recipes code
    code = build_recipes(funcs, include_docstrings, include_annotations, include_imports)
    print()
    print(code)
