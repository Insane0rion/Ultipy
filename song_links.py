from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import lxml
from pathlib import Path
from os import system
from time import sleep
import webbrowser
import subprocess as sb

def clear(): system('clear')

class FileHandler:
    def __init__(self):
        self.urls = []
        self.username = sb.getoutput("whoami")
        self.file_path = f"/home/{self.username}/Music/Ultipy/song_list.txt"
    
    def read_links(self):
        path = Path(self.file_path)
        with open(path, "r") as f:
            for link in f:
                self.urls.append(link)

    def append_links(self, link_list):
        def check_link(link): 
            if link in self.urls: return False
            else: return True
            
        self.read_links()
        path = Path(self.file_path)
        with open(path, "a") as f:
            for link in link_list:
                if check_link(link):
                    f.write(f"\n{link}")

class Song_Links:
    def __init__(self):
        self.root_link = input("Please enter the Ultimate Guitar Artist page!\n"
                               "If there is multpliy pages make sure 'page=' is included in your link! \n\n>")
        self.source : str = None
        self.main()

    def get_source(self, url)-> str:
        
        # Init Driver in Headless mode
        def _init_driver() -> webdriver:
            print("Init driver...")
            options=Options()
            options.headless=True
            driver = webdriver.Firefox(options=options)
            return driver
        
        # Loading Page and getting JS rendered Source
        def getting_source(driver) -> str:
            driver.get(url)
            source = driver.page_source
            driver.quit()
            return source
        
        # Saving Source for Debuggin
        def save_source(source):
            with open("source.txt", 'w') as f:
                for line in source:
                    f.write(line)
        
        driver = _init_driver()
        source = getting_source(driver)
        #save_source(source)
        del driver
        self.source = source
        return source
    
    def get_links(self, source: str)-> list:
        from song_text import Song
        
        # Finding Right Sector to Extracting Links from
        def find_sector(source):
            soup = bs(source, 'lxml')
            first_filter = soup.find_all("article")[2]
            sector = first_filter.find_all("a")
            return sector
        
        # Getting All Links from Sector by removing unnecessary substrings
        def extracting_links(sector) -> list:
            link_list = []
            for link in sector:
                first_split = str(link).split('href="')[1]
                link = first_split.split('"')[0]
                link_list.append(link)
            return link_list
        
        # Filtering Links to just get Song Links
        def filter_links(links: list) -> list:
            song_links = []
            for link in links:
                if "artist" not in link:
                    song_links.append(link)
            return song_links
    
        # Checking if links/songs already in file
        def checking_links_file(new_song_links: list):
            def generating_old_songs():
                file_handler = FileHandler()
                file_handler.read_links()
                urls = file_handler.urls
                del file_handler
                old_songs = [Song(url) for url in urls]
                return old_songs
            
            def generating_new_songs():
                new_songs = [Song(url) for url in new_song_links]
                return new_songs
            
            def compare_song_names(old_songs, new_songs):
                for new_song in new_songs:
                    for old_song in old_songs:
                        if new_song.name == old_song.name:
                            new_songs.remove(new_song)
                return new_songs
            
            old_songs = generating_old_songs()
            uncompared_new_songs = generating_new_songs()
            compared_new_songs = compare_song_names(old_songs, uncompared_new_songs)
            return [song.url for song in compared_new_songs]
            
        # Checking if song has multiply versions and seperating singel and 'double' songs into diffrent lists       
        def get_singel_songs(song_links: list) -> list:
            # Generating List with Song Objects to validate Metadata
            songs = []
            for link in song_links:
                song = Song(link)
                songs.append(song)
            
            # List for sorting the songs
            singel_song_links = []
            rest_songs = []
            # Looping through all Songs and Checking if there is diffrent chords for the same song
            # If no appending to certain list if yes need to check wich song to choose
            for song in songs:
                for other_song in songs:
                    if song.name == other_song.name and song.url != other_song.url:
                        singel = False
                        break
                    else:
                        singel = True
                        pass
                if singel: singel_song_links.append(song.url)
                else: rest_songs.append(song)
            return singel_song_links, rest_songs

        # Check which singel songs do you want to keep
        def check_singels(singel_songs: list) -> list:
            songs = [Song(url) for url in singel_songs]     
            songs_to_keep = []
            for song in songs:
                clear()
                while True:
                    dec=input(f"Do you want to have '{song}' in your libary? (y/n/b)\n\n>").lower()
                    if dec == "y":
                        songs_to_keep.append(song.url)
                        break
                    elif dec == "n":
                        break
                    elif dec == "b":
                        return songs_to_keep
            return songs_to_keep

        # Check if wich version you want to keep
        def checking_doubles(rest_songs: list) -> list:
            # List to check wich songs have been done already
            song_names_already_done = []
            song_versions_to_keep = []
            for song in rest_songs:
                # Checking if already done The Song if not Appending to list and get all Song Objects with same song name
                if song.name not in song_names_already_done:
                    song_names_already_done.append(song.name)
                    same_songs = [song]
                    for other_song in rest_songs:
                        if song.name == other_song.name and song.url != other_song.url:
                            same_songs.append(other_song)
                    clear()
                    while True:
                        dec = input(f"Do you want to have '{song.name}' in your libery? (y/n/b)\n\n>").lower()
                        if dec == "y":
                            clear()                            
							# Opening Firefox Tabs to check wich song gets taken at the end
                            print("Select the version you want to have! If u you dont want the song at all in your libary enter 0!")
                            print(f"Song: {song.name}")
                            v = 1
                            for song in same_songs:
                                webbrowser.get('firefox').open_new_tab(song.url)
                                print(f"Version {v}: {song.url}")
                                v += 1
                            while True:
                                dec = int(input("\n\n>"))
                                if dec == 0:
                                    break
                                if dec >= 1 and int(dec) <= len(same_songs):
                                    dec -= 1
                                    song_versions_to_keep.append(same_songs[dec].url)
                                    break
                                else:
                                    print("Select a displayed version!")
                            break
                        elif dec == "n":
                            break
                        elif dec == "b":
                            return song_versions_to_keep
                    for song in same_songs:
                        rest_songs.remove(song)
            return song_versions_to_keep
        
        
        sector = find_sector(source)
        link_list = extracting_links(sector)
        song_links = filter_links(link_list)
        new_song_links = checking_links_file(song_links)
        singel_songs, rest_songs = get_singel_songs(new_song_links)
        singel_songs_to_keep = check_singels(singel_songs)
        song_versions_to_keep = checking_doubles(rest_songs)
        links_to_keep = singel_songs_to_keep + song_versions_to_keep
        return links_to_keep

    def append_links(self, links: list):
        file_handler = FileHandler()
        file_handler.append_links(links)
        del file_handler

    def main(self,):
        def check_if_multiply_pages():
            numbers = [str(_) for _ in range(10)]
            for number in numbers:
                try:
                    if number in [char for char in self.root_link][48]:
                        return True
                except IndexError:
                    return False
            return False
        def add_page_number(url):
            splitted_url = [char for char in url]
            splitted_url[48] = str(int(splitted_url[48]) + 1)
            return ''.join(splitted_url)

        def check_page(url):
            self.source = self.get_source(url)
            if "Nothing found for" in self.source:
                return False
            else:
                return True
        
        
        if check_if_multiply_pages() is False:
            self.get_source(self.root_link)
            links = self.get_links(self.source)
            self.append_links(links)
        else:
            self.get_source(self.root_link)
            links = self.get_links(self.source)
            self.append_links(links)
            slave_link = self.root_link
            for _ in range(10):
                slave_link = add_page_number(slave_link)
                if check_page(slave_link):
                    links = self.get_links(self.source)
                    self.append_links(links)
                else:
                    break   

