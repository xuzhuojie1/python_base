print("test func")

# 一、=========函数参数==========================

#1.形参变量只有在被调用时才分配内存单元，在调用结束时，即刻释放所分配的内存单元。
# 因此，形参只在函数内部有效。函数调用结束返回主调用函数后则不能再使用该形参变量

#2.实参可以是常量、变量、表达式、函数等，无论实参是何种类型的量，在进行函数调用时，
# 它们都必须有确定的值，以便把这些值传送给形参。因此应预先用赋值，输入等办法使参数获得确定值
def calc(x, y):
    res = x**y
    return res
print(calc(2, 3))  # 8

#3.位置参数和关键字（标准调用：实参与形参位置一一对应；关键字调用：位置无需固定）
def test(x, y, z):
    print("x = {}, y = {}, z = {}".format(x, y, z))
# 位置参数：必须一一对应，缺一不可，多一也不行
    test(1, 2, 3)  # x = 1, y = 2, z = 3
# 关键字：无须一一对应，缺一不可，多一也不行
    test(x="a", y="b", z="c")  # x = a, y = b, z = c
# 位置参数必须是在关键字参数左边
    test(1, z="c", y="b")  # x = 1, y = b, z = c


#4.默认参数
def test(x, y="00y"):
    print("x = {}， y = {}".format(x, y))
test("00x")  # x = 00x， y = 00y
test("11x", "11y")  # x = 11x， y = 11y
test("22x", y="22y")  # x = 22x， y = 22y

#5.参数组
    # * 列表
    # ** 字典
def test(x, *args, **kwargs):
    print("x = {}, args = {}, kwargs={}".format(x, args, kwargs))

test(1, 2, 3, 4, 5, a="a", b="b")  # x = 1, args = (2, 3, 4, 5), kwargs={'a': 'a', 'b': 'b'}
test(1, 2, *[3, 4], **{"a": "a", "b": "b"})  # x = 1, args = (2, 3, 4), kwargs={'a': 'a', 'b': 'b'}


