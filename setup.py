# -*- coding:utf-8 -*-

#python setup.py sdist -> Source distribution (mit auf CD)
#python setup.py bdist -> Binary distribution (zum gucken)
#python setup.py bdist_msi -> Windows Installer (mit auf CD)

from distutils.core import setup
pymods=['PMF.__init__','PMF.Interface','PMF.PlantBuildingSet','PMF.PlantModel',
        'PMF.ProcessLibrary','PMF.CropDatabase']
#scripts=['Case_Study_I.py','Case_Study_II.py','Case_Study_III.py',
#         'cmf_fp_interface.py','cmf_setup.py', 
#         'giessen.rain','giessen.rHmean','giessen.Sunshine','giessen.Tmax',
#         'giessen.Tmin','giessen.txt','giessen.Windspeed'] 
#scripts=scripts, 
setup(name='PMF', py_modules=pymods, 
      author='Sebastian Multsch',
      author_email='sebastian.multsch@agrar.uni-giessen.de',version='0.1')
