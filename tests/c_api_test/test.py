import sys
import os
import ctypes
import collections

import numpy as np
from scipy import sparse

def LoadDll():
    """Load xgboost Library."""
    if os.name == 'nt':
        lib_path = '../../windows/x64/DLL/lib_lightgbm.dll'
    else:
        lib_path = '../../lib_lightgbm.so'
    lib = ctypes.cdll.LoadLibrary(lib_path)
    return lib

LIB = LoadDll()

dtype_float32 = 0
dtype_float64 = 1
dtype_int32 = 2
dtype_int64 = 3


def c_array(ctype, values):
    return (ctype * len(values))(*values)

def c_str(string):
    return ctypes.c_char_p(string.encode('ascii'))

def test_load_from_file(filename, reference):
    ref = None
    if reference != None:
        ref = ctypes.byref(reference)
    handle = ctypes.c_void_p()
    LIB.LGBM_CreateDatasetFromFile(c_str(filename), 
        c_str('max_bin=15'), 
        ref, ctypes.byref(handle) )
    num_data = ctypes.c_long()
    LIB.LGBM_DatasetGetNumData(handle, ctypes.byref(num_data) )
    num_feature = ctypes.c_long()
    LIB.LGBM_DatasetGetNumFeature(handle, ctypes.byref(num_feature) )
    print ('#data:%d #feature:%d' %(num_data.value, num_feature.value) ) 
    return handle

def test_save_to_binary(handle, filename):
    LIB.LGBM_DatasetSaveBinary(handle, c_str(filename))

def test_load_from_binary(filename):
    handle = ctypes.c_void_p()
    LIB.LGBM_CreateDatasetFromBinaryFile(c_str(filename), ctypes.byref(handle) )
    num_data = ctypes.c_long()
    LIB.LGBM_DatasetGetNumData(handle, ctypes.byref(num_data) )
    num_feature = ctypes.c_long()
    LIB.LGBM_DatasetGetNumFeature(handle, ctypes.byref(num_feature) )
    print ('#data:%d #feature:%d' %(num_data.value, num_feature.value) ) 
    return handle

def test_load_from_csr(filename, reference):
    data = []
    label = []
    inp = open(filename, 'r')
    for line in inp.readlines():
        data.append( [float(x) for x in line.split('\t')[1:]] )
        label.append( float(line.split('\t')[0]) )
    inp.close()
    mat = np.array(data)
    label = np.array(label, dtype=np.float32)
    csr = sparse.csr_matrix(mat)
    handle = ctypes.c_void_p()
    ref = None
    if reference != None:
        ref = ctypes.byref(reference)

    LIB.LGBM_CreateDatasetFromCSR(c_array(ctypes.c_int, csr.indptr), 
        dtype_int32, 
        c_array(ctypes.c_int, csr.indices), 
        csr.data.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p)),
        dtype_float64, 
        len(csr.indptr), 
        len(csr.data),
        csr.shape[1], 
        c_str('max_bin=15'), 
        ref, 
        ctypes.byref(handle) )
    num_data = ctypes.c_long()
    LIB.LGBM_DatasetGetNumData(handle, ctypes.byref(num_data) )
    num_feature = ctypes.c_long()
    LIB.LGBM_DatasetGetNumFeature(handle, ctypes.byref(num_feature) )
    LIB.LGBM_DatasetSetField(handle, c_str('label'), c_array(ctypes.c_float, label), len(label), 0)
    print ('#data:%d #feature:%d' %(num_data.value, num_feature.value) ) 
    return handle

def test_load_from_csc(filename, reference):
    data = []
    label = []
    inp = open(filename, 'r')
    for line in inp.readlines():
        data.append( [float(x) for x in line.split('\t')[1:]] )
        label.append( float(line.split('\t')[0]) )
    inp.close()
    mat = np.array(data)
    label = np.array(label, dtype=np.float32)
    csr = sparse.csc_matrix(mat)
    handle = ctypes.c_void_p()
    ref = None
    if reference != None:
        ref = ctypes.byref(reference)

    LIB.LGBM_CreateDatasetFromCSC(c_array(ctypes.c_int, csr.indptr), 
        dtype_int32, 
        c_array(ctypes.c_int, csr.indices), 
        csr.data.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p)),
        dtype_float64, 
        len(csr.indptr), 
        len(csr.data),
        csr.shape[0], 
        c_str('max_bin=15'), 
        ref, 
        ctypes.byref(handle) )
    num_data = ctypes.c_long()
    LIB.LGBM_DatasetGetNumData(handle, ctypes.byref(num_data) )
    num_feature = ctypes.c_long()
    LIB.LGBM_DatasetGetNumFeature(handle, ctypes.byref(num_feature) )
    LIB.LGBM_DatasetSetField(handle, c_str('label'), c_array(ctypes.c_float, label), len(label), 0)
    print ('#data:%d #feature:%d' %(num_data.value, num_feature.value) ) 
    return handle

