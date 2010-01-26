# -*- coding:utf-8 -*-

from distutils.core import setup
pymods=['PMF.__init__','PMF.Interface','PMF.PlantBuildingSet','PMF.PlantModel',
        'PMF.ProcessLibrary']
scripts=['Case_Study_I.py','Case_Study_II.py','Case_Study_III.py']

setup(name='PMF', py_modules=pymods, scripts=scripts,
      author='Sebastian Multsch',author_email='',version='0.1')
