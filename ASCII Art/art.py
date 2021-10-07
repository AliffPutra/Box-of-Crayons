from pyfiglet import Figlet
from termcolor import colored

banner = Figlet(font="roman")
print(colored(banner.renderText("All Good, All Ways"), "green"))
