import re
from functools import reduce

"""
一行代码实现1-100奇数求和（至少5种方案）

sum1 = 0
for i in range(101):
    if i % 2 == 1:
        sum1 += i
print(sum1)

sum_2 = reduce(lambda x, y: x + y, [i if i % 2 == 1 else 0 for i in range(101)])
print(sum_2)
sum_3 = reduce(lambda x, y: x + y, filter(lambda x: x % 2 == 1, [i for i in range(101)]))
print(sum_3)
sum_4 = sum(i if i % 2 == 1 else 0 for i in range(101))
print(sum_4)
"""
"""
练习4：登录，如果登录成功（username=qzcsbj，password=123456），输出欢迎信息，退出程序，如果错误次数3次，退出程序


n = 0
while True:
    a = input('please enter your username:')
    b = input('please enter your password:')
    if a == 'yanfei' and b == '123123':
        print('welcome')
        break
    else:
        n += 1
        if n < 3:
            print('login error {} times ,please try again'.format(n))
        else:
            print('login error {} times ,quit'.format(n))
            break
"""
"""
冒泡排序
练习6：冒泡排序，data = [10, 4, 33, 21, 54, 8, 11, 5]
每一趟只能确定将一个数归位。即第一趟只能确定将末位上的数归位，第二趟只能将倒数第 2 位上的数归位，依次类推下去。如果有 n 个数进行排序，只需将 n-1 个数归位，也就是要进行 n-1 趟操作。
而 “每一趟 ” 都需要从第一位开始进行相邻的两个数的比较，将较大的数放后面，比较完毕之后向后挪一位继续比较下面两个相邻的两个数大小关系，重复此步骤，直到最后一个还没归位的数。

data = [10, 4, 33, 21, 54, 8, 11, 5]
for i in range(len(data)):
    for j in range(len(data) - i - 1):
        if data[j + 1] < data[j]:
            data[j], data[j + 1] = data[j + 1], data[j]
    print(data)
"""
"""
列表 [11,22,33,44,55,66,77,88,99]，将所有大于 66 的值保存至字典的第一个key中，将小于 66 的值保存至第二个key的值中。即： {'k1': 大于66的所有值, 'k2': 小于66的所有值}

test_str2 = [11, 22, 33, 44, 55, 66, 77, 88, 99]
test_str_dic = {}
test_str_dic['key1'] = list()
test_str_dic['key2'] = list()
for item in test_str2:
    if item > 66:
        test_str_dic['key1'].append(item)
    else:
        test_str_dic['key2'].append(item)
print(test_str_dic)
"""
"""
练习3：两个列表，其中一个列表比另外一个列表多一个元素，写一个函数，返回这个元素


lia = [1, 2, 3, 4, 5, 4]
lib = [1, 2, 3, 4, 5]
for item in lib:
    lia.remove(item)
print(lia)
"""
"""
练习6：提取出只包含数字及字母，且以字母开头的最长的子字符串，打印出子字符串及其长度，如果有多个，都要打印出来。


testStr = '#ab1k23$%&()*+,-./:;<=ab12w4>?666qzcsbj@[4f]^{1aaa12|}'
test_srt_list = re.findall("[a-zA-Z]\w+", testStr)
print(sorted(test_srt_list, key=lambda x: len(x), reverse=True))
"""
testsort = '2kd4-1124*2|^2sdAmZ%fkMcv'
test = sorted(testsort, reverse=True)
new_list = []
for i in range(len(test)/2):
    new_list.append((test[i], test[len(test)-1 - i]))
print(new_list)