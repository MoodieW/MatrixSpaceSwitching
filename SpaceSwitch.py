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
#from MatrixSpaceSwitching.Qt import QtWidgets, QtCore, QtGui



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


def space_switch(drivers = None, driven = None, parent_node = None, buffer = None,
                 orient = None, point =  None, maintain_offset = None):

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
        driven_object = driven
        #if pm.addAttr(driven_object[0]+'.Space_Switch',e= 1, enumName= "pCube6:pCube5:pCube7:5:A:B:C" ):
        pm.addAttr(driven_object[0] ,ln='Space_Switch', at='enum', en=enum_list, k=True)
        choice = pm.createNode('choice', n=driven_object[0] + '_Switch')
        driven_object[0].Space_Switch >> choice.selector
        if maintain_offset:
            choice_offset = pm.createNode('choice', n=driven_object[0] + 'offset_Switch')
            driven_object[0].Space_Switch >> choice_offset.selector
            
    for iter, driver in enumerate(drivers):
        
        driver.worldMatrix[0] >> choice.input[iter]
        
    decomp = pm.createNode('decomposeMatrix', n=driven_object[0] + '_decompMatrix')
    mult = pm.createNode('multMatrix', n=driven_object[0] + '_multMatrix')

    choice.output                     >> mult.matrixIn[0]
    parent_node[0].worldInverseMatrix >> mult.matrixIn[1]
    mult.matrixSum                    >> decomp.inputMatrix    
    
    if maintain_offset:
        for iter, driver in enumerate(drivers):
            pm.addAttr(parent_node, ln=driver+'_offset', at='fltMatrix')
            temp_matrix = driven_object[0].getMatrix(worldSpace =True) * driver.getMatrix(worldSpace =True).inverse()
            offset_matrix = tuple(v for i in temp_matrix for v in i)
            pm.setAttr(parent_node[0]+'.'+driver+'_offset', offset_matrix)
            pm.connectAttr(parent_node[0]+'.'+driver+'_offset',  choice_offset.input[iter])  
              
        choice_offset.output >> mult.matrixIn[2]
    

    

if __name__ == "__main__":
    #drivers_list = pm.ls(sl=True)
    #driven_list = pm.ls(sl=True)
    #parent_tfm  = pm.ls(sl=True)

    space_switch(drivers = drivers_list, driven = driven_list, 
                 parent_node = parent_tfm, maintain_offset = True)
