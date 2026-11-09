import tkinter as tk


WIDTH = 800
HEIGHT = 500
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 90
BALL_SIZE = 16
PADDLE_SPEED = 7


class Pong:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#111827", highlightthickness=0)
        self.canvas.pack()

        self.left_y = HEIGHT / 2
        self.right_y = HEIGHT / 2
        self.ball_x = WIDTH / 2
        self.ball_y = HEIGHT / 2
        self.ball_dx = 5
        self.ball_dy = 3
        self.left_score = 0
        self.right_score = 0
        self.keys = set()

        self.left_paddle = self.canvas.create_rectangle(30, 0, 30 + PADDLE_WIDTH, 0, fill="white", outline="")
        self.right_paddle = self.canvas.create_rectangle(0, 0, 0, 0, fill="white", outline="")
        self.ball = self.canvas.create_oval(0, 0, 0, 0, fill="#fbbf24", outline="")
        self.score = self.canvas.create_text(
            WIDTH / 2,
            35,
            text="0     0",
            fill="white",
            font=("TkDefaultFont", 24, "bold"),
        )
        self.canvas.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="#374151", dash=(8, 8))

        self.root.bind("<KeyPress>", self.key_down)
        self.root.bind("<KeyRelease>", self.key_up)
        self.draw()
        self.update()

    def key_down(self, event):
        self.keys.add(event.keysym.lower())
        if event.keysym == "Escape":
            self.root.destroy()

    def key_up(self, event):
        self.keys.discard(event.keysym.lower())

    def draw(self):
        self.canvas.coords(
            self.left_paddle,
            30,
            self.left_y - PADDLE_HEIGHT / 2,
            30 + PADDLE_WIDTH,
            self.left_y + PADDLE_HEIGHT / 2,
        )
        self.canvas.coords(
            self.right_paddle,
            WIDTH - 30 - PADDLE_WIDTH,
            self.right_y - PADDLE_HEIGHT / 2,
            WIDTH - 30,
            self.right_y + PADDLE_HEIGHT / 2,
        )
        self.canvas.coords(
            self.ball,
            self.ball_x - BALL_SIZE / 2,
            self.ball_y - BALL_SIZE / 2,
            self.ball_x + BALL_SIZE / 2,
            self.ball_y + BALL_SIZE / 2,
        )
        self.canvas.itemconfigure(self.score, text=f"{self.left_score}     {self.right_score}")

    def update(self):
        if "w" in self.keys:
            self.left_y -= PADDLE_SPEED
        if "s" in self.keys:
            self.left_y += PADDLE_SPEED
        if "up" in self.keys:
            self.right_y -= PADDLE_SPEED
        if "down" in self.keys:
            self.right_y += PADDLE_SPEED

        half_paddle = PADDLE_HEIGHT / 2
        self.left_y = max(half_paddle, min(HEIGHT - half_paddle, self.left_y))
        self.right_y = max(half_paddle, min(HEIGHT - half_paddle, self.right_y))

        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_y <= BALL_SIZE / 2 or self.ball_y >= HEIGHT - BALL_SIZE / 2:
            self.ball_dy *= -1

        left_edge = 30 + PADDLE_WIDTH
        right_edge = WIDTH - 30 - PADDLE_WIDTH
        if (
            self.ball_dx < 0
            and left_edge - BALL_SIZE / 2 <= self.ball_x <= left_edge + BALL_SIZE / 2
            and abs(self.ball_y - self.left_y) <= half_paddle + BALL_SIZE / 2
        ):
            self.ball_dx = abs(self.ball_dx)
            self.ball_dy += (self.ball_y - self.left_y) / 18
        elif (
            self.ball_dx > 0
            and right_edge - BALL_SIZE / 2 <= self.ball_x <= right_edge + BALL_SIZE / 2
            and abs(self.ball_y - self.right_y) <= half_paddle + BALL_SIZE / 2
        ):
            self.ball_dx = -abs(self.ball_dx)
            self.ball_dy += (self.ball_y - self.right_y) / 18

        if self.ball_x < 0:
            self.right_score += 1
            self.reset_ball(-1)
        elif self.ball_x > WIDTH:
            self.left_score += 1
            self.reset_ball(1)

        self.draw()
        self.root.after(16, self.update)

    def reset_ball(self, direction):
        self.ball_x = WIDTH / 2
        self.ball_y = HEIGHT / 2
        self.ball_dx = 5 * direction
        self.ball_dy = 3


if __name__ == "__main__":
    window = tk.Tk()
    Pong(window)
    window.mainloop()