import pygame
import sys
from iNaturalist import get_random_animal
from geopy.distance import geodesic

pygame.init()

# Set up the display
WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Guess Game")

clock = pygame.time.Clock()

#load map
world_map = pygame.image.load("Equirectangular.png")
world_map = pygame.transform.scale(world_map, (WIDTH, HEIGHT))

#convert pixel coordinates to latitude and longitude
def pixel_to_geo(x, y, width, height):
    longitude = (x / width) * 360 - 180
    latitude = 90 - (y / height) * 180
    return latitude, longitude


#loading original random animal data
animal = get_random_animal()
print(animal)

#loading original animal image
animal_image = pygame.image.load(animal["image"])
animal_image = pygame.transform.scale(animal_image, (250,250))

#check distance and score

def check_distance(lat,lon):
    global total_score
    guess = (lat, lon)
    correct = (animal["lat"], animal["lon"])
    distance = geodesic(guess, correct).km
    print("Distance from correct location:", distance, "kilometers")

    score = max(0, 5000 - int(distance))
    print("Score:", score)

    total_score += score

    


#load new animal
def load_new_animal():
    global animal, animal_image
    animal = get_random_animal()
    print(animal)
    animal_image = pygame.image.load(animal["image"])
    animal_image = pygame.transform.scale(animal_image, (250,250))



#score reset
total_score = 0

#main loop
while True:
    #event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #detect mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print("Clicked:", x, y)
            lat, lon = pixel_to_geo(x, y, WIDTH, HEIGHT)
            print("Latitude:", lat, "Longitude:", lon)


            #check distance
            check_distance(lat, lon)

            #new animal
            load_new_animal()

    screen.blit(world_map, (0, 0))

    #display animal image and name
    screen.blit(animal_image, (20,20))


    font = pygame.font.SysFont(None, 36)

    text = font.render(animal["name"], True, (255,255,255))

    screen.blit(text, (20, 280))

    #display score
    score_text = font.render(f"Score: {total_score}", True, (255,255,255))
    screen.blit(score_text, (20, 320))

    pygame.display.update()
    clock.tick(60)