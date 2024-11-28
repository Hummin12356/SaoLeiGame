import random  # 导入python的标准random库
from enum import Enum  # 创建枚举类型

BLOCK_WIDTH = 30  # 定义游戏中方块的宽度
BLOCK_HEIGHT = 16  # 定义游戏中方块的高度
SIZE = 20  # 每块的大小
MINE_COUNTS = {1: 20, 2: 50, 3: 99}  # 每个关卡对应的地雷数量

# 定义BlockStatus的枚举类型
class BlockStatus(Enum):
    """定义方块的状态"""
    normal = 1  # 方块处于正常状态
    opened = 2   # 方块已经被打开
    mine = 3  # 方块是地雷
    flag = 4  # 方块被标记了旗帜
    ask = 5  # 方块处于问号状态
    bomb = 6  # 触发了爆炸
    hint = 7  # 方块有某种提示信息
    double = 8 # 游戏的双倍操作


class Mine:
    """单个地雷块"""
    def __init__(self, x, y, value=0): # 构造函数，初始化地雷块的坐标x和y以及是否为地雷的值
        self._x = x
        self._y = y
        self._value = value  # 0 表示非地雷，1 表示地雷
        self._around_mine_count = -1 # 周围地雷数量暂未计算
        self._status = BlockStatus.normal

    x = property(lambda self: self._x)  # 使用property函数定义了x，y属性的访问方式
    y = property(lambda self: self._y)

    def get_value(self): # 定义get_value，用于捕获value的值
        """返回是否为地雷"""
        return self._value

    def set_value(self, value): # 定义get_value，用于捕获value的值，确保value只能为1或0
        """设置是否为地雷 (0: 非地雷, 1: 地雷)"""
        if value in (0, 1):
            self._value = value
        else:
            raise ValueError("地雷值只能是 0 或 1")  # 返回值限制为0或1，否则抛出ValueError异常

    value = property(get_value, set_value)  #利用property函数，捕获_value的值

    def get_status(self):  #定义get_status(self)方法用于捕获_status的值
        """获取当前方块的状态"""
        return self._status

    def set_status(self, status):
        """设置当前方块的状态"""
        if isinstance(status, BlockStatus):
            self._status = status
        else:
            raise ValueError("状态必须是 BlockStatus 类型")

    status = property(get_status, set_status)  # 将获取和设置方法绑定到status属性

    around_mine_count = property(
        lambda self: self._around_mine_count,
        doc="周围地雷数量"
    )  # 通过属性访问器获取self._around_mine_count的值，由于表示周围地雷的数量



class MineBlock:  # 定义MineBlock类，用于管理所有地雷块
    """管理所有地雷块"""
    def __init__(self, level=3):  # 构造函数，根据传入的关卡level=3初始化地雷快
        # 根据关卡初始化地雷块
        self.mine_count = MINE_COUNTS.get(level, 99) # 从MINE_COUNTS字典中获取对应的关卡的地雷数量，若关卡不存在，则默认为99个雷
        self._block = [[Mine(i, j) for i in range(BLOCK_WIDTH)] for j in range(BLOCK_HEIGHT)]  # 创建一个二维列表，每个元素是一个Mine类的实例，表示一个地雷块
        self._place_mines()  # 调用内部方法来随机放置地雷。

    def get_block(self):
        return self._block

    block = property(get_block)  # 通过property装饰器定义了一个属性block，用于获取地雷块列表。

    def _place_mines(self):  # 随机放置地雷
        """随机放置地雷"""
        for i in random.sample(range(BLOCK_WIDTH * BLOCK_HEIGHT), self.mine_count):  # 从所有可能的方块索引中随机选择self.mine_count个索引。
            self._block[i // BLOCK_WIDTH][i % BLOCK_WIDTH].value = 1  # 现在可以设置 value

    def getmine(self, x, y):  # 获取指定坐标(x, y)处的地雷块
        """获取指定位置的地雷块"""
        return self._block[y][x]  # 返回二维列表_block中指定坐标的Mine实例

    def open_mine(self, x, y):  # 打开指定坐标(x, y)处的地雷块
        """打开一个地雷块"""
        if self._block[y][x].value:  # 如果是地雷
            self._block[y][x].status = BlockStatus.bomb  # 将方块的状态设置为（爆炸）
            return False  # 返回False，表示打开了地雷

        self._block[y][x].status = BlockStatus.opened  # 如果不是地雷，将方块的状态设置为已打开
        around = _get_around(x, y)  # 获取周围的方块坐标

        _sum = 0  # 初始化一个变量来统计周围地雷的数量
        for i, j in around:  # 遍历周围的方块
            if self._block[j][i].value:  # 如果周围的方块是地雷，增加周围地雷的数量
                _sum += 1
        self._block[y][x]._around_mine_count = _sum  # 设置当前方块周围的地雷数量

        if _sum == 0:  # 如果周围没有地雷，则递归打开周围区域
            for i, j in around:  # 再次遍历周围的方块
                if self._block[j][i]._around_mine_count == -1:  # 如果周围方块的周围地雷数量未计算（为 -1）
                    self.open_mine(i, j) # 递归地打开周围的方块

        return True


def _get_around(x, y):  # 定义了一个名为_get_around的函数，它接受两个参数x和y
    """获取指定点周围 8 个点的坐标"""
    return [(i, j) for i in range(max(0, x - 1), min(BLOCK_WIDTH - 1, x + 1) + 1)  # 生成一个i的范围，这个范围是基于x坐标的，确保不会超出方块宽度的边界
            for j in range(max(0, y - 1), min(BLOCK_HEIGHT - 1, y + 1) + 1) if i != x or j != y]  # 生成一个j的范围，这个范围是基于y坐标的，确保不会超出方块高度的边界
