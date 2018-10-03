'''
    File name: SpaceSwitching.py
    Author: Wayne Moodie
    Date created: 10/2/2018
    Date last modified: 10/2/2018
    Python Version: 2.7
'''

import pymel.core as pm
from functools import wraps
try:
    from PyQt5 import QtWidgets, QtCore, QtGui
except:
    pass
from MatrixSpaceSwitching.Qt import QtWidgets, QtCore, QtGui



def undo_func(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        pm.undoInfo(openChunk=True, chunkName=func.__name__)
        try:
            result = func(*args, **kwargs)
            pm.undoInfo(closeChunk=True)
            return result
        except:
            pm.undoInfo(closeChunk=True)
            if pm.undoInfo(query=True, undoName=True) == func.__name__:
                pm.undo()
            raise  # this doesn't raise the exception
    return func_wrapper

def space_switch(drivers = None, driven = None, orient = None,
                 point =  None,  scale =  None, maintain_offset = None):

    '''

    :param drivers:
    :param driven:
    :param orient:
    :param point:
    :param scale:
    :param maintain_offset:
    :return:
    '''

    if drivers == None:
        raise ValueError('Please Provide Driver Spaces')
    else:
        driver_list = drivers

    if driven == None:
        raise ValueError('Please provide Driven Object')
    else:
        driven_onject = drivers

