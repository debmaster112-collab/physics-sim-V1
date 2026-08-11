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
allEnergy = []
AllTime = []

pygame.init()
screen = pygame.display.set_mode((x, y))
clock = pygame.time.Clock()
running = True

vel_x = 0
vel_y = 0
gravity = -9.81
restitution = 1
acc_x = 0
acc_y = 0
ballMass = 1.0
time = 0

circleSize = 0.25

circle_x = circleSize #7.2 / 2
circle_y = 4.8 / 2

dt = 0


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
        pygame.draw.circle(screen, "red", (self.x + int((self.value - self.minVal) / (self.maxVal - self.minVal) * 200), self.y + 10) , 10)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()            
        if (self.x <= mouse_x <= self.x + self.w and self.y <= mouse_y <= self.y + self.h and pygame.mouse.get_pressed()[0]):
            x = self.minVal + (self.maxVal - self.minVal) * ((mouse_x - self.x) / 200)
            self.value = (round(x / self.step) * self.step)

        

restitution = Slider(10, 10, 0, 1, 0.1, 1)
test2 = Slider(10, 40, -20, 0, 1, -9)
        
        

while running:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    restitution.update()
    restitution.draw(screen)

    test2.update()
    test2 .draw(screen)

    time += dt

    #X position
    vel_x += acc_x * dt
    circle_x += vel_x * dt

    #Y position
    vel_y += (gravity + acc_y) * dt
    circle_y += vel_y * dt

    if circle_y <= circleSize:
        circle_y = circleSize
        vel_y = -vel_y * restitution.value
          
    potential_energy = -ballMass * gravity * circle_y
    kinetic_energy = 0.5 * ballMass * (vel_x ** 2 + vel_y ** 2)

    allVelocityX.append(vel_x)
    allVelocityY.append(vel_y)
    allpositionX.append(circle_x)
    allpositionY.append(circle_y)
    allPotentialEnergy.append(potential_energy)
    allKineticEnergy.append(kinetic_energy)
    allEnergy.append(kinetic_energy + potential_energy)
    AllTime.append(time)



    pygame.draw.circle(screen, "green", (circle_x / meters_per_pixel, y - circle_y / meters_per_pixel), circleSize / meters_per_pixel)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # limits FPS to 60 and converts to seconds

    # if time >= 5:
    #     running = False

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
axs[0, 2].plot(AllTime, allKineticEnergy)
axs[0, 2].set_title("Potential and kinetic Energy vs Time")
axs[0, 2].set_xlabel("Time (s)")
axs[0, 2].set_ylabel("Potential and Kinetic Energy (J)")

axs[1, 2].plot(AllTime, allEnergy)
axs[1, 2].set_title("Energy vs Time")
axs[1, 2].set_xlabel("Time (s)")
axs[1, 2].set_ylabel("Energy (J)")  

plt.show()