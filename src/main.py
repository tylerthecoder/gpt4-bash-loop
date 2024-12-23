import sys
from shell import main as shell_main
from clip import main as clip_main


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "clip":
        clip_main()
    else:
        shell_main()



