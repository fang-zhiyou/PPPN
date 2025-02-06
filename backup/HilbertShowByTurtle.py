import hilbert_trans

"""
    显示 Hilbert 曲线的坐标情况
"""

# 示例
n = 3  # Hilbert 曲线的阶
grid_size = 60  # 方格大小


import turtle
turtle.setup(800, 800)
turtle.setworldcoordinates(-50, -50, 600, 600)
turtle.setheading(0)
turtle.speed(0)
turtle.color("grey")

# 横纵
for i in range(2 ** n + 1):
    turtle.penup()
    turtle.goto(0, grid_size * i)
    turtle.pendown()
    turtle.goto(grid_size * (2 ** n), grid_size * i)
for i in range(2 ** n):
    turtle.penup()
    turtle.goto(i * grid_size + grid_size / 2, -30)
    turtle.pendown()
    turtle.write(i, align="center", font=("Arial", 16, "bold"))


for i in range(2 ** n + 1):
    turtle.penup()
    turtle.goto(grid_size * i, 0)
    turtle.pendown()
    turtle.goto(grid_size * i, grid_size * (2 ** n))
for i in range(2 ** n):
    turtle.penup()
    turtle.goto(-20, i * grid_size + grid_size / 2)
    turtle.pendown()
    turtle.write(i, align="center", font=("Arial", 16, "bold"))


turtle.color("blue")
for i in range(4 ** n):
    if i == 0:
        x, y = hilbert_trans.d2xy_right(n, i) # 调整方向
        pox = x * grid_size + grid_size / 2
        poy = y * grid_size + grid_size / 2
        turtle.penup()
        turtle.goto(pox, poy)
        turtle.write(i, align="center", font=("Arial", 16, "bold"))
        turtle.pendown()
    else:
        x, y = hilbert_trans.d2xy_right(n, i) # 调整方向
        pox = x * grid_size + grid_size / 2
        poy = y * grid_size + grid_size / 2
        turtle.goto(pox, poy)
        turtle.write(i, align="center", font=("Arial", 16, "bold"))


turtle.done()
