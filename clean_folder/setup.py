from setuptools import setup, find_namespace_packages


setup(
    name='clean_folder',
    version='1',
    description='Garbage collector',
    url='https://github.com/AnnaZahinailo/GOIT-HW-Python-7.git',
    author='Anna',
    author_email='',
    license='MIT',
    packages=['clean_folder'],
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)