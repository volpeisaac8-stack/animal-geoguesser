import pygame
import sys
from iNaturalist import get_random_animal
from geopy.distance import geodesic
import math

pygame.init()

# Set up the display
WIDTH = 1200
HEIGHT = 700


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Guess Game")

clock = pygame.time.Clock()

#game state stuff
game_state = "guessing"

guess_marker = None
answer_marker = None

last_distance = None
last_score = None


#load map
world_map = pygame.image.load("Equirectangular.png")
world_map = pygame.transform.scale(world_map, (WIDTH, HEIGHT))

#convert pixel coordinates to latitude and longitude
def pixel_to_geo(x, y, width, height):
    longitude = (x / width) * 360 - 180
    latitude = 90 - (y / height) * 180
    return latitude, longitude

#lat lon to pixel coordinates
def latlon_to_pixel(lat, lon, width, height):
    x = (lon + 180) / 360 * width
    y = (90 - lat) / 180 * height
    return int(x), int(y)

#loading original random animal data
animal = get_random_animal()
print(animal)

#loading original animal image
animal_image = pygame.image.load(animal["image"])
animal_image = pygame.transform.scale(animal_image, (250,250))

#check distance and score
distance = 0
def check_distance(lat, lon):
    global total_score
    global answer_marker
    global last_distance
    global last_score
    global game_state

    guess = (lat, lon)
    correct = (animal["lat"], animal["lon"])

    distance = geodesic(guess, correct).km
    print("Distance:", distance, "km")

    last_distance = int(distance)

    answer_marker = latlon_to_pixel(
        animal["lat"],
        animal["lon"],
        WIDTH,
        HEIGHT
    )

    score = int(1000 * math.exp(-distance / 1500))

    last_score = score

    total_score += score

    print("Score for this round:", score)

    game_state = "results"

    


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

    # EVENT HANDLING
    for event in pygame.event.get():

        # quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # MOUSE CLICK
        if event.type == pygame.MOUSEBUTTONDOWN:

            # only allow guessing during guessing state
            if game_state == "guessing":

                x, y = pygame.mouse.get_pos()

                print("Clicked:", x, y)

                # store player guess marker
                guess_marker = (x, y)

                # convert click to lat/lon
                lat, lon = pixel_to_geo(
                    x,
                    y,
                    WIDTH,
                    HEIGHT
                )

                print(
                    "Latitude:",
                    lat,
                    "Longitude:",
                    lon
                )

                # calculate score + reveal answer
                check_distance(lat, lon)

        # KEYBOARD INPUT
        if event.type == pygame.KEYDOWN:

            # continue to next animal
            if event.key == pygame.K_SPACE:

                if game_state == "results":

                    # load next animal
                    load_new_animal()
                    while not animal["name"]:
                        load_new_animal()

                    # clear old markers/results
                    guess_marker = None
                    answer_marker = None

                    last_distance = None
                    last_score = None

                    # back to guessing
                    game_state = "guessing"

    # DRAWING

    # draw map
    screen.blit(world_map, (0, 0))

    # draw animal image
    screen.blit(animal_image, (20, 400))

    # font
    font = pygame.font.SysFont(None, 36)

    # animal name
    animal_text = font.render(
        animal["name"],
        True,
        (255,255,255)
    )

    screen.blit(animal_text, (20, 370))

    # total score
    total_score_text = font.render(
        f"Total Score: {total_score}",
        True,
        (255,255,255)
    )

    screen.blit(total_score_text, (20, 320))

    # DRAW PLAYER GUESS
    if guess_marker:

        pygame.draw.circle(
            screen,
            (255,0,0),
            guess_marker,
            6
        )

    # DRAW ACTUAL LOCATION
    if answer_marker:

        pygame.draw.circle(
            screen,
            (0,255,0),
            answer_marker,
            6
        )

    # DRAW LINE BETWEEN THEM

    if guess_marker and answer_marker:

        pygame.draw.line(
            screen,
            (255,255,0),
            guess_marker,
            answer_marker,
            2
        )


    if game_state == "results":

        # distance text
        distance_text = font.render(
            f"Distance: {last_distance} km",
            True,
            (255,255,255)
        )

        screen.blit(distance_text, (20, 20))

        # round score
        round_score_text = font.render(
            f"+{last_score} points",
            True,
            (255,255,0)
        )

        screen.blit(round_score_text, (20, 60))

        # continue prompt
        continue_text = font.render(
            "Press SPACE to continue",
            True,
            (0,0,0)
        )

        screen.blit(continue_text, (20, 100))


    pygame.display.update()

    # frame cap
    clock.tick(60)