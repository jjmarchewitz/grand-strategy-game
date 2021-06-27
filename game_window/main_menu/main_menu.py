##########################################################################
# Main menu: handles main menu and sub-menus
##########################################################################

import pygame as pg
import engine.file_paths as paths
from engine.state import State
from game_window.window import Window
from .button import Button

class MainMenu():
    # Singleton instance
    __instance = None
    def get_instance():
        if MainMenu.__instance == None:
            MainMenu()
        return MainMenu.__instance

    def __init__(self):
        # Create singleton instance
        if MainMenu.__instance == None:
            MainMenu.__instance = self

        # Grab singleton instances
        self.state = State.get_instance()
        self.window = Window.get_instance()

        # Main menu properties
        self.properties = {
            "BACKGROUND": (25, 205, 255),
            "TITLE_TEXT": "HALO 2077",
            "TITLE_CENTER_X": self.window.properties["CENTER_X"],
            "TITLE_CENTER_Y": int(1.5*self.window.properties["HEIGHT_UNIT"]),
            "TITLE_FONT_SIZE": int(1.25* self.window.properties["HEIGHT_UNIT"]),
            "TITLE_COLOR": (50, 50, 50),
        }

        # Main menu buttons
        self.buttons = {
            "SP": Button("SINGLE PLAYER", 1),
            "HOST": Button("HOST", 2),
            "JOIN": Button("JOIN", 3),
            "OPTIONS": Button("OPTIONS", 4),
            "QUIT": Button("QUIT", 5),
        }

        # Title font
        font_folder = paths.get_font_folder()
        self.title_font = pg.font.Font(font_folder + "Halo3.ttf", self.properties["TITLE_FONT_SIZE"])

    def main_menu(self):
        """Execute the main menu logic, including calling any sub-menus."""

        self.window.clear()

        # Main menu
        while self.state.main_menu["MAIN"] == self.state.state:
            self.draw_main_menu()

            # Update frame
            self.state.update_game()

        # Options menu
        while self.state.main_menu["OPTIONS"] == self.state.state:
            self.state.update_game()

        # Start a new singleplayer
        while self.state.main_menu["SP"] == self.state.state:
            self.state.update_game()

        # Host a new multiplayer
        while self.state.main_menu["HOST"] == self.state.state:
            self.state.update_game()

        # Join a new multiplayer
        while self.state.main_menu["JOIN"] == self.state.state:
            self.state.update_game()

    def draw_main_menu(self):
        """Draw the main menu and check for button presses.

        This gets called in a loop and if statements can be used to perform actions once per frame.
        """
        # Blue background
        self.window.display_surface.fill(self.properties["BACKGROUND"])

        # Game title
        self.draw_title_text()

        # Draw buttons
        for name, button in self.buttons.items():
            button.draw()

        # Update the state of the game contained in engine/state.py
        self.update_state()


    def draw_title_text(self):
        """Draws the title text onto the main menu screen."""
        text_surface = self.title_font.render(self.properties["TITLE_TEXT"], True, self.properties["TITLE_COLOR"])

        top_left_x = int(self.properties["TITLE_CENTER_X"] - text_surface.get_width()/2)
        top_left_y = int(self.properties["TITLE_CENTER_Y"] - text_surface.get_height()/2)
        self.window.display_surface.blit(text_surface, (top_left_x, top_left_y))

    
    def update_state(self):
        """Update the state of the game contained in engine/state.py."""

        if self.buttons["SP"].is_pressed():
            self.state.update_state(self.state.main_menu["SP"])
        elif self.buttons["HOST"].is_pressed():
            self.state.update_state(self.state.main_menu["HOST"])
        elif self.buttons["JOIN"].is_pressed():
            self.state.update_state(self.state.main_menu["JOIN"])
        elif self.buttons["OPTIONS"].is_pressed():
            self.state.update_state(self.state.main_menu["OPTIONS"])
        elif self.buttons["QUIT"].is_pressed():
            self.state.update_state(self.state.super["QUIT"])


# Singleton instance
menu_obj = None
def get_instance():
    if menu_obj == None:
        menu_obj = Window()
    return menu_obj