import song_links
import song_text


def main_menu():
    while True:
        song_text.welcome_screen()
        print(f"{' ' * 32}| 1) Song Texts 2) Libary Appender 3) Quit|")
        print(f"{' ' * 33}{'-' * 41}")
        dec = input(f"{' ' * 50}>")
        if dec == '1':
            song_text.main()
        elif dec == '2':
            song_links.main()
        elif dec == '3':
            quit()
        else:
            song_text.clear()


if __name__ == "__main__":
    main_menu()
