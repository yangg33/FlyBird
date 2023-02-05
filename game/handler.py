import pygame

from game.constans import JUMP_FORCE, H, SPEED, W, FPS, VELOCITY
from game.history import save_history, get_max_points
from game.models import FlyBird, add_obstacle, DownBird


class Game:
    def __init__(self):
        self.cur_res_font = pygame.font.Font(None, 70)
        self.total_res_font = pygame.font.Font(None, 60)
        self.hint_font = pygame.font.Font(None, 50)

        self.points = 0

        self.clock = pygame.time.Clock()

    def start_game(self, sc, background):
        self.bird = FlyBird([W // 2, H // 2])
        self.ground = H - self.bird.image.get_height() // 2

        self.obstacles = []
        self.obstacles.append(add_obstacle())

        self.gamestart = False
        self.is_jumped = False
        self.is_loose = False
        self.points = 0

        self.sc = sc
        self.background = background

    def events_handler(self):
        move = JUMP_FORCE + VELOCITY
        is_show = 0

        while True:
            is_show += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if (
                        event.key == pygame.K_SPACE
                        and not self.gamestart
                        and not self.is_loose
                    ):
                        self.gamestart = True
                        pygame.time.set_timer(pygame.USEREVENT, 2000)
                    if event.key == pygame.K_SPACE and self.gamestart:
                        self.bird = FlyBird(
                            [self.bird.rect.centerx, self.bird.rect.centery]
                        )
                        move = -JUMP_FORCE
                        self.is_jumped = True
                    if event.key == pygame.K_RETURN and self.is_loose:
                        self.start_game(self.sc, self.background)
                        move = JUMP_FORCE + VELOCITY
                        is_show = 0
                if (
                    event.type == pygame.USEREVENT
                    and self.gamestart
                    and not self.is_loose
                ):
                    self.obstacles.append(add_obstacle())
            if move <= 0:
                self.bird = DownBird([self.bird.rect.centerx, self.bird.rect.centery])
            else:
                self.bird = FlyBird([self.bird.rect.centerx, self.bird.rect.centery])

            if self.is_jumped:
                if 0 <= self.bird.rect.centery + move < self.ground:
                    self.bird.rect.centery += move
                    move += VELOCITY
                elif self.bird.rect.centery + move < 0:
                    self.bird.rect.centery = 0
                    move += VELOCITY
                else:
                    self.bird.rect.centery = self.ground
                    move = JUMP_FORCE + VELOCITY
                    self.is_jumped = False

            self.sc.blit(self.background.image, self.background.rect)

            if self.gamestart:
                for obst1, obst2 in self.obstacles:
                    obst1.rect.centerx -= SPEED
                    obst2.rect.centerx -= SPEED

                    self.sc.blit(obst1.image, obst1.rect)
                    self.sc.blit(obst2.image, obst2.rect)

                while (
                    len(self.obstacles) != 0 and self.obstacles[0][0].rect.centerx < -30
                ):
                    self.points += 1
                    self.obstacles.pop(0)

            for obst1, obst2 in self.obstacles:
                self.sc.blit(obst1.image, obst1.rect)
                self.sc.blit(obst2.image, obst2.rect)
            if self.gamestart:
                tmp_points = 0
                for obst1, obst2 in self.obstacles:
                    if obst1.rect.colliderect(self.bird.rect) or obst2.rect.colliderect(
                        self.bird.rect
                    ):
                        self.gamestart = False
                        self.is_loose = True
                        is_show = 0
                        self.points += tmp_points

                        cur_res = self.cur_res_font.render(
                            f"Результат: {self.points}", True, (0, 0, 0)
                        )
                        res_rect = cur_res.get_rect()
                        res_rect.center = (W // 2, H // 2)
                        self.sc.blit(cur_res, res_rect)

                        save_history(point=self.points)
                        break

                    tmp_points += 1
            if self.is_loose:
                cur_res = self.cur_res_font.render(
                    f"Результат: {self.points}", True, (0, 0, 0)
                )
                res_rect = cur_res.get_rect()
                res_rect.center = (W // 2, H // 2)
                self.sc.blit(cur_res, res_rect)

                if is_show >= 0:
                    hint = self.hint_font.render(
                        f"Чтобы сыграть ещё раз, нажмите на ENTER", True, (50, 50, 50)
                    )
                    hint_rect = cur_res.get_rect()
                    hint_rect.center = (W // 2 - 250, H // 2 - 200)
                    self.sc.blit(hint, hint_rect)
                    if is_show == 30:
                        is_show = -30

            elif not self.gamestart:
                total_res = self.total_res_font.render(
                    f"Рекорд: {get_max_points()}", True, (0, 0, 0)
                )
                total_res_rect = total_res.get_rect()
                total_res_rect.x = 20
                total_res_rect.y = 20
                self.sc.blit(total_res, total_res_rect)

                if is_show >= 0:
                    hint = self.hint_font.render(
                        f"Чтобы продолжить игру, нажмите на ПРОБЕЛ", True, (50, 50, 50)
                    )
                    hint_rect = total_res.get_rect()
                    hint_rect.center = (W // 2 - 250, H // 2 - 200)
                    self.sc.blit(hint, hint_rect)
                    if is_show == 30:
                        is_show = -30

            self.sc.blit(self.bird.image, self.bird.rect)
            pygame.display.update()
            self.clock.tick(FPS)
