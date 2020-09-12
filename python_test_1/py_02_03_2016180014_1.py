import turtle

class DrawingTool:
    def __init__(self, pen_size):
        turtle.hideturtle()
        turtle.pensize(pen_size)
        #turtle.speed(0)
        self.move(-290,100)

    def move(self, x, y):
        turtle.penup()
        turtle.goto(x,y)
        turtle.pendown()

    def reset_degree(self):
        turtle.setheading(0)

    def draw_K(self):
        turtle.forward(60)
        turtle.right(120)
        turtle.forward(90)
        self.reset_degree()

    def draw_M(self):
        for i in range(4):
            if i % 2 == 0: turtle.forward(70)
            else: turtle.forward(45)
            turtle.right(90)
        self.reset_degree()

    def draw_I(self):
        turtle.right(90)
        turtle.forward(100)
        self.reset_degree()

    def draw_J(self):
        self.draw_K()
        turtle.left(60)
        turtle.forward(50)
        turtle.right(120)
        turtle.forward(50)
        self.reset_degree()

    def draw_S(self):
        turtle.right(110)
        turtle.forward(70)
        turtle.backward(40)
        turtle.left(60)
        turtle.forward(50)
        self.reset_degree()

    def draw_EO(self):
        self.draw_I()
        turtle.left(90)
        turtle.forward(60)
        turtle.left(90)
        turtle.forward(30)
        self.reset_degree()

    def draw_O(self):
        turtle.circle(30)
        self.reset_degree()


if __name__ == "__main__":
    name = DrawingTool(5)
    name.draw_K()
    name.move(-200, 120)

    name.draw_I()
    name.move(-270, 8)

    name.draw_M()
    name.move(-160, 90)

    name.draw_J()
    name.move(-65, 100)

    name.draw_I()
    name.move(0, 100)

    name.draw_S()
    name.move(45, 120)

    name.draw_EO()
    name.move(30, -40)

    name.draw_O()
    turtle.exitonclick()