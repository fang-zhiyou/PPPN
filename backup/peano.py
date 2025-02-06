import peano_trans

N = 3
grid_size = 30

SIDE = 2 ** N
MAX_ID = 4 ** N
MAX_P = SIDE * grid_size


import turtle
turtle.setup(800, 800)
turtle.setworldcoordinates(-50, -50, 600, 600)
turtle.setheading(0)
turtle.speed(0)
turtle.color("grey")


# 横纵
X = [i * grid_size for i in range(SIDE + 1)]
Y = [i * grid_size for i in range(SIDE + 1)]
for i, v in enumerate(X):
    turtle.penup()
    turtle.goto(v, MAX_P)
    turtle.pendown()
    turtle.goto(v, 0)
    turtle.penup()
for i, v in enumerate(Y):
    turtle.penup()
    turtle.goto(0, v)
    turtle.pendown()
    turtle.goto(MAX_P, v)
for i in range(SIDE + 1):
    turtle.penup()
    turtle.goto(X[i], - grid_size)
    turtle.pendown()
    turtle.write(i, align="center", font=("Arial", 16, "bold"))
for i in range(SIDE + 1):
    turtle.penup()
    turtle.goto(-20, Y[i] - 10)
    turtle.pendown()
    turtle.write(i, align="center", font=("Arial", 16, "bold"))

# 画曲线 1
turtle.color('blue')
turtle.penup()
x, y = peano_trans.d2xy_1(SIDE, 0)
turtle.goto(grid_size * x + grid_size / 2, grid_size * y + grid_size / 2)
turtle.pendown()

for i in range(MAX_ID):
    x, y = peano_trans.d2xy_1(SIDE, i)
    turtle.goto(grid_size * x + grid_size / 2, grid_size * y + grid_size / 2)
    d = peano_trans.xy2d_1(SIDE, x, y)
    turtle.write(i, align="center", font=("Arial", 16, "bold"))

# # 画曲线 2
# turtle.penup()
# x, y = peano_trans.d2xy_2(SIDE, 0)
# turtle.goto(grid_size * x + grid_size / 2, grid_size * y + grid_size / 2)
# turtle.pendown()
#
# for i in range(MAX_ID):
#     x, y = peano_trans.d2xy_2(SIDE, i)
#     turtle.goto(grid_size * x + grid_size / 2, grid_size * y + grid_size / 2)
#     # d = peano_trans.xy2d_1(SIDE, x, y)
#     # turtle.write(i, align="center", font=("Arial", 16, "bold"))

turtle.done()

