from setuptools import setup,find_packages
from typing import List


def get_requirements(file_path:str)->List[str]:
    ## this function will return a list of requirements
    requirements=[]
    with open(file_path,'r') as file_obj:
        requirements=file_obj.readlines()
    requirements=[req.replace('\n','') for req in requirements]   
    
    
## without this 
#     requirements = [
#     "numpy==1.24.2\n",
#     "pandas==2.0.1\n",
#     "scikit-learn==1.2.2\n",
#     "matplotlib\n",
#     "seaborn\n"
# ] its looks like this
    

setup(
    name='Security Model',
    version='0.0.1',
    author='Sarvesh Chhabra',
    author_email='sarveshpoker@gmail.com',
    packages=find_packages(),
    install_requirements=get_requirements('requirements.txt')
)

# -e . will automatically triggers setup.py file