"""
Start menu: handles main menu and sub-menus
"""

import engine.file_paths as paths
import os
import pygame as pg
import textwrap
from .button import Button, ButtonProperties
from .menus import Menu
from dataclasses import dataclass, field
from engine.events.event_handler import EventHandler
from engine.state_manager import StateManager
from game_window.window import Window, WindowProperties
from pygame.event import pump


class StartMenu():
    # Singleton instance
    __instance = None
    def get_instance():
        if StartMenu.__instance == None:
            StartMenu()
        return StartMenu.__instance

    def __init__(self):
        # Create singleton instance
        if StartMenu.__instance == None:
            StartMenu.__instance = self

        # Grab singleton instances
        self.event_handler = EventHandler.get_instance()
        self.state_manager = StateManager.get_instance()
        self.window = Window.get_instance()

        # Main menu properties
        self.properties = StartMenuProperties()

        self.menus = {
            "MAIN": "MAIN",
            "SP": "SP",
            "HOST": "HOST",
            "JOIN": "JOIN",
            "OPTIONS": "OPTIONS",
            "QUIT": "QUIT",
        }

        # Main menu buttons
        self.buttons = {
            "SP": Button(
                "SINGLE PLAYER",
                lambda: pg.event.post(self.event_handler.create_event("START_MENU", {"MENU_NAME": "SP"})),
                (self.button_coords_from_order(1))
                ),
            "HOST": Button(
                "HOST",
                lambda: self.event_handler.create_event("START_MENU", {"MENU_NAME": "HOST"}),
                (self.button_coords_from_order(2))
                ),
            "JOIN": Button(
                "JOIN",
                self.event_handler.create_event("START_MENU", {"MENU_NAME": "JOIN"}),
                (self.button_coords_from_order(3))
                ),
            "OPTIONS": Button(
                "OPTIONS",
                self.event_handler.create_event("START_MENU", {"MENU_NAME": "OPTIONS"}),
                (self.button_coords_from_order(4))
                ),
            "QUIT": Button(
                "QUIT",
                lambda: pg.event.post(pg.event.Event(pg.QUIT)),
                (self.button_coords_from_order(5))),
        }

        # Title font
        font_file_path = os.path.join(paths.get_font_folder(), "MoNOCOQUE.ttf")
        self.title_font = pg.font.Font(font_file_path, self.properties.title_font_size)

    def button_coords_from_order(self, order_num):
        pos_x = self.window.properties.center_x

        start_y = 4 * self.window.properties.height_unit
        spacing_y = ButtonProperties.height + int(0.75 * self.window.properties.height_unit)
        pos_y = start_y + (order_num - 1) * spacing_y

        return (pos_x, pos_y)

    def start_menu(self, current_event = None):
        """Execute the main menu logic, including calling any sub-menus."""

        # Check if the current event is a start menu change
        if current_event != None:
            if self.event_handler.custom_types["START_MENU"].pygame_id == current_event.type:
                self.window.clear()
                self.draw_start_menu()

        # Update the menu to be the correct one
        self.update_menu(current_event)

    def update_menu(self, current_event):
        """Check the current event against each menu type and display the appropriate one if required."""
        # # Main menu
        self.check_start_menu_buttons()


    def check_buttons(self):
        """Check the current menu state and call the appropriate button check function."""
        if self.state_manager.state == self.state_manager.start_menu["MAIN"]:
            self.check_start_menu_buttons()
            pass
        elif self.state_manager.state == self.state_manager.start_menu["SP"]:
            # TODO: replace with a sub-menu instead of a direct call to start the game
            pass
        elif self.state_manager.state == self.state_manager.start_menu["HOST"]:
            pass
        elif self.state_manager.state == self.state_manager.start_menu["JOIN"]:
            pass
        elif self.state_manager.state == self.state_manager.start_menu["OPTIONS"]:
            pass

    def check_start_menu_buttons(self):
        """Check the start menu buttons and post an event to the queue if pressed."""

        # Draw buttons
        for name, button in self.buttons.items():
            button.check()


    def draw_start_menu(self):
        """Draw the main menu and check for button presses.

        This gets called in a loop and if statements can be used to perform actions once per frame.
        """
        # Blue background
        self.window.display_surface.fill(self.properties.background_color)

        # Game title
        self.draw_title_text()

        # Draw buttons
        for name, button in self.buttons.items():
            button.draw()


    def draw_title_text(self):
        """Draws the title text onto the main menu screen."""
        # TODO: update so that the wrap works with all text by adding words on one by one. "Motherfucker" on a 600x600 will break the current version.
        wrapped_title_text_lines = textwrap.fill(self.properties.title_text, 12).split("\n")
        number_of_lines = len(wrapped_title_text_lines)
        line_height = self.title_font.size(wrapped_title_text_lines[0])[1]

        title_surface = pg.Surface((self.window.properties.width, number_of_lines * line_height))
        black = (0, 0, 0)
        title_surface.fill(black)
        title_surface.set_colorkey(black)

        for line_number, line in enumerate(wrapped_title_text_lines):
            text_surface = self.title_font.render(line, True, self.properties.title_color)

            top_left_x = int(self.window.properties.width/2 - text_surface.get_width()/2)
            top_left_y = line_number * text_surface.get_height()

            title_surface.blit(text_surface, (top_left_x, top_left_y))


        top_left_x = int(self.properties.title_center_x - title_surface.get_width()/2)
        top_left_y = int(self.properties.title_center_y - title_surface.get_height()/2)

        self.window.display_surface.blit(title_surface, (top_left_x, top_left_y))