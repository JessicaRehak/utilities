from typing import Optional

from colorama import Fore, Style


class Color:
    def __init__(self, text: str) -> None:
        self._text = text
        
    def _color(self, color: Fore) -> str:
        return "{}{}{}".format(color, self._text, Style.RESET_ALL)
    
    @property
    def green(self) -> str:
        return self._color(Fore.GREEN)
    
    @property
    def red(self) -> str:
        return self._color(Fore.RED)
    