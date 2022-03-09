import datetime
import time
import calendar
import pytz

if __name__ == '__main__':
    # 当前时间
    nowTime = datetime.datetime.now()
    strNowTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间,变为字符串
    # time.sleep(0.3)
    endTime = datetime.datetime.now()
    # 时间计算
    nowTime = nowTime + datetime.timedelta(seconds=1)  # 秒
    nowTime = nowTime + datetime.timedelta(days=1)  # 天
    nowTime = nowTime + datetime.timedelta(hours=1)  # 小时
    print(nowTime)
    print(nowTime.year)
    print(nowTime.day)
    print(nowTime.hour)

    print(nowTime.second)
    # 0:星期1 -- 6:星期天
    print(nowTime.weekday())

    riqi = "2018-06-03 14:52:13"
    cc = "1463392800000"
    cc = int(cc)

    # 将字符串转换为时间
    riqis = datetime.datetime.strptime(riqi, '%Y-%m-%d %H:%M:%S')

    # 将时间戳1463392800000转换为普通格式时间str
    xx = time.strftime("%y%m%d", time.localtime(cc / 1000))
    print(xx, type(xx))
    xx = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cc / 1000))
    print(xx, type(xx))

    # 将字符串整理成为时间戳1528008733000
    xx = int(time.mktime(time.strptime(riqi, "%Y-%m-%d %H:%M:%S"))) * 1000
    print(xx)

    # 获得指定月份有多少天
    monthRange = calendar.monthrange(2018, 2)
    # (3, 28)星期几(0,星期日),天数
    print(monthRange)

    # 东八区
    tz = pytz.timezone('Asia/Shanghai')
    t = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
