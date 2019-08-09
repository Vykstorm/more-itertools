

'''
Installation script for this library
'''

from setuptools import setup


if __name__ == '__main__':
    setup(
        name='more-itertools',
        version='1.0.2',
        description='An extension of the standard python module itertools',
        author='Vykstorm',
        author_email='victorruizgomezdev@gmail.com',
        keywords=['itertools', 'iteration', 'recipes'],
        url='https://github.com/Vykstorm/more-itertools',

        python_requires='>=3.5',
        install_requires=[],
        dependency_links=[],

        package_dir={'moreitertools': 'src'},
        packages=['moreitertools']
    )
