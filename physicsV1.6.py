import math

import matplotlib.pyplot as plt
import pygame

meters_per_pixel = 0.01

x = 7.2
y = 4.8

allVelocityX = []
allVelocityY = []
allpositionX = []
allpositionY = []
allPotentialEnergy = []
allKineticEnergy = []
allEnergy = []
AllTime = []

pygame.init()
screen = pygame.display.set_mode((x / meters_per_pixel, y / meters_per_pixel))
clock = pygame.time.Clock()
running = True

# forces
gravity = -9.81


class Slider:
    def __init__(self, x, y, minVal, maxVal, step, initialValue):
        self.x = x
        self.y = y
        self.w = 200
        self.h = 20
        self.rect = pygame.Rect(x, y, 200, 20)
        self.minVal = minVal
        self.maxVal = maxVal
        self.step = step
        self.value = initialValue

    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.rect, 0, 10)
        pygame.draw.circle(
            screen,
            "red",
            (
                self.x
                + int((self.value - self.minVal) / (self.maxVal - self.minVal) * 200),
                self.y + 10,
            ),
            10,
        )

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (
            self.x <= mouse_x <= self.x + self.w
            and self.y <= mouse_y <= self.y + self.h
            and pygame.mouse.get_pressed()[0]
        ):
            x = self.minVal + (self.maxVal - self.minVal) * ((mouse_x - self.x) / 200)
            self.value = round(x / self.step) * self.step


class Ball:
    def __init__(self, x, y, vel_x, vel_y, mass, radius):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.acc_x = 0
        self.acc_y = gravity
        self.mass = mass
        self.r = radius

    def update(self):
        # X position

        step_circle_x = self.x + self.vel_x * dt + self.acc_x * (dt**2) * 0.5

        if step_circle_x <= self.r:  # left wall collision
            w = self.x - self.r  # distance before next step

            a = self.acc_x / 2
            b = self.vel_x
            c = w

            # Time of the collision

            if a != 0:
                t1 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
                t2 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)

                valid_times = [t for t in (t1, t2) if 0 <= t <= dt]
                t_hit = min(valid_times)

            else:
                t_hit = -c / b

            t_after = dt - t_hit

            self.x = self.r

            self.vel_x += self.acc_x * t_hit
            self.vel_x = -(self.vel_x) * restitution.value
            self.x = self.x + self.vel_x * t_after + self.acc_x * t_after**2 * 0.5
            self.vel_x += self.acc_x * t_after

        elif step_circle_x >= x - self.r:  # right wall collision
            w = x - self.r - self.x  # height before next step

            a = self.acc_x / 2
            b = self.vel_x
            c = w

            # Time of the collision

            if a != 0:
                t1 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
                t2 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)

                valid_times = [t for t in (t1, t2) if 0 <= t <= dt]
                t_hit = min(valid_times)

            else:
                t_hit = -c / b

            t_after = dt - t_hit

            self.x = x - self.r

            self.vel_x += self.acc_x * t_hit
            self.vel_x = -(self.vel_x) * restitution.value
            self.x = self.x + self.vel_x * t_after + self.acc_x * t_after**2 * 0.5
            self.vel_x += self.acc_x * t_after

        else:
            self.x = step_circle_x
            self.vel_x += self.acc_x * dt

        if self.x <= self.r:
            self.x = self.r
            self.vel_x = 0

        if self.x >= x - self.r:
            self.x = x - self.r
            self.vel_x = 0

        # Y position
        step_circle_y = self.y + self.vel_y * dt + self.acc_y * (dt**2) * 0.5

        if step_circle_y <= self.r:  # floor collision
            h = self.y - self.r  # height before next step

            a = self.acc_y / 2
            b = self.vel_y
            c = h

            if a != 0:
                # Time of the collision
                t1 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
                t2 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)

                valid_times = [t for t in (t1, t2) if 0 <= t <= dt]
                t_hit = min(valid_times)

            else:
                t_hit = -c / b

            t_after = dt - t_hit

            self.y = self.r

            self.vel_y += self.acc_y * t_hit
            self.vel_y = -(self.vel_y) * restitution.value
            self.y = (self.y + self.vel_y * t_after) + self.acc_y * t_after**2 * 0.5
            self.vel_y += self.acc_y * t_after

        elif step_circle_y >= y - self.r:  # roof collision
            h = self.y - y + self.r  # height before next step

            a = self.acc_y / 2
            b = self.vel_y
            c = h

            if a != 0:
                # Time of the collision
                t1 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
                t2 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)

                valid_times = [t for t in (t1, t2) if 0 <= t <= dt]
                t_hit = min(valid_times)

            else:
                t_hit = -c / b

            t_after = dt - t_hit

            self.y = y - self.r

            self.vel_y += self.acc_y * t_hit
            self.vel_y = -(self.vel_y) * restitution.value
            self.y = (self.y + self.vel_y * t_after) + self.acc_y * t_after**2 * 0.5
            self.vel_y += self.acc_y * t_after

        else:
            self.y = step_circle_y
            self.vel_y += self.acc_y * dt

        if self.r >= self.y:
            self.y = self.r
            self.vel_y = 0

        potential_energy = -self.mass * gravity * (self.y - self.r)
        kinetic_energy = 0.5 * self.mass * (self.vel_x**2 + self.vel_y**2)
        Energy = kinetic_energy + potential_energy

        allVelocityX.append(self.vel_x)
        allVelocityY.append(self.vel_y)
        allpositionX.append(self.x)
        allpositionY.append(self.y)
        allPotentialEnergy.append(potential_energy)
        allKineticEnergy.append(kinetic_energy)
        allEnergy.append(Energy)
        AllTime.append(time)

    def draw(self):
        pygame.draw.circle(
            screen,
            "green",
            (self.x / meters_per_pixel, (y - self.y) / meters_per_pixel),
            self.r / meters_per_pixel,
        )


