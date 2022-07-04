from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.firefox.options import Options
import lxml
from random import choice
import requests
import os
from time import sleep
from subprocess import getoutput
from pathlib import Path


# Class to Prove File and Read Links out of it
class File_Handler:
    def __init__(self):
        self.filename = "song_list.txt"
        self.user = getoutput('whoami')
        self.main_path = f"/home/{self.user}/Music"
        self.check()
        self.read_links()

    # Function to prove existance of Dir and File
    def check(self):
        def check_dir():
            def check_root():
                path = Path(self.main_path)
                if path.is_dir() is False:
                    os.system(f"mkdir {self.main_path}")
                del path
                return

            def check_slave():
                slave_path = f"{self.main_path}/Ultipy"
                path = Path(slave_path)
                if path.is_dir() is False:
                    os.system(f"mkdir {path}")
                del path
                return

            check_root()
            check_slave()

        def check_file():
            path = Path(f"{self.main_path}/Ultipy/{self.filename}")
            try:
                with open(path, "r") as f:
                    return True
            except:
                with open(path, "w") as f:
                    return False

        check_dir()
        if check_file() is False:
            input(
                f"File '{self.filename}' created in folder {self.main_path}/Ultipy....\nPlease make sure to add UltiamteGuitar songs in this file to use the program! ")
            shutdown()
        else:
            return

    def read_links(self):
        path = Path(f"{self.main_path}/Ultipy/{self.filename}")
        with open(f"{path}", "r") as song_list:
            for song in song_list:
                urls.append(song)
            if len(urls) == 0:
                input("There is no links in the file! Please add them and then restart the program!")
                shutdown()

    def del_link(self, links: list):
        path = Path(f"{self.main_path}/Ultipy/{self.filename}")
        new_path = Path(f"{self.main_path}/Ultipy/new_song_list.txt")
        with open(path, "r") as f:
            lines = f.readlines()
        with open(new_path, "w") as nf:
            for line in lines:
                if line in links:
                    pass
                else:
                    nf.write(line)
        os.system(f"rm {path}")
        os.system(f"mv {new_path} {path}")


# Method Class to save song chords into a file
class Song_Saver:
    def __init__(self, song):
        self.artist = song.artist.replace(" ", "_")
        self.user = getoutput('whoami')
        self.song_name = song.name.replace(" ", "_")
        self.song_chords = song.text_and_chords
        self.main_path = f"/home/{self.user}/Music/Ultipy"
        self.check_artist_dict()

    def check_artist_dict(self):
        path = f"{self.main_path}/{self.artist}"
        path = Path(path)
        if path.is_dir() is False:
            os.system(f'mkdir {path}')
            return
        else:
            return

    def check_song_file(self):
        path = Path(f"{self.main_path}/{self.artist}/{self.song_name}.txt")
        if path.is_file() is True:
            return True
        else:
            return False

    def write_song_file(self):
        path = f"{self.main_path}/{self.artist}/{self.song_name}.txt"
        path = Path(path)
        with open(path, "w") as f:
            f.writelines(self.song_chords)

    def read_song_file(self):
        path = Path(f"{self.main_path}/{self.artist}/{self.song_name}.txt")
        with open(path, 'r') as f:
            return f.read()


