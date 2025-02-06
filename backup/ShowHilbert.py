import turtle


# 为了展示 4 条曲线重合的结果
def draw_gird(tur: turtle, grid_size, order):
    length = (2 ** (order - 1)) * grid_size
    for y in range(-length, length + 1, grid_size):
        if y == 0:
            tur.color('black')
            tur.penup()
            tur.goto(-length, y)
            tur.pendown()
            tur.goto(length, y)
            tur.write(y)
            tur.color('grey')
        else:
            tur.penup()
            tur.goto(-length, y)
            tur.pendown()
            tur.goto(length, y)
            tur.write(y)

    for x in range(-length, length + 1, grid_size):
        if x == 0:
            tur.color('black')
            tur.penup()
            tur.goto(x, length)
            tur.pendown()
            tur.write(x)
            tur.goto(x, -length)
            tur.color('grey')
        else:
            tur.penup()
            tur.goto(x, length)
            tur.pendown()
            tur.write(x)
            tur.goto(x, -length)


def hilbert_curve_up(tur, level, angle, step):
    if level == 0:
        return
    tur.right(angle)
    hilbert_curve_up(tur, level - 1, -angle, step)
    tur.forward(step)
    tur.left(angle)
    hilbert_curve_up(tur, level - 1, angle, step)
    tur.forward(step)
    hilbert_curve_up(tur, level - 1, angle, step)
    tur.left(angle)
    tur.forward(step)
    hilbert_curve_up(tur, level - 1, -angle, step)
    tur.right(angle)


# 配置信息，order_curve 希尔伯特曲线的阶， grid_size 单元格的大小
order_curve = 3
grid_size = 30


st_pos = (2 ** (order_curve - 1)) * grid_size - grid_size // 2

turtle.setup(910, 910)
turtle.color('grey')
turtle.speed("fastest")
turtle.penup()
draw_gird(turtle, grid_size, order_curve)

# 画四条 Hibert Curve
turtle.penup()
turtle.setheading(0)
turtle.goto(-st_pos, st_pos)
turtle.color("blue")
turtle.pendown()
hilbert_curve_up(turtle, order_curve, 90, grid_size)

turtle.penup()
turtle.setheading(90)
turtle.goto(-st_pos, -st_pos)
turtle.color("blue")
turtle.pendown()
hilbert_curve_up(turtle, order_curve, 90, grid_size)

turtle.penup()
turtle.setheading(180)
turtle.goto(st_pos, -st_pos)
turtle.color("blue")
turtle.pendown()
hilbert_curve_up(turtle, order_curve, 90, grid_size)

turtle.penup()
turtle.setheading(270)
turtle.goto(st_pos, st_pos)
turtle.color("blue")
turtle.pendown()
hilbert_curve_up(turtle, order_curve, 90, grid_size)

turtle.done()

