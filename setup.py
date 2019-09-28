import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='reprPIP',  
     version='1.0',
     scripts=[],
     author="zmbbsmn",
     author_email="zimobabashimanong@gmail.com",
     description="reproducible PIP",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/zmbbsmn/reprPIP.git",
     packages=setuptools.find_packages(),
     install_requires=['typeguard'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )