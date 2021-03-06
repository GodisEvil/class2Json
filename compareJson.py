#-*- coding: utf-8
'''
    对比接口返回的 json，输出如下：
    add
        keyPath type
        ...
    minux
        keyPath type
        ...
    diff
        keyPath from {} to {}
'''

import sys
import json


def isBasicClass(check_class):
    if isinstance(check_class,int) or isinstance(check_class,str) or isinstance(check_class,bool) or \
        isinstance(check_class, bytearray) or isinstance(check_class,bytes) or isinstance(check_class,float):
        return True
    if check_class is None:
        return True
    return False


def compare(oldValue, newValue, keyPath = '.'):
    '''
    先确定数据类型，数据类型不同则直接返回 {diff: 'from {} to {}'}
    数据类型相同，则判断是否复合类型，是的话则检查类型里的元素
        list，只检查 oldValue[0] 和 newValue[0]，长度不同则返回 {'diff': 'new list length {}, old list lenth {}'.format(len(oldValue), len(newValue))}
        dict，逐一检查是否有键不同，有的话
            add key type
            minus key type
            相同的键则对元素递归检查
        tuple、set 直接报错
    :param oldValue:
    :param newValue:
    :return:
    '''
    keyPath = keyPath.strip('.')
    if str(type(oldValue)) == str(type(newValue)):
        if isBasicClass(oldValue):
            return {}
        if isinstance(oldValue, list):
            ## 假设 list 的数据类型是一样的，所以统一只检查第一个元素
            if not oldValue or not newValue:
                if oldValue == newValue:
                    return {}
                return {'diff': [{keyPath: ('old length {}, new length: {}'.format(len(oldValue), len(newValue)))}]}
            result = compare(oldValue[0], newValue[0], keyPath + '[0]')
            return result
        if isinstance(oldValue, dict) and isinstance(newValue, dict):
            result =  {'add': [], 'minus': [], 'diff': []}
            oldKyes, newKeys = set(oldValue.keys()), set(newValue.keys())
            sameKeys = oldKyes & newKeys
            minusKeys = oldKyes - newKeys
            addKeys = newKeys - oldKyes
            for key in minusKeys:
                result['minus'].append({keyPath + '.' + key: type(oldValue[key])})
            for key in addKeys:
                result['add'].append({keyPath + '.' + key: type(newValue[key])})
            for key in sameKeys:
                tmpResult = compare(oldValue[key], newValue[key], keyPath + '.' + key)
                if tmpResult:
                    for key in result:
                        result[key].extend(tmpResult.get(key, []))
            if not result['add']:
                result.pop('add')
            if not result['minus']:
                result.pop('minus')
            if not result['diff']:
                result.pop('diff')
            if not result:
                return {}
            return result
        raise ValueError(type(oldValue))
    else:
        return {'diff': [{keyPath: 'from {} to {}'.format(type(oldValue), type(newValue))}]}


def compareFile(file1, file2):
    oldData = open(file1, 'r', encoding='utf-8').read()
    newData = open(file2, 'r', encoding='utf-8').read()
    oldData = json.loads(oldData)
    newData = json.loads(newData)
    result = compare(oldData, newData, '.')
    return result


if __name__ == '__main__':
    result = compareFile(sys.argv[1], sys.argv[2])
    #print(result)
    print('diff file {}, {}'.format(sys.argv[1], sys.argv[2]))
    for diffKey in result:
        print('{}:'.format(diffKey))
        for diffDetail in result[diffKey]:
            for keyPath in diffDetail:
                print('\t{}: {}'.format(keyPath, diffDetail[keyPath]))
