from random import randint
import pygame


def visualize(system):
    pygame.init()

    clock, FPS = pygame.time.Clock(), 30
    WIDTH = 500
    screen = pygame.display.set_mode([WIDTH]*2)
    colors = generate_random_colors(system.empires)
    offset = calculate_offset(system)
    coef = get_normalization_coef_to(system, WIDTH)


    count, loop, running = 0, True, True
    while running:
        screen.fill((255, 255, 255))

        if loop and count > 40:
            loop = event_loop(system)

        if count == 100000:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for empire in system.empires:
            pygame.draw.circle(screen, colors[empire], convert_pos(empire.imperialist.model, offset, coef), 20)
            for colony in empire.colonies:
                pygame.draw.circle(screen, colors[empire], convert_pos(colony.model, offset, coef), 10)

        pygame.display.flip()
        clock.tick(FPS)
        count += 1
    pygame.quit()

def convert_pos(pos, offset, coef):
    return (pos[0] + offset) * coef, (pos[1] + offset) * coef

def generate_random_colors(empires):
    return {empire: [randint(0, 255) for _ in range(3)] for empire in empires}

def calculate_offset(system):
    return -system.countries[0].function.lower_bound

def get_normalization_coef_to(system, width):
    return width / (system.countries[0].function.upper_bound - system.countries[0].function.lower_bound)

def event_loop(system):
    """
    MAIN LOOP
    :return: None
    """
    for empire in system.empires:
        empire.make_assimilation()
        empire.make_revolution()
    system.competition()
    return len(system.empires) > 1
