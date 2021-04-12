from main import rdb


def rdbget(key):
    value = rdb.get(key)
    if isinstance(value, bytes):
        return value.decode()
    else:
        return value

def func_string():
    """
    SET key value [EX seconds] [PX milliseconds] [NX|XX]
    将键key设定为指定的value。
    如果key已经保存了一个值，那么这个操作会直接覆盖原来的值，并且忽略原始类型。
    当set命令执行成功之后，之前设置的过期时间都将失效.
    EX seconds – 设置键key的过期时间，单位时秒
    PX milliseconds – 设置键key的过期时间，单位时毫秒
    NX – 只有键key不存在的时候才会设置key的值
    XX – 只有键key存在的时候才会设置key的值
    """
    if not rdb.exists("k1"):
        rdb.set("k1", "今天下雨", ex=60)
    if not rdb.exists("k2"):
        rdb.set("k2", "今天周一", px=66666)
    print(rdbget("k1"))
    print(rdbget("k2"))
    """
    ttl秒 pttl毫秒
    返回key剩余的过期时间。 这种反射能力允许Redis客户端检查指定key在数据集里面剩余的有效期。
    如果key不存在或者已过期，返回 -2
    如果key存在并且没有设置过期时间（永久有效），返回 -1 。
    """
    print(rdb.ttl("k1"))
    print(rdb.pttl("k2"))
    """
    append key value
    如果 key 已经存在，并且值为字符串，那么这个命令会把 value 追加到原来值（value）的结尾。
    如果 key 不存在，那么它将首先创建一个空字符串的key，再执行追加操作，这种情况 APPEND 将类似于 SET 操作。
    """
    print(rdb.append("k1", "好冷啊"))
    print(rdbget("k1"))
    """
    decr key
    decrby key decrement
    incr key
    incrby key decrement
    对key对应的数字做加减1操作。如果key不存在，那么在操作之前，这个key对应的值会被置为0
    如果key有一个错误类型的value或者是一个不能表示成数字的字符串，就返回错误。这个操作最大支持在64位有符号的整型数字。
    """
    print(rdb.set("k3", "10"))
    # key必须是数字字符串或数字 否则触发异常
    print(rdb.decr("k3"))
    print(rdb.incr("k3"))
    # key必须是数字字符串或数字 否则触发异常
    print(rdb.decrby("k3", 3))
    print(rdb.incrby("k3", 3))
    # 6
    print(rdbget("k3"))
    """
    getrange key start end
    返回key对应的字符串value的子串，这个子串是由start和end位移决定的（两者都在string内）。
    可以用负的位移来表示从string尾部开始数的下标。所以-1就是最后一个字符，-2就是倒数第二个，以此类推。
    这个函数处理超出范围的请求时，都把结果限制在string内。
    """
    rdb.set("k4", "python is awesome!")
    print(rdb.getrange("k4", 0, 9))
    """
    getset key value
    自动将key对应到value并且返回原来key对应的value。如果key存在但是对应的value不是字符串，就返回错误。
    """
    print(rdb.getset("k3", 0))
    print(rdb.get("k3"))
    """
    MGET key [key ...] 原子操作
    返回所有指定的key的value。对于每个不对应string或者不存在的key，都返回特殊值none。
    正因为此，这个操作从来不会失败。
    """
    print(rdb.mget(['k1', 'k2', 'j1']))
    """
    MSET key value [key value ...] 原子操作
    对应给定的keys到他们相应的values上。MSET会用新的value替换已经存在的value，就像普通的SET命令一样。
    总是返回True，因为MSET不会失败。
    MSETNX key value [key value ...] 原子操作
    对应给定的keys到他们相应的values上。只要有一个key已经存在，MSETNX一个操作都不会执行。
    由于这种特性，MSETNX可以实现要么所有的操作都成功，要么一个都不执行，这样可以用来设置不同的key，来表示一个唯一的对象的不同字段。
    """
    d1 = {
        'k1': '123',
        'k2': '456'
    }
    print(rdb.mset(d1))
    d1nx = {
        'k1': '123',
        'k6': '456'
    }
    print(rdb.msetnx(d1nx))
    # STRLEN 返回key的string类型value的长度。如果key对应的非string类型，就返回错误。不存在key返回0
    # rdb.set("k9", 111)
    print(rdb.strlen('k10'))


if __name__ == "__main__":
	if rdb.ping():
		print("redis connected!")
	else:
		print("redis not connected!")
	func_string()