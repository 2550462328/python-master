#!/usr/bin/evn python
# -*- encoding: utf-8 -*-

if __name__ == '__main__':
    array = [1, 4, 3, 3, "A", "B", "c", "A"]

    # 向末尾增加一个新元素
    array.append("AA")
    # 在指定索引位置插入元素
    array.insert(1, "B")
    # 新列表每个元素增加到list中
    array.extend(["D", "DD"])

    # 修改
    array[0] = "updata"  # 修改指定元素的值
    array[1:] = "sss"  # 修改指定索引位置后的全部数据
    list_ = array[-1]
    list_2 = array[1:3]
    a = "a"
    # 字母大写
    print(a.title())

    # 指定元素的索引位置
    if array.index('s'):
        print('s' in array)

    # 删除指定索引位置元素并返回删除元素
    print(array.pop(0))
    # 删除末尾元素
    print(array.pop())
    # 删除指定索引位置元素
    del array[0]
    # 删除指定元素 注:只会找到第一个相同元素删除, list 中没有找到值, Python 会引发一个异常
    array.remove("s")

    # sort永久性排序,reverse=True 倒序
    array.sort(reverse=True)
    # 临时性,reverse=True 倒序
    _list = sorted(array, reverse=True)

    # list运算符
    array = array + ['example', 'new']  # 增加
    array += [1, 2] * 3  # list可以进行复制元素,并累加

    # list中规律增加字符串
    lists = ["A", "B", "C"]
    strlist = ";".join(lists)  # A;B;C
    print(strlist)

    # list 去重
    # ids = [1, 4, 3, 3, 4, 2, 3, 4, 5, 6, 1]
    # func = lambda x, y: x if y in x else x + [y]
    # lists = reduce(func, [[], ] + ids)
    # print(lists)

    # 创建数值列表
    number1 = list(range(1, 6))
    print(number1)

    number2 = list(range(1, 11, 2))
    print(number2)
    # 过滤列表中重复的值
    # [elem for elem in li if li.count(elem) == 1]
