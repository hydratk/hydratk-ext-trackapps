# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open("README.rst", "r") as f:
    readme = f.readlines()
    
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",   
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",    
    "Programming Language :: Python :: Implementation :: PyPy",    
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]

packages = [
            'hydratk.extensions.trackapps' 
           ]

requires = [
            'hydratk',
            'hydratk-lib-network'
           ]  
           
data_files = [
              ('/etc/hydratk/conf.d', ['etc/hydratk/conf.d/hydratk-ext-trackapps.conf']) 
             ]  

entry_points = {
                'console_scripts': [
                    'trackapps = hydratk.extensions.trackapps.bootstrapper:run_app'                               
                ]
               }                    
                
setup(name='hydratk-ext-trackapps',
      version='0.1.0',
      description='Interface to bugtracking and test management applications',
      long_description=readme,
      author='Petr Rašek',
      author_email='bowman@hydratk.org',
      url='http://extensions.hydratk.org/trackapps',
      license='BSD',
      packages=find_packages('src'),
      install_requires=requires,
      package_dir={'' : 'src'},
      classifiers=classifiers,
      data_files=data_files,
      entry_points=entry_points 
     )