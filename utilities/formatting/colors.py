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

    def __repr__(self):
        return "Color({})".format(self._text)

    def __str__(self):
        return self._text

class Header(Color):
    def __init__(self, text: str, width: int = 120, symbol: str = "=") -> None:
        super().__init__('{text:{symbol}<{width}}'.format(text=text, symbol=symbol, width=width))    
