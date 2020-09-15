import turtle

def draw_square(size):
    for i in range(4):
        turtle.forward(size)
        turtle.left(90)

def draw_grid(size, row):
    column = 0

    turtle.penup()
    turtle.goto(-200, -200)
    turtle.pendown()

    while column < row:
        for i in range(5):
            draw_square(size)
            turtle.forward(size)
        turtle.penup()
        turtle.goto(turtle.xcor() - 500, turtle.ycor() + 100)
        turtle.pendown()
        column += 1

if __name__ == "__main__":
    draw_grid(100, 5)
    turtle.exitonclick()