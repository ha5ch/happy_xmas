import random
import time
import os
import sys


COLOR = {
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "PURPLE": "\033[0;35m",
    "CYAN": "\033[0;36m",
    "RED": "\033[91m",
    "RESET": "\033[0m",
}

# copied from https://asciiartist.com/christmas-trees-in-ascii-text-art/
TREE = r"""
      \ /
     - * -
      /o\
     /*~~\
    /o~*~o\
   /~o~o~~*\
  /*~~o~*~~*\
 /~o~~*~o~~*~\
/o~*~~o~*~~o~~\
~`~`~`|~|`~`~`~
     |===|
     '___'
""".split(
    "\n"
)
TREE_WIDTH = len(max(TREE, key=len))

# created with https://textkool.com/en/ascii-art-generator
XMAS = """
██╗  ██╗| █████╗ |██████╗ |██████╗ |██╗   ██╗|   |██╗  ██╗|███╗   ███╗| █████╗ |███████╗
██║  ██║|██╔══██╗|██╔══██╗|██╔══██╗|╚██╗ ██╔╝|   |╚██╗██╔╝|████╗ ████║|██╔══██╗|██╔════╝
███████║|███████║|██████╔╝|██████╔╝| ╚████╔╝ |   | ╚███╔╝ |██╔████╔██║|███████║|███████╗
██╔══██║|██╔══██║|██╔═══╝ |██╔═══╝ |  ╚██╔╝  |   | ██╔██╗ |██║╚██╔╝██║|██╔══██║|╚════██║
██║  ██║|██║  ██║|██║     |██║     |   ██║   |   |██╔╝ ██╗|██║ ╚═╝ ██║|██║  ██║|███████║
╚═╝  ╚═╝|╚═╝  ╚═╝|╚═╝     |╚═╝     |   ╚═╝   |   |╚═╝  ╚═╝|╚═╝     ╚═╝|╚═╝  ╚═╝|╚══════╝""".split(
    "\n"
)
XMAS_WIDTH = len(max(XMAS, key=len))

UP = "\x1B[{}A".format(len(TREE) + len(XMAS)) # ANSI code to move upwards
CLR = "\x1B[0K"                               # ANSI code for carriage return ('\r')
END = f"{CLR}\n"


def check_os():
    """need some adjustments when executed on windows"""
    if os.name == "nt":
        from ctypes import windll

        k = windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11), 7)


def coloured(color: str, string: str) -> str:
    return f"{color}{string}{COLOR['RESET']}"


def build_output(lst: list[str], up: str = "", offset: int = 0) -> str:
    lines = [" " * offset + line for line in lst]
    joined = f"{CLR}\n".join(lines)
    output = f"{up}{joined}"
    return output


def color_tree(tree: list[str]) -> list[str]:
    COLORS_BAUBLE = ["RED", "GREEN", "BLUE"]
    COLORS_STAR = ["CYAN", "PURPLE"]
    out = []
    for line in tree:
        new_line = []
        for char in line:
            if char == "o":
                col = COLOR[random.choice(COLORS_BAUBLE)]
                new_line.append(coloured(col, "o"))
            elif char == "*":
                col = COLOR[random.choice(COLORS_STAR)]
                new_line.append(coloured(col, "*"))
            else:
                new_line.append(char)
        out.append("".join(new_line))
    return out


def color_xmas(lst: list[str]) -> list[str]:
    COLORS = ["RED", "GREEN", "BLUE", "CYAN", "PURPLE"]
    random.shuffle(COLORS)
    out = []
    for line in lst:
        new_parts = []
        for idx, part in enumerate(line.split("|")):
            col = COLOR[COLORS[idx % len(COLORS)]]
            new_parts.append(coloured(col, part))
        out.append("".join(new_parts))
    return out


def main():
    check_os()
    print("\n" * len(TREE), "\n" * len(XMAS), sep="") # set up blank lines so cursor moves work
    while True:
        coloured_tree = color_tree(TREE)
        output = build_output(coloured_tree, UP, XMAS_WIDTH // 2 - TREE_WIDTH // 2)
        print(output, end=END)

        coloured_xmas = color_xmas(XMAS)
        output = build_output(coloured_xmas)
        print(output, end=END)

        time.sleep(random.uniform(0.75, 1.5))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        sys.exit(e)
