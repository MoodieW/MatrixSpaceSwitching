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


def create_enum_list(drivers):

    '''
    creates a string from a list that will be formatted correctly for the addAttr enumName flag.
    :param drivers: pass a list of drivers to be converted into a list of.
    :return: returns string of enumeration.
    '''

    enum_list = ''
    for i in drivers:
        enum_list += str(i.name())+":"

    return enum_list[:-1]


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

    #Create choice node and wires it up
    if drivers == None:
        raise ValueError('Please Provide Driver Spaces')
    else:
        driver_list = drivers
        enum_list = create_enum_list(driver_list)

    if driven == None:
        raise ValueError('Please provide Driven Object')
    else:
        driven_object = drivers

        pm.addAttr(ln='Space_Switch', at='enum', en=enum_list, k=True)
        choice = pm.createNode('choice', n=driven_object + '_Switch')
        driven_object.Space_Switch >> choice.selector


    for iter, driver in enumerate(drivers):
        driver.worldMatrix[0] >> choice.input[iter]

    driven_parent=  driven.getParent()

    decomp = pm.createNode('decomposeMatrix', n=driven + '_decompMatrix')
    mult = pm.createNode('multMatrix', n=driven + '_multMatrix')
    wt = pm.createNode('wtAddMatrix', n=driven + '_wtMatrix')