def test_load_from_mat(filename, reference):
    data = []
    label = []
    inp = open(filename, 'r')
    for line in inp.readlines():
        data.append( [float(x) for x in line.split('\t')[1:]] )
        label.append( float(line.split('\t')[0]) )
    inp.close()
    mat = np.array(data)
    data = np.array(mat.reshape(mat.size), copy=False)
    label = np.array(label, dtype=np.float32)
    handle = ctypes.c_void_p()
    ref = None
    if reference != None:
        ref = ctypes.byref(reference)

    LIB.LGBM_CreateDatasetFromMat(data.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p)), 
        dtype_float64,
        mat.shape[0],
        mat.shape[1],
        1,
        c_str('max_bin=15'), 
        ref, 
        ctypes.byref(handle) )
    num_data = ctypes.c_long()
    LIB.LGBM_DatasetGetNumData(handle, ctypes.byref(num_data) )
    num_feature = ctypes.c_long()
    LIB.LGBM_DatasetGetNumFeature(handle, ctypes.byref(num_feature) )
    LIB.LGBM_DatasetSetField(handle, c_str('label'), c_array(ctypes.c_float, label), len(label), 0)
    print ('#data:%d #feature:%d' %(num_data.value, num_feature.value) ) 
    return handle
def test_free_dataset(handle):
    LIB.LGBM_DatasetFree(handle)

def test_dataset():
    train = test_load_from_file('../../examples/binary_classification/binary.train', None)
    test = test_load_from_mat('../../examples/binary_classification/binary.test', train)
    test_free_dataset(test)
    test = test_load_from_csr('../../examples/binary_classification/binary.test', train)
    test_free_dataset(test)
    test = test_load_from_csc('../../examples/binary_classification/binary.test', train)
    test_free_dataset(test)
    test_save_to_binary(train, 'train.binary.bin')
    test_free_dataset(train)
    train  = test_load_from_binary('train.binary.bin')
    test_free_dataset(train)
def test_booster():
    train = test_load_from_mat('../../examples/binary_classification/binary.train', None)
    test = [test_load_from_mat('../../examples/binary_classification/binary.test', train)]
    name = [c_str('test')]
    booster = ctypes.c_void_p()
    LIB.LGBM_BoosterCreate(train, c_array(ctypes.c_void_p, test), c_array(ctypes.c_char_p, name), 
        len(test), c_str("app=binary metric=auc num_leaves=31 verbose=0"), ctypes.byref(booster))
    is_finished = ctypes.c_int(0)
    for i in range(100):
        LIB.LGBM_BoosterUpdateOneIter(booster,ctypes.byref(is_finished))
        result = np.array([0.0], dtype=np.float32)
        out_len = ctypes.c_ulong(0)
        LIB.LGBM_BoosterEval(booster, 0, ctypes.byref(out_len), result.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))
        print ('%d Iteration test AUC %f' %(i, result[0]))
    LIB.LGBM_BoosterSaveModel(booster, -1, c_str('model.txt'))
    LIB.LGBM_BoosterFree(booster)
    test_free_dataset(train)
    test_free_dataset(test[0])
    booster2 = ctypes.c_void_p()
    LIB.LGBM_BoosterLoadFromModelfile(c_str('model.txt'), ctypes.byref(booster2))
    data = []
    inp = open('../../examples/binary_classification/binary.test', 'r')
    for line in inp.readlines():
        data.append( [float(x) for x in line.split('\t')[1:]] )
    inp.close()
    mat = np.array(data)
    preb = np.zeros(( mat.shape[0],1 ), dtype=np.float64)
    data = np.array(mat.reshape(mat.size), copy=False)
    LIB.LGBM_BoosterPredictForMat(booster2,
        data.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p)), 
        dtype_float64,
        mat.shape[0],
        mat.shape[1],
        1,
        1,
        50,
        preb.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
    LIB.LGBM_BoosterPredictForFile(booster2, 1, 50, 0, c_str('../../examples/binary_classification/binary.test'), c_str('preb.txt'))
    LIB.LGBM_BoosterFree(booster2)

test_dataset()
test_booster()

