"""
Start menu: handles main menu and sub-menus
"""

from engine.state_manager import StateManager
import engine.file_paths as paths
import pygame as pg
import os
import textwrap
from .button import Button, ButtonProperties
from dataclasses import dataclass
from engine.events.event_handler import EventHandler
from game_window.window import Window

class Menu():
    """Base class for all menus"""

    def __init__(self):
        """Construct a Menu object."""
        self.buttons = {}
        self.event_handler = EventHandler.get_instance()
        self.state_manager = StateManager.get_instance()
        self.window = Window.get_instance()

    def draw(self):
        """Draw the menu."""
        for _, value in self.buttons.items():
            value.draw()
        
    def add_button(self, name, button):
        """Add a button to the menu to be drawn."""
        self.buttons.update({name: button})
        
    def check(self):
        """Check all buttons for being pressed and run their functions if needed."""
        for _, value in self.buttons.items():
            value.check()
    

@dataclass
class MainMenuProperties():
    """Properties of the Main Menu"""
    window = Window.get_instance()
    background_color: tuple[int, int, int] = (25, 205, 255)
    title_text: str = "GEARS OF HALO THEFT AUTO 5"
    title_color: tuple[int, int, int] = (50, 50, 50)
    title_center_x: int = window.properties.center_x
    title_center_y: int = int(1.875*window.properties.height_unit)
    title_font_size: int = int(1.15*window.properties.height_unit)
    
class MainMenu(Menu):
    """The game's main menu, the first screen that can be interacted with after launch."""

    def __init__(self):
        """Construct a MainMenu object"""
        super().__init__()
        self.properties = MainMenuProperties()
        
        self.add_button(
            "SP",
            Button(
                "SINGLE PLAYER",
                lambda: self.event_handler.create_and_push_state_event(self.state_manager.launch_menu["SP"]),
                (self.button_coords_from_order(1))
                )
            )
        self.add_button(
            "HOST",
            Button(
                "HOST",
                lambda: self.event_handler.create_and_push_state_event(self.state_manager.launch_menu["HOST"]),
                (self.button_coords_from_order(2))
            )
        )
        self.add_button(
            "JOIN",
            Button(
                "JOIN",
                lambda: self.event_handler.create_and_push_state_event(self.state_manager.launch_menu["JOIN"]),
                (self.button_coords_from_order(3))
            )
        )
        self.add_button(
            "OPTIONS",
            Button(
                "OPTIONS",
                lambda: self.event_handler.create_and_push_state_event(self.state_manager.launch_menu["OPTIONS"]),
                (self.button_coords_from_order(4))
            )
        )
        self.add_button(
            "QUIT",
            Button(
                "QUIT",
                lambda: pg.event.post(pg.event.Event(pg.QUIT)),
                (self.button_coords_from_order(5))
            )
        )
        
    def button_coords_from_order(self, order_num):
        """Get coordinates for the main menu buttons from their order."""
        pos_x = self.window.properties.center_x

        start_y = 4 * self.window.properties.height_unit
        spacing_y = ButtonProperties.height + int(0.75 * self.window.properties.height_unit)
        pos_y = start_y + (order_num - 1) * spacing_y

        return (pos_x, pos_y)
    
    def draw(self):
        """Draw the main menu."""
        # Blue background
        self.window.display_surface.fill(self.properties.background_color)
        self.draw_title()
        super().draw()
        
    def draw_title(self):
        """Draw the main menu title."""
        # Title font
        font_file_path = os.path.join(paths.get_font_folder(), "MoNOCOQUE.ttf")
        title_font = pg.font.Font(font_file_path, self.properties.title_font_size)
        
        # TODO: update so that the wrap works with all text by adding words on one by one. "Motherfucker" on a 600x600 will break the current version.
        wrapped_title_text_lines = textwrap.fill(self.properties.title_text, 12).split("\n")
        number_of_lines = len(wrapped_title_text_lines)
        line_height = title_font.size(wrapped_title_text_lines[0])[1]

        # Create and fill the title surface
        title_surface = pg.Surface((self.window.properties.width, number_of_lines * line_height))
        black = (0, 0, 0)
        title_surface.fill(black)
        title_surface.set_colorkey(black)

        for line_number, line in enumerate(wrapped_title_text_lines):
            text_surface = title_font.render(line, True, self.properties.title_color)

            top_left_x = int(self.window.properties.width/2 - text_surface.get_width()/2)
            top_left_y = line_number * text_surface.get_height()

            title_surface.blit(text_surface, (top_left_x, top_left_y))


        top_left_x = int(self.properties.title_center_x - title_surface.get_width()/2)
        top_left_y = int(self.properties.title_center_y - title_surface.get_height()/2)

        self.window.display_surface.blit(title_surface, (top_left_x, top_left_y))
        

@dataclass
class DummyMenuProperties():
    window = Window.get_instance()
    background_color: tuple[int, int, int] = (100, 100, 100)
    title_text: str = "Dummy Menu"
    title_color: tuple[int, int, int] = (50, 50, 50)
    title_center_x: int = window.properties.center_x
    title_center_y: int = int(1.875*window.properties.height_unit)
    title_font_size: int = int(1.15*window.properties.height_unit)

class DummyMenu(Menu):
    """Dummy menu to test functionality."""
    
    def __init__(self):
        super().__init__()
        self.properties = DummyMenuProperties()
        
        self.add_button(
            "EXIT_TO_MAIN",
            Button(
                "BACK TO MAIN",
                lambda: self.event_handler.create_and_push_state_event(self.state_manager.launch_menu["MAIN_MENU"]),
                (self.window.properties.center_x, self.window.properties.center_y)
            )
        )
        
    def draw(self):
        """Draw the dummy menu."""
        # Fill background
        self.window.display_surface.fill(self.properties.background_color)
        super().draw()
