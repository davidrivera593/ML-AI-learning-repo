from __future__ import annotations

import random
from dataclasses import dataclass

import pygame

from config import (
    FPS,
    HIT_LINE_X,
    HIT_WINDOW_PIXELS,
    NOTE_SPEED,
    NOTE_SPAWN_INTERVAL_SECONDS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


@dataclass
class Note:
    x: float
    y: float


class BeatGame:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Face Beat Game MVP")
        self.clock = pygame.time.Clock()

        self.notes: list[Note] = []
        self.spawn_timer = 0.0
        self.score = 0
        self.running = True

        self.bg_color = (18, 18, 22)
        self.note_color = (99, 102, 241)
        self.hit_line_color = (250, 204, 21)
        self.text_color = (240, 240, 240)

        self.font = pygame.font.SysFont("Segoe UI", 24)

    def _spawn_note(self) -> None:
        y = random.randint(80, WINDOW_HEIGHT - 80)
        self.notes.append(Note(x=WINDOW_WIDTH + 20, y=float(y)))

    def _update_notes(self, dt: float) -> None:
        for note in self.notes:
            note.x -= NOTE_SPEED * dt
        self.notes = [n for n in self.notes if n.x > -40]

    def apply_hit(self) -> bool:
        for index, note in enumerate(self.notes):
            if abs(note.x - HIT_LINE_X) <= HIT_WINDOW_PIXELS:
                self.notes.pop(index)
                self.score += 1
                return True
        return False

    def step(self, dt: float, hit_action: bool) -> None:
        self.spawn_timer += dt
        if self.spawn_timer >= NOTE_SPAWN_INTERVAL_SECONDS:
            self.spawn_timer = 0.0
            self._spawn_note()

        self._update_notes(dt)

        if hit_action:
            self.apply_hit()

        self._render()

    def _render(self) -> None:
        self.screen.fill(self.bg_color)

        pygame.draw.line(
            self.screen,
            self.hit_line_color,
            (HIT_LINE_X, 30),
            (HIT_LINE_X, WINDOW_HEIGHT - 30),
            4,
        )

        for note in self.notes:
            pygame.draw.circle(self.screen, self.note_color, (int(note.x), int(note.y)), 16)

        score_text = self.font.render(f"Score: {self.score}", True, self.text_color)
        self.screen.blit(score_text, (20, 20))

        pygame.display.flip()

    def poll_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def tick(self) -> float:
        return self.clock.tick(FPS) / 1000.0

    def close(self) -> None:
        pygame.quit()
