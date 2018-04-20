#-*- coding: utf-8

def isBasicClass(check_class):
    if isinstance(check_class,int) or isinstance(check_class,str) or isinstance(check_class,bool) or \
        isinstance(check_class, bytearray) or isinstance(check_class,bytes) or isinstance(check_class,float):
        return True
    if check_class is None:
        return True
    return False

def class2ProtoDict(check_class):
    '''
    如果是基本类型，直接返回
    是 list/set/dict，则逐一解析并返回原类型
    否则表示是某个类，那么返回解析后的它的 __dict__
    :param check_class:
    :return:
    '''
    if isBasicClass(check_class):
        return check_class

    if isinstance(check_class, dict):
        result = {}
        for var_key in check_class:
            result[var_key] = class2ProtoDict(check_class[var_key])
        return result
    if isinstance(check_class, list):
        result = []
        for var_item in check_class:
            result.append(class2ProtoDict(var_item))
        return result
    if isinstance(check_class, set):
        result = set()
        for var_item in check_class:
            result.add(class2ProtoDict(var_item))
        return result
    if hasattr(check_class, '__dict__'):
        return class2ProtoDict(check_class.__dict__)
    else:
        raise ValueError(check_class)
