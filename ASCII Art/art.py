import pandas
from pyfiglet import Figlet
from termcolor import colored


def main():
    t = input("Enter a text to be converted into ASCII: ")

    print("Color options are")
    print("grey | red | green | yellow | blue | magenta | cyan | white")
    c = input("Choose your color: ")

    print("Font options are")
    print("roman | rectangles | puffy | pepper | pebbles | ogre | ntgreek | moscow")
    x = input("Choose your font: ").lower()

    f = Figlet(font=x)
    print(colored(f.renderText(t), c))

    r = input("Do you want to restart the program? ").lower()
    if r == "yes" or r == "y":
        main()
    else:
        print("See you again")
        exit()


main()
