import math

import matplotlib.pyplot as plt
import pygame

meters_per_pixel = 0.01

x = 720
y = 480

allVelocityX = []
allVelocityY = []
allpositionX = []
allpositionY = []
allPotentialEnergy = []
allKineticEnergy = []
allEnergy = []
AllTime = []

pygame.init()
screen = pygame.display.set_mode((x, y))
clock = pygame.time.Clock()
running = True

# ball values
vel_x = 0
vel_y = 0
acc_x = 0
acc_y = 0
circleSize = 0.25
circle_x = 7.2 / 2
circle_y = 4.8 / 2
ballMass = 1.0

# forces
gravity = -9.81

# constants
restitution = 1

time = 0

acc_y = gravity

dt = 0


def physics():
    global circle_x, circle_y, vel_x, vel_y

    # X position
    circle_x += vel_x * dt + acc_x * (dt**2) * 0.5
    vel_x += acc_x * dt

    # Y position
    step_circle_y = circle_y + vel_y * dt + acc_y * (dt**2) * 0.5

    if step_circle_y <= circleSize:
        h = circle_y - circleSize #height before next step

        a = acc_y / 2
        b = vel_y
        c = h

        #Time of the collision
        t1 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
        t2 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)

        valid_times = [t for t in (t1, t2) if 0 <= t <= dt]
        t_hit = min(valid_times) 

        circle_y = circleSize

        vel_y += acc_y * t_hit 
        vel_y = -(vel_y) * restitution.value
        circle_y = circle_y + vel_y * (dt - t_hit) + acc_y * ((dt - t_hit) ** 2) * 0.5
        vel_y += acc_y * (dt - t_hit)

    else:
        circle_y = step_circle_y
        vel_y += acc_y * dt

    potential_energy = -ballMass * gravity * circle_y
    kinetic_energy = 0.5 * ballMass * (vel_x**2 + vel_y**2)
    Energy = kinetic_energy + potential_energy

    print(Energy, time)

    allVelocityX.append(vel_x)
    allVelocityY.append(vel_y)
    allpositionX.append(circle_x)
    allpositionY.append(circle_y)
    allPotentialEnergy.append(potential_energy)
    allKineticEnergy.append(kinetic_energy)
    allEnergy.append(Energy)
    AllTime.append(time)


def draw():
    screen.fill("purple")

    restitution.update()
    restitution.draw(screen)

    pygame.draw.circle(
        screen,
        "green",
        (circle_x / meters_per_pixel, y - circle_y / meters_per_pixel),
        circleSize / meters_per_pixel,
    )

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
    axs[1, 2].set_ylim(0, 25)

    plt.show()


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


restitution = Slider(10, 10, 0, 1, 0.1, 1)


while running:

    dt = clock.tick(60) / 1000  # limits FPS to 60 and converts to seconds
    time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    physics()
    draw()

    # if time >= 5:
    #     running = False

pygame.quit()

graph()