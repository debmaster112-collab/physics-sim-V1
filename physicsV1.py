import pygame
import matplotlib.pyplot as plt

meters_per_pixel = 0.01

x = 720 
y = 480 

allVelocityX = []
allVelocityY = []
allpositionX = []
allpositionY = []
allPotentialEnergy = []
allKineticEnergy = []
AllTime = []

pygame.init()
screen = pygame.display.set_mode((x, y))
clock = pygame.time.Clock()
running = True

vel_x = 0
vel_y = 0
gravity = -9.81
acc_x = 0
acc_y = gravity
ballMass = 1.0
time = 0

circleSize = 0.25

circle_x = circleSize #7.2 / 2
circle_y = 4.8 / 2

dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    time += dt

    #X position
    vel_x += acc_x * dt
    circle_x += vel_x * dt

    #Y position
    vel_y += gravity * dt
    circle_y += vel_y * dt

    potential_energy = ballMass * gravity * circle_y
    kinetic_energy = 0.5 * ballMass * (vel_x ** 2 + vel_y ** 2)

    allVelocityX.append(vel_x)
    allVelocityY.append(vel_y)
    allpositionX.append(circle_x)
    allpositionY.append(circle_y)
    allPotentialEnergy.append(potential_energy)
    allKineticEnergy.append(kinetic_energy)
    AllTime.append(time)

    if circle_y <= circleSize:
        circle_y = circleSize
        vel_y = -vel_y

    pygame.draw.circle(screen, "green", (circle_x / meters_per_pixel, y - circle_y / meters_per_pixel), circleSize / meters_per_pixel)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS to 60 and converts to seconds

    if time >= 5:
        running = False

pygame.quit()

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
axs[0, 2].set_title("Potential Energy vs Time")
axs[0, 2].set_xlabel("Time (s)")
axs[0, 2].set_ylabel("Potential Energy (J)")

axs[1, 2].plot(AllTime, allKineticEnergy)
axs[1, 2].set_title("Kinetic Energy vs Time")
axs[1, 2].set_xlabel("Time (s)")
axs[1, 2].set_ylabel("Kinetic Energy (J)")  

plt.show()