class Song_Link:
    def __init__(self):
        self.tmp_link_list = []
        self.main()
        
    def get_link(self):
        while True:
            clear()
            link = input("Enter the link of the song\n\n>") ; clear()
            if link: self.tmp_link_list.append(link); break             
            else: clear
        while True:
            dec = input("Do you want to append another song? (y/n)\n\n>")
            if dec == 'y': self.get_link() 
            else: break

    def append_links(self):
        print("Appending Links...")
        sleep(0.5)
        return FileHandler().append_links(self.tmp_link_list)        

    def main(self):
        self.get_link()
        self.append_links()
        self.tmp_link_list.clear()

def main():
    def print_menu():
        def heading():
            print(f"{' '*54}Song Links\n"
              f"{' '*31}{'-'*55}\n"
              f"{' '*30}| A simple way to append links to your Song-Chords file |\n"
              f"{' '*28}{'-'*61}")
        def console():
            print(f"{' '*27}| 1) Singel Songs{' '*9}2) Artist Page{' '*12}3) Return |\n"
                  f"{' '*28}{'-'*61}")

        clear()
        heading()
        console()
        
        
    
    while True:
        print_menu()
        dec = input(f"{' '*52}>")
        clear()
        if dec == "1":
            song_link = Song_Link()
            del song_link
        elif dec == "2":
            song_links = Song_Links()
            del song_links
        elif dec == "3":
            break



if __name__ == "__main__":
    main()
    print("Goodbye!")
    sleep(1)