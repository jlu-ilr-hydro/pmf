# -*- coding:utf-8 -*-

from distutils.core import setup
pymods=['PMF.__init__','PMF.Interface','PMF.PlantBuildingSet','PMF.PlantModel',
        'PMF.ProcessLibrary']
scripts=['CaseStudyI_with_CMF.py']

setup(name='PMF', py_modules=pymods, scripts=scripts,
      author='Sebastian Multsch',author_email='',version='0.1')