ball = Ball(x / 2, y / 2, 10, 10, 1, 0.25)

restitution = Slider(10, 10, 0, 1, 0.1, 1)

time = 0
dt = 0

# def physics():
#     global ball


def draw():
    screen.fill("purple")

    restitution.update()
    restitution.draw(screen)

    ball.draw()

    pygame.display.flip()


def graph():
    fig, axs = plt.subplots(2, 3)

    fig.suptitle("Physics Simulation")

    axs[0, 0].plot(AllTime, allpositionX)
    axs[0, 0].set_title("Position X vs Time")
    axs[0, 0].set_xlabel("Time (s)")
    axs[0, 0].set_ylabel("Position X (m)")

    axs[0, 1].plot(AllTime, allpositionY)
    axs[0, 1].set_title("Position Y vs Time")
    axs[0, 1].set_xlabel("Time (s)")
    axs[0, 1].set_ylabel("Position Y (m)")

    axs[1, 0].plot(AllTime, allVelocityX)
    axs[1, 0].set_title("Velocity X vs Time")
    axs[1, 0].set_xlabel("Time (s)")
    axs[1, 0].set_ylabel("Velocity X (m/s)")

    axs[1, 1].plot(AllTime, allVelocityY)
    axs[1, 1].set_title("Velocity Y vs Time")
    axs[1, 1].set_xlabel("Time (s)")
    axs[1, 1].set_ylabel("Velocity Y (m/s)")

    axs[0, 2].plot(AllTime, allPotentialEnergy)
    axs[0, 2].plot(AllTime, allKineticEnergy)
    axs[0, 2].set_title("Potential and kinetic Energy vs Time")
    axs[0, 2].set_xlabel("Time (s)")
    axs[0, 2].set_ylabel("Potential and Kinetic Energy (J)")

    axs[1, 2].plot(AllTime, allEnergy)
    axs[1, 2].set_title("Energy vs Time")
    axs[1, 2].set_xlabel("Time (s)")
    axs[1, 2].set_ylabel("Energy (J)")
    # axs[1, 2].set_ylim(0, 25)

    plt.show()


while running:
    dt = clock.tick(60) / 1000  # limits FPS to 60 and converts to seconds
    time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ball.update()
    draw()

    # if time >= 5:
    #     running = False

pygame.quit()

graph()