# Class to init driver and the song text when called
class Song:
    def __init__(self, url):
        self.url = url
        self.artist = None
        self.name = None
        self.text_and_chords = None
        self.get_song_info()

    def get_song_info(self):

        # Functions to get Song Metadata by the provided link
        def get_artist_by_link() -> str:
            try:
                # Filtering Out Artist Name and Replacing - with a Space
                splitted_url = self.url.split("/")
                filtered_artist = splitted_url[4]
                artist_lowered = filtered_artist.replace("-", " ")
                # Splitting Up Artist name to Upper the first letter of each substring
                # After
                artist_to_upper = artist_lowered.split()
                artist_final = []
                for part in artist_to_upper:
                    artist_final.append(part.capitalize())
                artist = ' '.join(artist_final)
                if artist[-1] == " ":
                    artist = artist[:-1]
                return artist

            except:
                print("Link Invalid Format | Artist Name Unkown!")
                return "Unkown"

        def get_song_name_by_link() -> str:
            try:
                splitted_url = self.url.split("/")
                song_raw = splitted_url[5]
                song_splitted = song_raw.split("-")
                for _ in range(2):
                    del song_splitted[-1]
                song_splitted_capped = []
                for part in song_splitted:
                    song_splitted_capped.append(part.capitalize())
                song_name = ' '.join(song_splitted_capped)
                return song_name
            except:
                print("Link Invalid Format | Song Name Unkown!")
                return "Unkown"

        # Functions to get song metadata bt source code
        # Getting Source and Soup and finding all elements of tag meta and get meta to split
        def get_str_to_split() -> str:
            try:
                source = requests.get(self.url).content
                soup = bs(source, 'lxml')
                metas = soup.find_all("meta")
                meta_to_split = metas[2]
                str_to_split = str(meta_to_split).split('"')[1]
                return str_to_split
            except:
                return None

        def get_artist_by_site(str_to_split) -> str:
            if str_to_split is None:
                return "Offline Mode | Couldn't catch artist name"
            artist_name = str_to_split.split("-")[0]
            if artist_name[-1] == " ":
                artist_name = artist_name[:-1]
            return artist_name

        def get_song_by_site(str_to_split) -> str:
            if str_to_split is None:
                return "Offline Mode | Couldn't catch song name"
            first_split = str_to_split.split("-")[1]
            song_name_raw = first_split.split("(")[0]
            substring = [char for char in song_name_raw]
            substring.pop(0)
            substring.pop()
            song_name = ''.join(substring)
            return song_name

        # Checking if HTML source is needed to get song meta data
        def checking(url):
            to_check = self.url.split("/")[4]
            if "-" not in to_check:
                return False
            else:
                return True

        if checking(self.url) is True:
            self.artist = get_artist_by_link()
            self.name = get_song_name_by_link()
        else:
            string_to_split = get_str_to_split()
            self.artist = get_artist_by_site(string_to_split)
            self.name = get_song_by_site(string_to_split)

    def get_text(self):
        # Init webdriver to run headless
        def _init_driver():
            print("Init Driver...")
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
            return driver

        # Get Source of JS Site and deletes driver afterwards
        def get_source(driver, url) -> str:
            print("Getting page source code...")
            driver.get(url)
            html = driver.page_source
            driver.quit()
            return html

        # Function to filter out the Text/Chords of the Song depending of State of Site
        def getting_text(html) -> str:
            print("Filtering text...")
            raw_text = bs(html, "lxml").get_text()
            try:
                first_split = raw_text.split("+5 IQ")
                second_split = first_split[1].split("XBy")
                song_text_and_chords = second_split[0]
            except IndexError:
                first_split = raw_text.split("[Intro]")
                second_split = first_split[1].split("XBy")
                song_text_and_chords = second_split[0]
            if "XShort" in song_text_and_chords:
                song_text_and_chords = song_text_and_chords.split("XShort")[0]
            if "videos" in song_text_and_chords:
                song_text_and_chords = song_text_and_chords.split("videos")[1]
            if "performances" in song_text_and_chords:
                song_text_and_chords = song_text_and_chords.split("performances")[1]
            return song_text_and_chords

        if self.text_and_chords is None:
            if internet_connection is False:
                input("No internet connection!\n Load song in online mode for offline use!")
                mode()
            song_saver = Song_Saver(self)
            if song_saver.check_song_file() is False:
                driver = _init_driver()
                source = get_source(driver, self.url)
                self.text_and_chords = getting_text(source)
                clear()
                song_saver.song_chords = self.text_and_chords
                song_saver.write_song_file()
                return self.text_and_chords
            else:
                self.text_and_chords = song_saver.read_song_file()
        else:
            pass

    def display_song(self):
        print(f"{self.name} by {self.artist}\n")
        input(self.text_and_chords)
        clear()

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


