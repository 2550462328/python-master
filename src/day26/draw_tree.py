import turtle
import random
from time import sleep


# 画树的躯干
def tree(branchLen, t):
    sleep(0.0005)
    if branchLen > 3:
        if 8 <= branchLen <= 12:
            if random.randint(0, 2) == 0:
                # 白色
                t.color('snow')
            else:
                # 淡珊瑚色
                t.color('lightcoral')
            t.pensize(branchLen / 3)
        elif branchLen < 8:
            if random.randint(0, 1) == 0:
                t.color('snow')
            else:
                t.color('lightcoral')
            t.pensize(branchLen / 2)
        else:
            # 赭色
            t.color('sienna')
            t.pensize(branchLen / 10)
        t.forward(branchLen)
        a = 1.5 * random.random()
        t.right(20 * a)
        b = 1.5 * random.random()
        tree(branchLen - 10 * b, t)
        t.left(40 * a)
        tree(branchLen - 10 * b, t)
        t.right(20 * a)
        t.up()
        t.backward(branchLen)
        t.down()


def petal(m, t):
    for i in range(m):
        a = 200 - 400 * random.random()
        b = 10 - 20 * random.random()
        t.up()
        t.forward(b)
        t.left(90)
        t.forward(a)
        t.down()
        t.color('lightcoral')
        t.circle(1)
        t.up()
        t.backward(a)
        t.right(90)
        t.backward(b)


def main():
    # 绘图区域
    t = turtle.Turtle()
    # 画布大小
    w = turtle.Screen()
    # 隐藏画笔
    t.hideturtle()
    t.getscreen().tracer(5, 0)
    # 小麦色
    w.screensize(bg='wheat')
    t.left(90)
    t.up()
    t.backward(150)
    t.down()
    t.color('sienna')

    tree(60, t)
    petal(200, t)

    t = turtle.getscreen()
    t.getcanvas().postscript(file='E:\\py\\day26\\tree.eps')
    w.exitonclick()


# 使用 turtle 画布 画一棵树
if __name__ == '__main__':
    main()
