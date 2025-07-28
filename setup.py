'''
The setup.py file is an essential part of packaging and
distributing Python projects. It is used by setuptools
(or distutils in older Python versions) to define the configuration
of your project, such as its metadata, dependencies, and more
'''
from setuptools import setup,find_packages
from typing import List


def get_requirements(file_path:str)->List[str]:
    ## this function will return a list of requirements
    try:
        requirements_list:List[str]=[]
        with open(file_path,'r') as file_obj:
            #read line from the file
            lines=file_obj.readlines()
            ## process each line
            for line in lines:
                requirement=line.strip()
            ## ignore empty lines and -e . and '\n'
                if requirement and requirement!= '-e .':
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    
    return requirements_list
    
    
## without this 
#     requirements = []
#     "numpy==1.24.2\n",
#     "pandas==2.0.1\n",
#     "scikit-learn==1.2.2\n",
#     "matplotlib\n",
#     "seaborn\n"]
#  its looks like this
    

setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Sarvesh Chhabra',
    author_email='sarveshpoker@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)

# -e . will automatically triggers setup.py file

