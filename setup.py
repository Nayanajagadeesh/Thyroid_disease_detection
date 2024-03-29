# using setup.py our project  can be use as a package and it can also be used as library by other projects
# for any pyhon project thisis the first file

from setuptools import find_packages,setup

from typing import List

REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements()->List[str]:
    
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)    
        # because it is not a library that's why we newed tyo remove it
    return requirement_list



setup(
    name="Thyroid",
    version="0.0.1",
    author="Nayana",
    author_email="jnayana323@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
