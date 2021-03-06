"""
@property
    Python内置的@property装饰器就是负责把一个方法变成属性调用的
    把一个getter方法变成属性，只需要加上@property就可以了，
    此时，@property本身又创建了另一个装饰器@score.setter，负责把一个setter方法变成属性赋值，
    于是，我们就拥有一个可控(对数据进行校验)的属性操作：
"""


class Student():
    _score = 0

    @property
    def score(self):
        return self._score;

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise  ValueError("score must be an integer!")
        if value < 0 or value > 100:
            raise ValueError("score must between 0 - 100")
        self._score = value

s = Student()
print(s.score)  # 0
s.score = 60
print(s.score)  # 60
# s.score = 101  # ValueError: score must between 0 - 100

"""
注意到这个神奇的@property，我们在对实例属性操作的时候，就知道该属性很可能不是直接暴露的，而是通过getter和setter方法来实现的。

还可以定义只读属性，只定义getter方法，不定义setter方法就是一个只读属性：
下面的birth是可读写属性，而age就是一个只读属性，因为age可以根据birth和当前时间计算出来。
"""
class Student():

    _birth = 0

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2021 - self._birth