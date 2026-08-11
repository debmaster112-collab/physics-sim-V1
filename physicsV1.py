import pygame
import matplotlib.pyplot as plt

meters_per_pixel = 0.01

x = 720 
y = 480 

allVelocity = []
allposition = []
AllTime = []

pygame.init()
screen = pygame.display.set_mode((x, y))
clock = pygame.time.Clock()
running = True

vel = 0
acc = 9.81
time = 0

circleSize = 0.25

circle_x = 7.2 / 2
circle_y = 4.8 / 2

dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")


    vel += acc * dt
    circle_y += vel * dt
    time += dt

    allVelocity.append(vel)
    allposition.append(circle_y)
    AllTime.append(time)

    # if circle_y >= y - circleSize:
        # circle_y = y - circleSize
        # vel = -vel

    pygame.draw.circle(screen, "green", (circle_x / meters_per_pixel, circle_y / meters_per_pixel), circleSize / meters_per_pixel)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS to 60 and converts to seconds

    if time >= 5:
        running = False

pygame.quit()


fig, axs = plt.subplots(2)
fig.suptitle("Physics Simulation")

axs[0].plot(AllTime, allVelocity)
axs[0].set_title("Velocity vs Time")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Velocity (m/s)")

axs[1].plot(AllTime, allposition)
axs[1].set_title("Position vs Time")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Position (m)")

plt.show()