# Class For Libary Mode
class Libary:
    def __init__(self):
        self.all_songs = [Song(url) for url in urls]
        clear()

    def init_dict(self):
        self.song_dict = self.create_song_dict()
        self.artist_tree = self.create_artist_tree()
        self.create_song_trees()

    # Song Dictonary is needed to sort songs by name
    def create_song_dict(self) -> dict:
        song_dict = {}
        for song in self.all_songs:
            song_dict[song.name] = song
        return song_dict

    # Function to create artist dict with key artist name and value an empty list to store the song names
    def create_artist_tree(self) -> dict:
        print("Creating Artist Trees...")
        # Looping through all songs, checking if artist already in list and sorting it at the end
        artist_list = []
        for song in self.song_dict.values():
            artist = song.artist
            if artist not in artist_list:
                artist_list.append(artist)
        artist_list.sort()
        # Creating Artist Dict
        artist_tree = {}
        for artist in artist_list:
            artist_tree[artist] = []
        return artist_tree

    # Function to create song lists for the diffrent artist.
    def create_song_trees(self):
        print("Creating Song Trees...")
        # Getting all song names and sorting them alphabeticly
        songs_sorted = [song_name for song_name in self.song_dict.keys()]
        songs_sorted.sort()
        # Looping through this list and getting the right call instance for it, appending song instances then to artist tree
        i = 1
        m = len(songs_sorted)
        for song in songs_sorted:
            print(f"Loading Libary... ({i}/{m})")
            self.artist_tree[self.song_dict[song].artist].append(self.song_dict[song])
            i += 1

    # Way to complicated functions to display a 2 rowed list of songs in artis tree (w/ multiply pages)
    def choose_artist(self):
        artist_list = [artist for artist in self.artist_tree.keys()]
        # Checking if multiply Pages are needed
        if len(artist_list) <= 8:
            # Displayer in a Row of two
            while True:
                dis_pos = 1
                index_pos = 0
                adder = 0
                print(f"{' ' * 46}Music Libary \n{'-' * 100}")
                for i in range(4):
                    try:
                        whitespace = ' ' * (50 - 2 - len(artist_list[index_pos + adder]))
                        print(
                            f"{dis_pos + adder}) {artist_list[index_pos + adder]}{whitespace}|{' ' * 10}{dis_pos + 1 + adder}) {artist_list[index_pos + 1 + adder]}")
                        adder += 2
                    except IndexError:
                        try:
                            print(f"{dis_pos + adder}) {artist_list[index_pos + adder]}            ")
                            break
                        except IndexError:
                            break

                print("9) Menu")
                dec = input("\n\n>")
                if dec == "9":
                    menu()
                try:
                    choosen = int(dec) - 1
                    artist = artist_list[choosen]
                    return artist
                except:
                    print("Input a displayed number!")
        else:
            # Displaying Multiply Pages in a row of two
            number_of_loops = len(artist_list) / 8
            if number_of_loops % 2 != 0:
                number_of_loops += 1
            chossing = True
            while chossing:
                current_site = 1
                total_sites = int(number_of_loops)
                index_pos = 0
                for site in range(int(number_of_loops)):
                    dis_pos = 1
                    adder = 0
                    print(f"{' ' * 46}Music Libary \n{'-' * 100}")
                    for i in range(4):
                        try:
                            whitespace = ' ' * (50 - 2 - len(artist_list[index_pos + adder]))
                            print(
                                f"{dis_pos + adder}) {artist_list[index_pos + adder]}{whitespace}|{' ' * 23}{dis_pos + 1 + adder}) {artist_list[index_pos + 1 + adder]}")
                            adder += 2
                        except IndexError:
                            try:
                                print(f"{dis_pos + adder}) {artist_list[index_pos + adder]}")
                                break
                            except IndexError:
                                break
                    print(f"9) Menu{' ' * 44}| {' ' * 22}0) Next site")
                    dec = input(f"\n{' ' * 90}(Page:{current_site}/{total_sites})\n>")
                    if dec == "9":
                        menu()
                    elif dec == "0":
                        clear()
                        index_pos += 9
                        current_site += 1
                        if current_site > total_sites:
                            current_site = 1
                            index_pos = 0
                    else:
                        try:
                            choosen = int(dec) + index_pos - 1
                            artist = artist_list[choosen]
                            return artist
                        except:
                            print("Input a displayed number!")
            return None

    def choose_song(self, chossen_artist):
        clear()
        song_list = [song for song in self.artist_tree[chossen_artist]]
        if len(song_list) <= 8:
            to_add = 0
            print(f"{' ' * (50 - int(len(chossen_artist) / 2))}{chossen_artist}\n{'-' * 90}")
            for _ in range(4):
                dis_pos = 1
                try:
                    whitespace = ' ' * (50 - 2 - len(song_list[0 + to_add].name))
                    print(
                        f"{dis_pos + to_add}) {song_list[0 + to_add]}{whitespace}| {dis_pos + 1 + to_add}) {song_list[0 + 1 + to_add]}")
                    to_add += 2
                except IndexError:
                    try:
                        print(f"{dis_pos + to_add}) {song_list[0 + to_add]}")
                        to_add += 1
                    except IndexError:
                        break
            print("9) Artists")
            while True:
                song_dec = input("\n\n>")
                if song_dec == "9":
                    self.Chosse()
                else:
                    try:
                        song_dec = int(song_dec) - 1
                        return song_list[song_dec]
                    except IndexError:
                        print("Please enter a displayed number!")

        else:
            number_of_loops = len(song_list) / 8
            if number_of_loops % 2 != 0:
                number_of_loops += 1
            chossing = True
            while chossing:
                current_site = 1
                total_sites = int(number_of_loops)
                index_pos = 0
                for site in range(int(number_of_loops)):
                    dis_pos = 1
                    adder = 0
                    print(f"{' ' * (70 - len(chossen_artist))}{chossen_artist}\n{'-' * 100}")
                    for i in range(4):
                        try:
                            whitespace = ' ' * (50 - 2 - len(song_list[index_pos + adder].name))
                            print(
                                f"{dis_pos + adder}) {song_list[index_pos + adder]}{whitespace}| {dis_pos + 1 + adder}) {song_list[index_pos + 1 + adder]}")
                            adder += 2
                        except IndexError:
                            try:
                                print(f"{dis_pos + adder}) {song_list[index_pos + adder]}")
                                break
                            except IndexError:
                                break
                    print(f"9) Artists{' ' * 42}| 0) Next site")
                    Dec = True
                    while Dec:
                        dec = input(f"\n{' ' * 90}(Page:{current_site}/{total_sites})\n>")
                        if dec == "9":
                            self.Chosse()
                        elif dec == "0":
                            current_site += 1
                            index_pos += 8
                            clear()
                            break
                        else:
                            try:
                                dec = int(dec) - 1
                                return song_list[dec + index_pos]

                            except:
                                print("Please enter a displayed number!")

    # Main Function to Choose Songs from Libary
    def Chosse(self):
        clear()
        artist = self.choose_artist()
        song = self.choose_song(artist)
        clear()
        song.get_text()
        song.display_song()
        self.Chosse()

    # Func for Random mode
    def random_mode(self):
        clear()
        already_took = []
        while True:
            # Checking if all songs been go through
            if len(urls) == len(already_took):
                clear()
                print("Unfortunatly you got no more songs to play! Going to main menu!")
                sleep(2)
                menu()
            # Getting Random URL and asking for display
            url = choice(urls)
            if url not in already_took:
                # Appending URL to already took to check to avoid doubled display
                already_took.append(url)
                song = Song(url)
                song.get_song_info()
                print("You are in the random mode, but you can always enter (m)enu to go to the main menu!\n\n ")
                dec = input(
                    f"If you want to play '{song}' by {song.artist} enter anything, if not just hit enter!\n\n>").lower()
                # Checking if input was given and if cointins m or menu its going to the main menu
                # Other whise getting song info and printing it
                if len(dec) != 0:
                    if [char for char in dec][0] == "m":
                        clear()
                        menu()
                    else:
                        clear()
                        song.get_text()
                        print(f"'{song.name}' by {song.artist}")
                        input(song.text_and_chords)
                        clear()
                        pass
                else:
                    clear()
                    pass

    # Function To Update Libary -> Saving all Texts and Chords in the Filesystem
    def get_all_texts(self):
        faulty_links = []
        i = 1
        m = len(libary.all_songs)
        for song in libary.all_songs:
            try:
                print("loading and saving All Songs...")
                print(f"({i}/{m})")
                song.get_text()
                i += 1
                clear()
            except:
                faulty_links.append(song.url)
        print("No more Songs to Load...\n\nFaulty Songs:")
        input([url for url in faulty_links])
        if len(faulty_links) != 0:
            while True:
                dec = input("Do you want to remove the faulty links? (y/n)").lower()
                if dec == "y":
                    fh.del_link(faulty_links)
                    break
                elif dec == "n":
                    break
        menu()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_internet_connection():
    print("Checking Network Connection...")
    try:
        _ = requests.head("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def welcome_screen():
    return print(f"{' ' * 47}--------------\n"
                 f"{' ' * 46}-- Welcome to --\n"
                 f"{' ' * 46}----------------\n"
                 f"{' ' * 46} --- Ultipy ---\n"
                 f"{' ' * 46}---------------- v.1.3.1\n"
                 f"{' ' * 32} -----------------------------------------\n"
                 f"{' ' * 32}| A simple webscraper for ultimate guitar!|\n"
                 f"{' ' * 24} -----------------------------------------------------------")


def menu():
    mode = menu
    clear()
    welcome_screen()
    if internet_connection is False:
        print(f"{' ' * 24}| 1) Random mode 2) Libary mode 3) Save All chords 4) Quit  (Offline Mode!)")
    else:
        print(f"{' ' * 24}| 1) Random mode 2) Libary mode 3) Save all chords  4) Quit |")
    print(f"{' ' * 25}{'-' * 59}")
    while True:
        dec = input(f"{' ' * 50}>")
        if dec == "1":
            mode = libary.random_mode
            libary.random_mode()
        elif dec == "2":
            clear()
            mode = libary
            libary.Chosse()
            main()
        elif dec == "3":
            libary.get_all_texts()
        elif dec == "4":
            quit()


def shutdown():
    clear()
    print("Goodbye!")
    sleep(2)
    clear()
    quit()


def main():
    # List to Store Links red out of File
    global urls, libary, internet_connection, mode, fh
    internet_connection = check_internet_connection()
    urls = []
    clear()
    print("Loading Libary....")
    fh = File_Handler()
    libary = Libary()
    libary.init_dict()
    clear()
    menu()


if __name__ == '__main__':
    main()
