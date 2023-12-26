import os, keyboard, pygame, time, math, random
from colored import attr, bg, fg

r, y, g, bl, blue, w, reset, bold, gray, cyan, red2, g2  = fg(196), fg(226), fg(2), fg(21), fg(39), fg(255), attr('reset'), attr(1), "\033[90m" , "\033[96m", fg(204), fg(35)
t, x, tab ="\t"*5 +"   ", "▬", "\t" *7
line = "\n" *10  
tabf = "\t" *5
tab_lines = "\t" *5 + "         " 
tab3, tab4 = "\t" *4 , "\t" *4 +  " " *7
printed_song_count_4queue, bar_sec_4SongList, highlighted_line_count, instruction_counter, printed_instruction = 0, 0, 0, 0, 0
chosen_category, paused, current_song, first_run = None, False, "", True
currently_hovered_4queue, current_page, currently_hovered_4songList = -1, 1, 0

class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def get_elements(self):
        curr_node = self.head
        elements = []
        while curr_node:
            elements.append(curr_node.value)
            curr_node = curr_node.next_node
        return elements

    def append(self, value):
        if not self.head:
            self.head = Node(value, None)
            return

        curr_node = self.head
        while curr_node.next_node:
            curr_node = curr_node.next_node
        curr_node.next_node = Node(value, None)
                
    def extend(self, values):
        for value in values:
            self.append(value)

    def remove(self, value = None, remove_all = False):
        if remove_all:
            self.head = None
            return 
        curr_node = self.head
        if curr_node.value == value:
            self.head = curr_node.next_node
            curr_node = None
            return
        while curr_node:
            if curr_node.value == value:
                break
            previous_node = curr_node
            curr_node = curr_node.next_node
        previous_node.next_node = curr_node.next_node
        curr_node = None    

    def get_length(self):
        length = 0
        curr_node = self.head
        while curr_node:
            length+=1
            curr_node = curr_node.next_node
        return length

    def has(self, value):
        curr_node = self.head
        for _ in range(self.get_length()):
            if curr_node.value == value:
                return True
            curr_node = curr_node.next_node
        return False

    def shuffle(self):
        songs = self.get_elements()
        random.shuffle(songs)
        self.head = None
        self.append(songs.pop(songs.index(current_song)))
        for song in songs:
            self.append(song)

class SongList:
    def __init__(self) -> None:
        global border_color, icon_color, playing_color, title_color, buttons_color, bar_color, volume, thin_line, sec_color, artist_color, queue_color
        self.song_list = get_songs(chosen_category)
        self.header ="           {}{}  {}{}{}{}\n".format(w, tab, f'{"  #": <12}', f'{"  𝐀 𝐑 𝐓 𝐈 𝐒 𝐓": <24}', f'{"   𝐓 𝐈 𝐓 𝐋 𝐄": <25}', "   𝐆 𝐄 𝐍 𝐑 𝐄")
        if chosen_category == "Korea":
            if default_theme:   
                border_color, icon_color, playing_color, title_color, buttons_color, bar_color, volume, thin_line, sec_color, artist_color = g, w, g, w, w, g, g, gray + "─"*200, w, w
                self.first, self.second, self.third, self.title_left_line, self.title_right_line, self.selected_color, self.left_lcolor, self.right_lcolor = g, g, w, g, w, g, w, w
            else:       
                artist_color, title_color, border_color, icon_color, playing_color, title_color, buttons_color, bar_color, volume, thin_line, sec_color, queue_color = w, w, blue, w, blue, w, w, blue, blue, gray + "─"*200, w, w
                self.first, self.second, self.third, self.title_left_line, self.title_right_line, self.selected_color, self.left_lcolor, self.right_lcolor  = r, w, blue, r, blue, blue, blue, r
            self.title = f"""
    {tab}\t\t{self.first}             █▄▀ {self.second}█▀█ {self.third}█▀█ {self.first}█▀▀ {self.second}▄▀█ {self.third}█▄░█   {self.first}█▀▄▀█ {self.second}█░█ {self.third}█▀ {self.first}█ {self.second}█▀▀
    {tab}\t\t{self.first}             █░█ {self.second}█▄█ {self.third}█▀▄ {self.first}██▄ {self.second}█▀█ {self.third}█░▀█   {self.first}█░▀░█ {self.second}█▄█ {self.third}▄█ {self.first}█ {self.second}█▄▄\n
    {tabf}\t        {self.title_left_line} {"━"*52}{self.title_right_line}{"━"*52}\n\n"""
            self.header ="         {}{}  {}{}{}{}\n".format(w, tab, f'{"  #": <13}', f'{" 𝐀 𝐑 𝐓 𝐈 𝐒 𝐓": <24}', f'{"  𝐓 𝐈 𝐓 𝐋 𝐄": <26}', " 𝐆 𝐄 𝐍 𝐑 𝐄")
        elif chosen_category == "Japan":
            if default_theme:   
                border_color, icon_color, playing_color, title_color, buttons_color, bar_color, volume, thin_line, sec_color, artist_color = g, w, g, w, w, g, g, gray + "─"*200, w, w
                self.first, self.second, self.title_left_line, self.title_right_line, self.selected_color, self.left_lcolor, self.right_lcolor  = g, w, g, w, g, w, w
            else:
                artist_color, border_color, icon_color, playing_color, title_color, buttons_color, bar_color, volume, thin_line, sec_color, queue_color = w, r, w, r, w, fg(160), w, r, gray + "─"*200, w, ""             
                self.first, self.second, self.title_left_line, self.title_right_line, self.selected_color, self.left_lcolor, self.right_lcolor  = r, w, r, w, r, w, r
            self.title = f"""
    {tab}\t                 {self.first}░░█ {self.second}▄▀█ {self.first}█▀█ {self.second}▄▀█ {self.first}█▄░█ {self.second}█▀▀ {self.first}█▀ {self.second}█▀▀   {self.first}█▀▄▀█ {self.second}█░█ {self.first}█▀ {self.second}█ {self.first}█▀▀
    {tab}\t                 {self.first}█▄█ {self.second}█▀█ {self.first}█▀▀ {self.second}█▀█ {self.first}█░▀█ {self.second}██▄ {self.first}▄█ {self.second}██▄   {self.first}█░▀░█ {self.second}█▄█ {self.first}▄█ {self.second}█ {self.first}█▄▄\n
    {tabf}\t           {self.title_left_line}{"━"*50}{self.title_right_line}{"━"*50}\n\n"""
        elif chosen_category == "PH":
            if default_theme:   
                self.first, self.second, self.third, self.fourth, self.title_left_line, self.title_right_line, self.selected_color, self.left_lcolor, self.right_lcolor = g, w, g, w, g, w, g, w, w
                border_color, icon_color, playing_color, title_color, buttons_color, bar_color, volume, thin_line, sec_color, artist_color = g, w, g, w, w, g, g, gray + "─"*200, w, w
            else:               
                self.first, self.second, self.third, self.fourth, self.title_left_line, self.title_right_line, self.selected_color, self.left_lcolor, self.right_lcolor = bl, y, w, r, r, bl, y, bl, r 
                artist_color, title_color, buttons_color, border_color, icon_color, sec_color, thin_line, queue_color, playing_color, volume, bar_color = fg(196), blue, blue, w, y, fg(196), fg(11) + "─"*200, fg(11), blue, blue, fg(196)
            self.title = f"""
    {tab}\t\t                 {self.first}█▀█ {self.second}█ {self.third}█▄░█ {self.fourth}█▀█ {self.first}█▄█   {self.second}█▀▄▀█ {self.third}█░█ {self.fourth}█▀ {self.first}█ {self.second}█▀▀
    {tab}\t\t                 {self.first}█▀▀ {self.second}█ {self.third}█░▀█ {self.fourth}█▄█ {self.first}░█░   {self.second}█░▀░█ {self.third}█▄█ {self.fourth}▄█ {self.first}█ {self.second}█▄▄\n
    {tabf}\t             {self.title_left_line}{"━"*50}{self.title_right_line}{"━"*50}\n\n"""
        else:
            border_color, icon_color, playing_color, title_color, buttons_color, bar_color, volume, thin_line, sec_color, artist_color, queue_color = g, w, g, w, w, g, g, gray + "─"*200, w, w, ""
            self.selected_color, self.left_lcolor, self.right_lcolor = g, w, w
            self.title  = f"""{g}
{tabf}\t\t               ⣠⣾⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀                                                              ⣠⣴⣾⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀
{tabf}\t\t            ⢀⣰⣿ {w}B A C K{g} ⣿⣿⠀                                                             ⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀
{tabf}\t\t            ⠋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀                                                            ⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀  ⡆⢀⣾⣋
{tabf}\t\t             ⣿⣿⢥      ⡿⣿⣿⡏              ▄▀█ {w}█░░ {g}█░░   {w}█▀ {g}█▀█ {w}█▄░█ {g}█▀▀ {w}█▀       {g}        ⢸⣿  {w}N E X T{g} ⣿⣿⠁⠀⠀ ⢸⣿⣿⣿⠟⠀⠀
{tabf}{g}\t\t   ⣤⢀⣀⠀⠀⠀⠀⠀⠀⠀⠘⠏⢇      ⢹⣿⡟⠀⠀             █▀█ {w}█▄▄ {g}█▄▄   {w}▄█ {g}█▄█ {w}█░▀█ {g}█▄█ {w}▄█ {g}              ⢘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⣀⡀⠀⣰⣿⣿⡿⠁⠀⠀
{tabf}{g}\t\t    ⣻⣻⣌⠐⡄⠀ ⢤ ⠤ ⢸⣗⣠⣈⣠⣴⣇⣻⣧⠀⠀⠀⠀⠀⠀⠀                                                         ⠏⢿⣿⣿⣧⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀
{tabf}{g}\t\t     ⠉⠉⢄⠈⢄⠀ ⢈⡀ ⠈⢤⣏⣿⢛⣿⣿⣀⢀⣰⣄                                                             ⠀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠉⠉
{tabf}{g}\t\t        ⢂⠀⠑⠔⢣⣠⣭⣧⡀⠻⣿⡟⡋⠉⠁⠉⣺⣿⣷                                                             ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
{tabf}\t            {g}{"━"*50}{w}{"━"*50}                                                                                                                                                                                                                                               
"""
    
    def to_asci_art(self, song_code: str) -> str:
        fonts= [["█▀▀█", "█▄▀█", "█▄▄█"],["▄█░", "░█░", "▄█▄"], ["█▀█", "░▄▀", "█▄▄"], ["█▀▀█", "░░▀▄", "█▄▄█"],
       ["░█▀█░", "█▄▄█▄", "░░░█░"], ["█▀▀", "▀▀▄", "▄▄▀"], ["▄▀▀▄","█▄▄░", "▀▄▄▀"], ["▀▀▀█", "░░█░", "░▐▌"],
       ["▄▀▀▄", "▄▀▀▄", "▀▄▄▀"], ["▄▀▀▄", "▀▄▄█", "░▄▄▀"]]
        converted_song_code = []
        for number in song_code:
            for i in range(10):
                if str(i) == number:
                    converted_song_code.append(fonts[i])

        fi, s, t, fo, fif = converted_song_code[0], converted_song_code[1], converted_song_code[2],converted_song_code[3],converted_song_code[4]
        code = f'''{self.selected_color}
{tab}\t\t\t                {fi[0]}  {s[0]}  {t[0]}  {fo[0]}  {fif[0]}
{tabf}\t          {self.left_lcolor}{f"━"*35}   {self.selected_color}{fi[1]}  {s[1]}  {t[1]}  {fo[1]}  {fif[1]}   {self.right_lcolor}{f"━"*35}{self.selected_color}
{tab}\t\t\t                {fi[2]}  {s[2]}  {t[2]}  {fo[2]}  {fif[2]}
'''
        return code

    def display_songList_page(self, currently_hovered_4songList = 0, currently_hovered_4queue=-1, song_code="00000"):
        os.system('cls')
        print(self.title,self.header)
        i = 0
        for song in self.song_list[int(f"{current_page-1}0") : int(f"{current_page}0")]:
            print(reset+"{}".format(self.selected_color if i == currently_hovered_4songList else "")+"\t"+song+reset)
            i+=1
        print(self.to_asci_art(song_code))
        if song_queue.get_length():
            print(f'{w}{tab_lines}            𝐒 𝐎 𝐍 𝐆   𝐐 𝐔 𝐄 𝐔 𝐄 {reset}{self.selected_color}\n             {tab_lines}{" ╔═"+"══"*50+"╗"}\n{reset}')
            for i in range(song_queue.get_length()):
                print("          {}".format(self.selected_color if i == currently_hovered_4queue else "")+f"{song_queue.get_elements()[i].rstrip()}{reset}")
                if i == 9:
                    break
            print("\n"+f'             {tab_lines}{self.selected_color}{" ╚═"+"══"*50+"╝"}' )

def colorText(text): #for text file coloring
    lis = {"white":"\033[1;30;0m","blue":"\033[0;34m","yellow":"\33[93m","red":"\u001b[31;1m","green":"\033[32m","reset":"\033[0m"}
    for color in lis:
        text = text.replace("[[" + color + "]]", lis[color])
    return text

def display_theme_choices_or_thanksMessage(path = "Menu resources/Exit_Thanks.txt"): 
    os.system("cls")
    if path != "Menu resources/Exit_Thanks.txt":    
        print(title)
    with open(path, encoding='UTF-8') as file:
        for line in file:
            asci = ''.join(line)
            print(colorText(asci.rstrip()))
    if path == "Menu resources/Exit_Thanks.txt":
        print(reset)
        time.sleep(2)
        keyboard.press("x")
        os._exit(0)

def display_main_menu():
    global song_queue, default_theme, currently_hovered_4queue,currently_hovered_4songList, current_page, title, first_run
    currently_hovered_4songList, currently_hovered_4queue, current_page, default_theme, song_queue = 0, -1, 1, False, LinkedList()
    r, y, b, w, reset  = fg(196), fg(226), fg(21), fg(255), attr('reset') #random colorsa
    gr, light_g, blue_gr, turquoise = fg(35), fg(2), fg(29), fg(36) #green color palette
    bar_blue, bar_red, bar_yellow, gray = fg(69), fg(1), fg(3), fg(15) #musical notes and bar colors
    wr = fg(255) + attr(7)
    reset, white, white_hl, red, yellow, blue, green = "\033[0m", "\033[1;30;0m", "\33[47m", "\u001b[31;1m", "\33[93m", "\033[0;34m", "\033[32m" #unicode songbooks colors
    tab = "\t" *3
    title = f"""\n\n\n
{tab}                                                                                                      {gr} ▄▄{reset}                                                    
{tab}                                                 {gr}█████            █████{reset}                              {gr} █{reset}     {gr}███████████{reset}    
{tab}                                                 {gr}███████        ███████{reset}                             {turquoise}███{reset}   {gr}████       ████{reset}             {bar_red}|\  
{tab}           {bar_blue}____|\_______________|\\_____________  {gr}████ ████    ████ ████{reset}                                   {gr}████       ████{reset}  {bar_blue}___|_______|_____`___|_____|___|__________                  
{tab}           {bar_red}____|/___3_|________@'_\|__|_____|__  {gr}████  ████  ████  ████{reset}    {turquoise}████    ████{reset}   {gr}███████{reset}   {turquoise}███{reset}   {gr}████       ████{reset}  {bar_red}___|___|___|_____|___|_|__@'___|___|___|__  
{tab}           {bar_yellow}___/|______|____________|__|_____|__  {gr}████    ██████    ████{reset}    {turquoise}████    ████{reset}   {gr}███    {reset}   {turquoise}███{reset}   {gr}████       ████{reset}  {bar_yellow}__@'___|__@'____@'___|_|______@'___|___|__
{tab}           {w}__|_/_\__4_|___|_______@'__|____O'__  {turquoise}████     ████     ████{reset}    {gr}████    ████{reset}   {gr}███████{reset}   {gr}███{reset}   {turquoise}████       ████{reset}  {w}_______|____________O'_|__________@'___|__             
{tab}           {bar_blue}___\|/_____|___|___________|________  {turquoise}████              ████{reset}    {gr}████    ████{reset}   {turquoise}    ███{reset}   {gr}███{reset}   {turquoise}████  ▄▄▄  ████{reset}  {bar_blue}_______|_______________|_______________|__
{tab}           {bar_red}    |         O'                      {turquoise}████              ████{reset}    {gr}  ████████  {reset}   {turquoise}███████{reset}   {gr}███{reset}   {turquoise}  ███████████  {reset}                                                                                                                                                                                                                           {turquoise}▀▀▀{reset}
    """
    back = f'''    
    {tab}           {bar_yellow}________________{bar_blue}_________________{bar_red}_________________{gr}_________________  █▄▄ {gray}▄▀█ {gr}█▀▀ █▄▀  _________________{bar_red}_________________{bar_blue}_________________{bar_yellow}_________________
    {tab}                                                                                {turquoise}█▄█ {gray}█▀█ {turquoise}█▄▄ █░█'''

    green_bars = ['Menu resources/green_bar1.txt', 'Menu resources/green_bar2.txt', 'Menu resources/green_bar3.txt', 'Menu resources/green_bar4.txt'] #DEFAULT BAR animation
    ALL_Book = ["Menu resources/ALL_Close_Book.txt", "Menu resources/ALL_Open_Book.txt"] #ALL BOOK animation
    pinoy_bars = ['Menu resources/pinoy_bar1.txt', 'Menu resources/pinoy_bar2.txt', 'Menu resources/pinoy_bar3.txt', 'Menu resources/pinoy_bar4.txt'] #PINOY BAR animation
    PH_Book = ["Menu resources/PH_Close_Book.txt", "Menu resources/PH_Open_Book.txt"] #PINOY BOOK animation
    PH_Green_Book = ["Menu resources/PH_Close_GreenBook.txt", "Menu resources/PH_Open_GreenBook.txt"] #PINOY GREEN BOOK animation
    JP_Book = ["Menu resources/JP_Close_Book.txt", "Menu resources/JP_Open_Book.txt"] #JAPAN BOOK animation
    JP_Green_Book = ["Menu resources/JP_Close_GreenBook.txt", "Menu resources/JP_Open_GreenBook.txt"] #JAPAN GREEN BOOK animation
    KR_Book = ["Menu resources/KR_Close_Book.txt", "Menu resources/KR_Open_Book.txt"] #KOREAN BOOK animation
    KR_Green_Book = ["Menu resources/KR_Close_GreenBook.txt", "Menu resources/KR_Open_GreenBook.txt"] #KOREAN GREEN BOOK animation
    japan_bars = ['Menu resources/japan_bar1.txt', 'Menu resources/japan_bar2.txt', 'Menu resources/japan_bar3.txt', 'Menu resources/japan_bar4.txt'] #JAPAN BAR animation
    korean_bars = ['Menu resources/korean_bar1.txt', 'Menu resources/korean_bar2.txt', 'Menu resources/korean_bar3.txt', 'Menu resources/korean_bar4.txt'] #KOREAN BAR animation
                
    def book_animation(paths):
        frames = []
        for name in paths:
            with open(name, "r", encoding="UTF-8") as f:
                frames.append(f.readlines())
        for _ in range(3):
            for frame in frames:
                asci = "".join(frame)
                print(colorText(asci)) 
                time.sleep(1.1)
                play_sound_effect("Sound effects/page turn.mp3")
                os.system("cls")

    def display_bar_animation(paths):
        frames = []
        for name in paths:
            with open(name, encoding='UTF-8') as f:
                frames.append(f.readlines())
        
        for _ in range(2):
            for frame in frames:
                play_sound_effect("Sound effects/bar animation.mp3")
                asci = ''.join(frame)
                print(colorText(asci))
                time.sleep(0.7)
                os.system('cls')
                
    def show_menu(for_opening= True):
        global default_theme, chosen_category, song_list_page, songs, first_run
        if not first_run: play_sound_effect("Sound effects/Esc.mp3")
        os.system('cls')
        if first_run:
            import intro
            play_sound_effect("Sound effects/boom.mp3") ; first_run = False
        os.system('cls')
        print(title)
        print(f"""{reset}{tab}{tab}{tab}                            {w}SELECT A MUSIC CATEGORY\n
    {blue}                          _____________{reset}                       {red}        _____________                       {white}        _____________                       {green}        _____________
    {blue}                       __/ {white} SONG BOOK {blue} \____________________  {red}     __/ {white} SONG BOOK {red} \____________________   {white}    __/{white}  SONG BOOK{white}  \____________________   {green}    __/{white}  SONG BOOK{green}  \____________________
    {blue}                      /█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {red}    /█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {white}    /█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    /█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {blue}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {red}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {white}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {blue}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {red}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {white}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|                
    {blue}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {red}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {white}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {blue}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {red}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {white}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {blue}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {red}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {white}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {yellow}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {red}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {red}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {yellow}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {red}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {red}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {yellow}                      |█|░░░░                           ░░░░| {red}    |█|░░░                             ░░░| {red}    |█|░                                 ░| {green}    |█|░░░░░                         ░░░░░|
    {yellow}                      |█|░░░░ {gr}    █▀█ {white}█ █▄ █ █▀█ █▄█  {yellow}  ░░░░|{red}     |█|░░░ {gr}  █▄▀ {white}█▀█ █▀█ █▀▀ ▄▀█ █▄ █ {red} ░░░|     {red}|█|░{gr}   █ {white}▄▀█ █▀█ ▄▀█ █▄ █ █▀▀ █▀ █▀▀{red} ░|{green}     |█|░░░░░   {gr}    ▄▀█ {white}█   █        {green} ░░░░░| 
    {yellow}                      |█|░░░░ {turquoise}    █▀▀ {white}█ █ ▀█ █▄█  █   {yellow}  ░░░░|{red}     |█|░░░ {turquoise}  █ █ {white}█▄█ █▀▄ ██▄ █▀█ █ ▀█ {red} ░░░|  {red}   |█|░{turquoise} █▄█ {white}█▀█ █▀▀ █▀█ █ ▀█ ██▄ ▄█ ██▄{red} ░|{green}     |█|░░░░░    {turquoise}   █▀█ {white}█▄▄ █▄▄     {green}  ░░░░░|
    {yellow}                      |█|░░░░                           ░░░░| {blue}    |█|░░░                            {blue} ░░░| {red}    |█|░                                 ░| {green}    |█|░░░░░                         ░░░░░|
    {yellow}                      |█|░░░░ {white}    █▀▄▀█ █ █ █▀ █ █▀▀  {yellow}  ░░░░|     {blue}|█|░░░ {white}     █▀▄▀█ █ █ █▀ █ █▀▀     {blue}░░░|{red}     |█|░{white}        █▀▄▀█ █ █ █▀ █ █▀▀{red}       ░|{green}     |█|░░░░░  {white}  █▀ █▀█ █▄ █ █▀▀ █▀  {green} ░░░░░|
    {yellow}                      |█|░░░░ {white}    █ ▀ █ █▄█ ▄█ █ █▄▄  {yellow}  ░░░░|     {blue}|█|░░░ {white}     █ ▀ █ █▄█ ▄█ █ █▄▄     {blue}░░░|{red}     |█|░{white}        █ ▀ █ █▄█ ▄█ █ █▄▄{red}       ░| {green}    |█|░░░░░  {white}  ▄█ █▄█ █ ▀█ █▄█ ▄█  {green} ░░░░░|
    {yellow}                      |█|░░░░                           ░░░░|  {blue}   |█|░░░                             ░░░|  {red}   |█|░                                 ░| {green}    |█|░░░░░                         ░░░░░|
    {yellow}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {blue}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {red}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {yellow}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {blue}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {red}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {red}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {blue}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {white}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {red}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {blue}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {white}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {red}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {blue}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {white}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {red}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {blue}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {white}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {red}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {blue}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {white}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {red}                      |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {blue}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|  {white}   |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| {green}    |█|░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░|
    {red}                      \______________/-------------------\__/  {blue}   \______________/-------------------\__/  {white}   \______________/-------------------\__/ {green}    \______________/-------------------\__/   
    """)
        print(f'''    
{tab}          {bar_yellow}_________________{bar_blue}_________________{bar_red}_________________{gr}_________________  █▀▀ {gray}▀▄▀ {gr}█ ▀█▀  _________________{bar_red}_________________{bar_blue}_________________{bar_yellow}__________________
{tab}                                                                                {turquoise}██▄ {gray}█░█ {turquoise}█ ░█░''')
        while True: #keyboard press flow
            if keyboard.is_pressed("p"): #PINOY CATEGORY
                chosen_category = "PH"
                play_sound_effect("Sound effects/menu selection.mp3")
                songs = get_songs(chosen_category)
                os.system('cls')
                display_theme_choices_or_thanksMessage("Menu resources/Pinoy_Theme.txt")
                print(back)
                while True:
                    if keyboard.is_pressed("c"): #pinoy theme
                        play_sound_effect("Sound effects/menu selection.mp3")
                        os.system('cls')
                        display_bar_animation(pinoy_bars)
                        book_animation(PH_Book)
                        song_list_page = SongList()
                        return song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
                    elif keyboard.is_pressed("g"): #green theme
                        play_sound_effect("Sound effects/menu selection.mp3")
                        os.system('cls')
                        display_bar_animation(green_bars)
                        book_animation(PH_Green_Book)
                        default_theme = True
                        song_list_page = SongList()
                        return song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
                    elif keyboard.is_pressed("esc"):
                        return show_menu()
            elif keyboard.is_pressed("k"): #KOREAN CATEGORY
                play_sound_effect("Sound effects/menu selection.mp3")
                chosen_category = "Korea"
                songs = get_songs(chosen_category)
                os.system('cls')
                display_theme_choices_or_thanksMessage("Menu resources/Korean_Theme.txt")
                print(back)
                while True:
                    if keyboard.is_pressed("c"): #korean theme
                        play_sound_effect("Sound effects/menu selection.mp3")
                        os.system('cls')
                        display_bar_animation(korean_bars)
                        book_animation(KR_Book)
                        song_list_page = SongList()
                        return song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
                    elif keyboard.is_pressed("g"): #green theme
                        play_sound_effect("Sound effects/menu selection.mp3")
                        os.system('cls')
                        display_bar_animation(green_bars)
                        book_animation(KR_Green_Book)
                        default_theme = True
                        song_list_page = SongList()
                        return song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
                    elif keyboard.is_pressed("esc"):
                        return show_menu()
            elif keyboard.is_pressed("j"): #JAPAN Category
                play_sound_effect("Sound effects/menu selection.mp3")
                chosen_category = "Japan"
                songs = get_songs(chosen_category)
                os.system('cls')
                display_theme_choices_or_thanksMessage("Menu resources/Japan_Theme.txt")
                print(back)
                while True:
                    if keyboard.is_pressed("c"): #japan theme
                        play_sound_effect("Sound effects/menu selection.mp3")
                        os.system('cls')
                        display_bar_animation(japan_bars)
                        book_animation(JP_Book)
                        song_list_page = SongList()
                        return song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
                    elif keyboard.is_pressed("g"): #green theme
                        play_sound_effect("Sound effects/menu selection.mp3")
                        os.system('cls')
                        display_bar_animation(green_bars)
                        book_animation(JP_Green_Book)
                        default_theme = True
                        song_list_page = SongList()
                        return song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
                    elif keyboard.is_pressed("esc"):
                        return show_menu()
            elif keyboard.is_pressed("a"): #ALL Category
                play_sound_effect("Sound effects/menu selection.mp3")
                chosen_category = "All Songs"
                song_list_page = SongList()
                songs = get_songs(chosen_category)
                os.system('cls')
                display_bar_animation(green_bars)
                book_animation(ALL_Book)
                return song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
            elif keyboard.is_pressed("x"): #EXIT
                os.system('cls')
                keyboard.press("x")
                display_theme_choices_or_thanksMessage("Menu resources/Exit_Thanks.txt")
                return "Exited"
    return show_menu()

def play_song(path: str):
    pygame.init() 
    if chosen_category != "All Songs":
        pygame.mixer.music.load(path)
    else:
        categories = ["PH", "Japan", "Korea"]
        path = path.split("/")
        path[1] = categories[int(path[2][1])-1]
        pygame.mixer.music.load("/".join(path))
    pygame.mixer.music.play()
    
def get_songs(chosen_category : str) -> list:
    paths = {"PH":"Song books/PH Songbook.txt", "Japan": "Song books/JP Songbook.txt", "Korea": "Song books/KR Songbook.txt" }
    if chosen_category != "All Songs":
        with open (paths[chosen_category]) as f:
            songs = [song.strip() for song in f.readlines()]
    else:
        songs = []
        for path in paths:
            with open(paths[path]) as f:
                songs+=[song.strip() for song in f.readlines()]
    final_song_list = []                
    for song in songs:
        song = song.split("%")
        final_song_list.append("{}  {}{}{}{}".format(tab, f'{song[0]: <14}', f'{song[1]: <25}', f'{song[2]: <25}', f'{song[3]}'))
    return final_song_list

def display_musicPlayer_menu( play_button = "█ █", color= "" ): 
    t1 = "\t" *4 + " " *4
    print(f'''\n\t    {thin_line}\n{border_color}{tab3} ╔⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤╗
{tab3}{border_color} ┊  {icon_color} ,----, {border_color}┊{playing_color}  ɴᴏᴡ ᴘʟᴀʏɪɴɢ ♫                                                                                  
{tab3}{border_color} ┊  {icon_color} |    | {border_color}┊ {title_color} {title}{buttons_color}🗘   〡◀       {play_button}      ▶ 〡  ⭮\
    {t1}{volume}{color}{"".join([random.choice(list("▁▂▃▄▅▆█")) if i%2==0 else f" " for i in range(18)]) if color else "▁ ▂ ▃ ▄ ▅ ▆ █"}  {w}⇱  {r}🆇
{tab3}{border_color} ┊ {icon_color}(_|  (_| {border_color}┊{artist_color}{bold}  {artist}''')

def play_song_preview():
    global artist, title, bar_sec_4SongList
    if currently_hovered_4queue == -1:
        os.system("cls")
        song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
        if chosen_category != "All Songs":
            currently_hovered_song = song_list_page.song_list[currently_hovered_4songList]
            song_code, artist, song_name, _ = [element.strip() for element in currently_hovered_song.split("   ") if element]
            title = "{}".format(f'{song_name:<50}')#-------   
        else:
            currently_hovered_song = song_list_page.song_list[int(f"{current_page-1}{currently_hovered_4songList}")]
            song_code, artist, song_name, _ = [element.strip() for element in currently_hovered_song.split("   ") if element]
            title = "{}".format(f'{song_name:<50}')#-------
     
        play_song(f'Songs/{chosen_category}/{song_code}.mp3')
        space_num = [15, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        if chosen_category == "All Songs":      spaces = space_num[song_queue.get_length() if song_queue.get_length() <10 else 10]
        else: spaces = space_num[song_queue.get_length() if song_queue.get_length() <10 else 10]+5
        print("\n"*spaces)
        display_musicPlayer_menu()
        songPreview_startingTime, bar_sec_4SongList = time.time(), 0

        while bar_sec_4SongList <=60:
            print(f'{tab3}{border_color} ╚⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤╝{tab4}{sec_color}'+'{}'.format("0" if bar_sec_4SongList < 60 else "1")+\
                ":{}".format(f"0{bar_sec_4SongList}" if bar_sec_4SongList < 10 else bar_sec_4SongList if bar_sec_4SongList <60 else "00")+f' {bar_color}{x*bar_sec_4SongList}{gray}{x*(60-bar_sec_4SongList)}{reset}', end="\r")
            bar_sec_4SongList = round(time.time()- songPreview_startingTime)
            if keyboard.is_pressed("space"):
                song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
                    
                print("\n"*spaces) 
                display_musicPlayer_menu(play_button="███")
                print(f'{tab3}{border_color} ╚⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤╝{tab4}{sec_color}'+'{}'.format("0" if bar_sec_4SongList < 60 else "1")+\
                ":{}".format(f"0{bar_sec_4SongList}" if bar_sec_4SongList < 10 else bar_sec_4SongList if bar_sec_4SongList <60 else "00")+f' {bar_color}{x*bar_sec_4SongList}{gray}{x*(60-bar_sec_4SongList)}{reset}', end="\r")
                break
        pygame.mixer.music.stop()  

def play_sound_effect(path: str) -> None:
    pygame.init() 
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def bring_down_hover_4songList_page():
    global currently_hovered_4songList, currently_hovered_4queue
    if currently_hovered_4songList <9: 
        currently_hovered_4songList+=1
        play_sound_effect("Sound effects/Hover sound.mp3")
        song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
    else:
        if song_queue.get_length() < 10: valid_downward_movement = currently_hovered_4queue <= song_queue.get_length()-2 
        else: valid_downward_movement = currently_hovered_4queue <9
        if valid_downward_movement:
            if currently_hovered_4songList == 9: currently_hovered_4songList +=1
            currently_hovered_4queue+=1
            play_sound_effect("Sound effects/Hover sound.mp3")
            song_list_page.display_songList_page(currently_hovered_4songList = None,  currently_hovered_4queue = currently_hovered_4queue)
    
def bring_up_hover_4songList_page():
    global currently_hovered_4songList, currently_hovered_4queue
    if currently_hovered_4queue == 0:
        currently_hovered_4queue-=1
        currently_hovered_4songList-=1
        play_sound_effect("Sound effects/Hover sound.mp3")
        song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
    elif currently_hovered_4songList > 0 and currently_hovered_4queue==-1:
        currently_hovered_4songList-=1
        play_sound_effect("Sound effects/Hover sound.mp3")
        song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
    elif currently_hovered_4songList==10:
        currently_hovered_4queue-=1
        play_sound_effect("Sound effects/Hover sound.mp3")
        song_list_page.display_songList_page(currently_hovered_4songList = None, currently_hovered_4queue = currently_hovered_4queue)
    
def add_to_queue():
    if currently_hovered_4songList!=10 and not song_queue.has(song_list_page.song_list[int(f"{current_page-1}{currently_hovered_4songList}")]):
        song_queue.append(song_list_page.song_list[int(f"{current_page-1}{currently_hovered_4songList}")])
        play_sound_effect("Sound effects/Add to queue.mp3")
        song_list_page.display_songList_page(currently_hovered_4songList=currently_hovered_4songList,\
                                            song_code = song_list_page.song_list[int(f"{current_page-1}{currently_hovered_4songList}")].split()[0])
    
def remove_from_queue():
    global currently_hovered_4queue, currently_hovered_4songList
    try:
        if song_queue.get_elements()[currently_hovered_4queue]:
            if song_queue.get_length()==1 and currently_hovered_4songList==10:
                play_sound_effect("Sound effects/Remove from queue.mp3")
                song_queue.remove(song_queue.get_elements()[currently_hovered_4queue])
                currently_hovered_4queue-=1
                currently_hovered_4songList-=1
                song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
            elif currently_hovered_4queue!=-1:
                play_sound_effect("Sound effects/Remove from queue.mp3")
                song_queue.remove(song_queue.get_elements()[currently_hovered_4queue])
                if currently_hovered_4queue > 0:
                    currently_hovered_4queue-=1
                    song_list_page.display_songList_page(currently_hovered_4songList = None, currently_hovered_4queue = currently_hovered_4queue)
                else:
                    song_list_page.display_songList_page(currently_hovered_4songList = None, currently_hovered_4queue = currently_hovered_4queue)
    except:
        pass

def view_songList_nextPage():
    global current_page
    if current_page !=3 and chosen_category == "All Songs" and currently_hovered_4queue==-1:
        current_page+=1
        play_sound_effect("Sound effects/Next page.mp3")
        song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)

def view_songList_perviousPage():
    global current_page
    if current_page !=1 and chosen_category == "All Songs" and currently_hovered_4queue==-1:
        current_page-=1
        play_sound_effect("Sound effects/Next page.mp3")
        song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)

def print_song_title(song_code):
    if chosen_category == "All Songs" or default_theme:
        white, red, red2, yellow, yellow2, blue, cyan = fg(15), fg(35), fg(36), fg(35), fg(36), fg(35), fg(36)
    else:
        white, red, red2, yellow, yellow2, blue, cyan = fg(15), fg(196), fg(204), fg(228), fg(220), "\033[0;34m", "\033[96m"
    tab, tab2, tab3 = "\t" *7, "\t" *4, "\t" *3
    match song_code:
        case "01001":
            print(f""" 
{tab}\t         ♪ ╔═══╗                                                                ╔═══╗ ♪
{tab}\t        ♫  ║███║  {yellow}▄▀█ {yellow2}█▀▄ {yellow}█ {yellow2}█▀▀  {white} ▄▄  {yellow} █▀█ {yellow2}▄▀█ {yellow}█▀█ {yellow2}▄▀█ {yellow}█░░{yellow2} █░█{yellow} █▀▄▀█ {yellow2}▄▀█{yellow} █▄░█ {white}  ║███║  ♫
{tab}\t        {yellow} ♫ ║(O)║  {yellow2}█▀█{yellow} █▄▀ {yellow2}█{yellow} ██▄   ░░  {yellow2} █▀▀{yellow} █▀█{yellow2} █▀▄{yellow} █▀█{yellow2} █▄▄ {yellow}█▄█ {yellow2}█░▀░█ {yellow}█▀█{yellow2} █░▀█{yellow}   ║(●)║ ♫
{tab}\t    {yellow2}    ♪  ╚═══╝                                                                ╚═══╝  ♪
""")
        case "01002":
           print(f""" 
{tab2}\t        {white} ♪ ╔═══╗                                                                                                                 ╔═══╗ ♪
{tab2}\t        ♫  ║███║  {yellow}▄▀█ {yellow2}█▀█ {yellow}█▀█  {yellow2} █░█ {yellow}█ {yellow2}█▄▀{yellow} █{yellow} █▄░█{yellow2} █▀▀  {yellow} █▀{yellow2} █▀█ {yellow}█▀▀{yellow2} █ {yellow}█▀▀ {yellow2}▀█▀ {yellow}█▄█  {white} ▄▄  {yellow2} █▀█ {yellow}▄▀█ {yellow2}█▄░█{yellow} ▄▀█ {yellow2}█░░ {yellow}▄▀█ {yellow2}█▄░█{yellow} █▀▀ {yellow2}█ {yellow}█▄░█ {white} ║███║  ♫
{tab2}\t        {yellow} ♫ ║(O)║  {yellow2}█▀█ {yellow}█▀▀ {yellow2}█▄█  {yellow} █▀█ {yellow2}█ {yellow}█░█{yellow2} █{yellow2} █░▀█ {yellow}█▄█ {yellow2}  ▄█ {yellow}█▄█ {yellow2}█▄▄ {yellow}█ {yellow2}██▄ {yellow}░█░ {yellow2}░█░   ░░  {yellow} █▀▀{yellow2} █▀█ {yellow}█░▀█ {yellow2}█▀█ {yellow}█▄▄{yellow2} █▀█{yellow} █░▀█{yellow2} █▄█ {yellow}█ {yellow2}█░▀█{yellow}  ║(●)║ ♫
{tab2}\t       {yellow2} ♪  ╚═══╝                                                                                                                 ╚═══╝  ♪
""")
        case "01003":
            print(f"""
{tab2}\t       {white} ♪ ╔═══╗                                                                                                                   ╔═══╗ ♪
{tab2}\t       ♫  ║███║  {yellow}{yellow}█▀▀ {yellow2}█▀█ {yellow}▄▀█ {yellow2}█▄░█ {yellow}█▀▀ {yellow2}█ {yellow}█▀  {yellow2} █▀▄▀█ ░ {white}  ▄▄  {yellow2} █▄▀ {yellow}▄▀█{yellow2} █░░ {yellow}█▀▀{yellow2} █ {yellow}█▀▄ {yellow2}█▀█ {yellow}█▀ {yellow2}█▀▀{yellow} █▀█ {yellow2}█▀█ {yellow}█▀▀  {yellow2} █░█░█ {yellow}█▀█{yellow2} █▀█ {yellow}█░░ {yellow2}█▀▄ {white} ║███║  ♫
{tab2}\t       {yellow} ♫ ║(O)║  {yellow2}█▀░ {yellow}█▀▄ {yellow2}█▀█{yellow} █░▀█ {yellow2}█▄▄ {yellow}█ {yellow2}▄█  {yellow} █░▀░█ {yellow2}▄   ░░  {yellow} █░█{yellow2} █▀█{yellow} █▄▄{yellow2} ██▄ {yellow}█ {yellow2}█▄▀ {yellow}█▄█{yellow2} ▄█ {yellow}█▄▄{yellow2} █▄█ {yellow}█▀▀{yellow2} ██▄  {yellow} ▀▄▀▄▀ {yellow2}█▄█ {yellow}█▀▄{yellow2} █▄▄ {yellow}█▄▀{yellow}  ║(●)║ ♫ 
{tab2}\t      {yellow2} ♪  ╚═══╝                                                                                                                   ╚═══╝  ♪
""")
        case "01004":
           print(f"""
{tab3}\t\t     {white} ♪ ╔═══╗                                                                                                                      ╔═══╗ ♪
{tab3}\t\t     ♫  ║███║  {yellow}{yellow}█ {yellow2}█░█  {yellow} █▀█ {yellow2}█▀▀  {yellow} █▀ {yellow2}█▀█ {yellow}▄▀█ {yellow2}█▀▄ {yellow}█▀▀{yellow2} █▀ {white}  ▄▄  {yellow} █▀▄ {yellow2}█░█ {yellow}█░░{yellow2} █▀█  {yellow} █▄░█ {yellow2}█▀▀  {yellow} █░█{yellow2} ▄▀█ {yellow}█▄░█ {yellow2}█▀▀ {yellow}█▀▀ {yellow2}▄▀█ {yellow}█▄░█ {yellow2}▄▀█ {yellow}█▄░█ {white} ║███║  ♫
{tab3}\t\t     {yellow} ♫ ║(O)║  {yellow2}█ {yellow}▀▄▀ {yellow2}  █▄█ {yellow}█▀░ {yellow2}  ▄█ {yellow}█▀▀{yellow2} █▀█ {yellow}█▄▀{yellow2} ██▄ {yellow}▄█   ░░  {yellow2} █▄▀ {yellow}█▄█{yellow2} █▄▄ {yellow}█▄█  {yellow2} █░▀█ {yellow}█▄█  {yellow2} █▀█ {yellow}█▀█{yellow2} █░▀█ {yellow}█▄█ {yellow2}█▄█ {yellow}█▀█ {yellow2}█░▀█ {yellow}█▀█ {yellow2}█░▀█{yellow}  ║(●)║ ♫  
{tab3}\t\t    {yellow2} ♪  ╚═══╝                                                                                                                      ╚═══╝  ♪
""")
        case "01005":
            print(f""" 
{tab2}\t\t\t           {white} ♪ ╔═══╗                                                                            ╔═══╗ ♪
{tab2}\t\t\t           ♫  ║███║  {yellow}{yellow}░░█ {yellow2}█░█ {yellow}▄▀█{yellow2} █▄░█  {yellow} █▄▀{yellow2} ▄▀█ {yellow}█▀█{yellow2} █░░ {yellow}█▀█{yellow2} █▀  {white} ▄▄  {yellow} █▄▄{yellow2} █░█ {yellow}█▄▀{yellow2} █▀ {yellow}▄▀█ {yellow2}█▄░█ {white} ║███║  ♫
{tab2}\t\t\t           {yellow} ♫ ║(O)║  {yellow2}█▄█{yellow} █▄█ {yellow2}█▀█{yellow} █░▀█ {yellow2}  █░█ {yellow}█▀█ {yellow2}█▀▄ {yellow}█▄▄ {yellow2}█▄█ {yellow}▄█   ░░  {yellow2} █▄█ {yellow}█▄█ {yellow2}█░█{yellow} ▄█ {yellow2}█▀█ {yellow}█░▀█{yellow}  ║(●)║ ♫   
{tab2}\t\t\t          {yellow2} ♪  ╚═══╝                                                                            ╚═══╝  ♪
""")
        case "01006":
            print(f"""
{tab2}\t\t\t            {white} ♪ ╔═══╗                                                                         ╔═══╗ ♪
{tab2}\t\t\t            ♫  ║███║  {yellow}{yellow}░░█ {yellow2}█░█ {yellow}▄▀█{yellow2} █▄░█  {yellow} █▄▀{yellow2} ▄▀█ {yellow}█▀█{yellow2} █░░ {yellow}█▀█{yellow2} █▀  {white} ▄▄ {yellow}█▀█ {yellow2}▄▀█{yellow} █▄░█{yellow2} █▀▀{yellow} █{yellow2} ▀█▀{white}  ║███║  ♫
{tab2}\t\t\t            {yellow} ♫ ║(O)║  {yellow2}█▄█{yellow} █▄█ {yellow2}█▀█{yellow} █░▀█ {yellow2}  █░█ {yellow}█▀█ {yellow2}█▀▄ {yellow}█▄▄ {yellow2}█▄█ {yellow}▄█   ░░{yellow2} █▀▀{yellow} █▀█{yellow2} █░▀█{yellow} █▄▄{yellow2} █ {yellow}░█░{yellow}  ║(●)║ ♫ 
{tab2}\t\t\t           {yellow2} ♪  ╚═══╝                                                                         ╚═══╝  ♪
""")
        case "01007":
            print(f"""
{tab2}\t\t\t         {white} ♪ ╔═══╗                                                                               ╔═══╗ ♪
{tab2}\t\t\t         ♫  ║███║  {yellow}{yellow}█▀▄▀█ {yellow2}▄▀█{yellow} █▀▀ {yellow2}█▄░█{yellow} █░█ {yellow2}█▀  {yellow} █░█ {yellow2}▄▀█ {yellow}█░█ {yellow2}█▀▀{yellow} █▄░█ {white}  ▄▄  {yellow2} █ {yellow}█▀▄▀█ {yellow2}▄▀█ {yellow}█░█ {yellow2}█▀▀{white}  ║███║  ♫
{tab2}\t\t\t         {yellow} ♫ ║(O)║  {yellow2}█░▀░█ {yellow}█▀█ {yellow2}█▄█ {yellow}█░▀█ {yellow2}█▄█{yellow} ▄█  {yellow2} █▀█ {yellow}█▀█{yellow2} ▀▄▀ {yellow}██▄ {yellow2}█░▀█   ░░  {yellow} █ {yellow2}█░▀░█{yellow} █▀█ {yellow2}█▀█ {yellow}██▄{yellow}  ║(●)║ ♫  
{tab2}\t\t\t        {yellow2} ♪  ╚═══╝                                                                               ╚═══╝  ♪
""")
        case "01008":
            print(f""" 
{tab2}\t\t            {white} ♪ ╔═══╗                                                                                         ╔═══╗ ♪
{tab2}\t\t            ♫  ║███║  {yellow}{yellow}█▀ {yellow2}▄▀█ {yellow}█▀▄▀█  {yellow2} █▀▀ {yellow}█▀█{yellow2} █▄░█{yellow} █▀▀ {yellow2}█▀▀ {yellow}█▀█ {yellow2}█▀▀ {yellow}█ {yellow2}█▀█ {yellow}█▄░█ {white}  ▄▄  {yellow2} █▀▄ {yellow}█{yellow2} █░█░█ {yellow}▄▀█ {yellow2}▀█▀ {yellow}▄▀█{white}  ║███║  ♫
{tab2}\t\t            {yellow} ♫ ║(O)║  {yellow2}▄█ {yellow}█▀█ {yellow2}█░▀░█  {yellow} █▄▄{yellow2} █▄█ {yellow}█░▀█{yellow2} █▄▄{yellow} ██▄{yellow2} █▀▀{yellow} █▄▄{yellow2} █{yellow} █▄█ {yellow2}█░▀█   ░░  {yellow} █▄▀{yellow2} █ {yellow}▀▄▀▄▀{yellow2} █▀█ {yellow}░█░ {yellow2}█▀█{yellow}  ║(●)║ ♫
{tab2}\t\t           {yellow2} ♪  ╚═══╝                                                                                         ╚═══╝  ♪
""")
        case "01009":
            print(f"""
{tab2}\t\t\t             {white} ♪ ╔═══╗                                                                        ╔═══╗ ♪
{tab2}\t\t\t             ♫  ║███║  {yellow}{yellow}▀█{yellow2} ▄▀█ {yellow}█▀▀{yellow2} █▄▀  {yellow} ▀█▀ {yellow2}▄▀█{yellow} █▄▄{yellow2} █░█ {yellow}█▀▄ {yellow2}█░░ {yellow}█▀█ {white}  ▄▄  {yellow2} █▀█{yellow} ▄▀█{yellow2} █▄░█ {yellow}█▀█{white}  ║███║  ♫
{tab2}\t\t\t             {yellow} ♫ ║(O)║  {yellow2}█▄ {yellow}█▀█ {yellow2}█▄▄ {yellow}█░█  {yellow2} ░█░ {yellow}█▀█ {yellow2}█▄█ {yellow}█▄█ {yellow2}█▄▀ {yellow}█▄▄{yellow2} █▄█   ░░  {yellow} █▀▀ {yellow2}█▀█{yellow} █░▀█ {yellow2}█▄█{yellow}  ║(●)║ ♫ 
{tab2}\t\t\t            {yellow2} ♪  ╚═══╝                                                                        ╚═══╝  ♪
""")
        case "01010":
           print(f"""
{tab2}\t\t\t          {white} ♪ ╔═══╗                                                                              ╔═══╗ ♪
{tab2}\t\t\t          ♫  ║███║  {yellow}{yellow}▀█ {yellow2}▄▀█ {yellow}█▀▀ {yellow2}█▄▀  {yellow} ▀█▀ {yellow2}▄▀█ {yellow}█▄▄ {yellow2}█░█{yellow} █▀▄{yellow2} █░░{yellow} █▀█ {white} ▄▄  {yellow2} █░█{yellow} ▄▀█ {yellow2}▀█▀ {yellow}█▀▄ {yellow2}█▀█ {yellow}█▀▀{white}  ║███║  ♫
{tab2}\t\t\t          {yellow} ♫ ║(O)║  {yellow2}█▄ {yellow}█▀█ {yellow2}█▄▄ {yellow}█░█  {yellow2} ░█░ {yellow}█▀█ {yellow2}█▄█ {yellow}█▄█ {yellow2}█▄▀ {yellow}█▄▄ {yellow2}█▄█  ░░  {yellow} █▀█ {yellow2}█▀█ {yellow}░█░{yellow2} █▄▀{yellow} █▄█ {yellow2}█▄█{yellow}  ║(●)║ ♫ 
{tab2}\t\t\t         {yellow2} ♪  ╚═══╝                                                                              ╚═══╝  ♪
""")
        case "02001":
            print(f"""  
{tab}\t\t        {white} ♪ ╔═══╗                                                   ╔═══╗ ♪
{tab}\t\t        ♫  ║███║  {red}{red}▄▀█{red2} █░░ {red}█▀▀{red2} █▄▀{red} █░█{red2} █▄░█  {white} ▄▄  {red} █▄▄ {red2}▄▀█{red} █▄▀{red2} ▄▀█{white}  ║███║  ♫
{tab}\t\t        {red2} ♫ ║(O)║  {red2}█▀█ {red}█▄▄ {red2}██▄{red} █░█{red2} █▄█ {red}█░▀█   ░░  {red2} █▄█ {red}█▀█ {red2}█░█ {red}█▀█{red2}  ║(●)║ ♫
{tab}\t\t       {red} ♪  ╚═══╝                                                   ╚═══╝  ♪
""")
        case "02002":
           print(f"""
{tab2}\t\t\t      {white} ♪ ╔═══╗                                                                                      ╔═══╗ ♪
{tab2}\t\t\t      ♫  ║███║  {red}{red}▄▀█ {red2}█▀▄▀█ {red}█ {red2}  █▀ {red}▄▀█ {red2}█▄▀ {red}▄▀█ {red2}█▀▀ {red}█░█{red2} █▀▀ {red}█░█ {red2}█ {white}  ▄▄  {red} █▀▀ {red2}█▀▀ {red}█▄░█ {red2}▀█▀ {red}█▀█ {red2}▄▀█{red} █░░{white}  ║███║  ♫
{tab2}\t\t\t      {red2} ♫ ║(O)║  {red2}█▀█ {red}█░▀░█ {red2}█  {red} ▄█ {red2}█▀█ {red}█░█{red2} █▀█ {red}█▄█{red2} █▄█ {red}█▄▄ {red2}█▀█ {red}█   ░░  {red2} █▄▄ {red}██▄{red2} █░▀█ {red}░█░ {red2}█▀▄ {red}█▀█ {red2}█▄▄{red2}  ║(●)║ ♫
{tab2}\t\t\t     {red} ♪  ╚═══╝                                                                                      ╚═══╝  ♪
 """)
        case "02003":
            print(f"""
{tab2}\t\t\t           {white} ♪ ╔═══╗                                                                            ╔═══╗ ♪
{tab2}\t\t\t           ♫  ║███║  {red}{red}█▄▄{red2} ▄▀█ {red}█▀▀{red2} █▄▀  {red} █▀█ {red2}█▄░█  {white} ▄▄  {red} █▀{red2} ▀█▀ {red}█▀█ {red2}█ {red}█▄▀ {red2}█▀▀ {red}  █▄▄ {red2}▄▀█{red} █▀▀{red2} █▄▀{white}  ║███║  ♫
{tab2}\t\t\t           {red2} ♫ ║(O)║  {red2}█▄█ {red}█▀█{red2} █▄▄{red} █░█ {red2}  █▄█{red} █░▀█   ░░  {red2} ▄█ {red}░█░ {red2}█▀▄ {red}█{red2} █░█ {red}██▄ {red2}  █▄█ {red}█▀█ {red2}█▄▄ {red}█░█{red2}  ║(●)║ ♫ 
{tab2}\t\t\t          {red} ♪  ╚═══╝                                                                            ╚═══╝  ♪
""")
        case "02004":
            print(f""" 
{tab2}\t\t\t      {white} ♪ ╔═══╗                                                                                     ╔═══╗ ♪
{tab2}\t\t\t      ♫  ║███║   {red}{red}█▄▀{red2} ▄▀█ {red}█▄░█ {red2}▄▀█  {red} █▄▄{red2} █▀█ {red}█▀█ {red2}█▄░█  {white} ▄▄  {red} █▀ {red2}█ {red}█░░ {red2}█░█ {red}█▀█ {red2}█░█ {red}█▀▀{red2} ▀█▀ {red}▀█▀{red2} █▀▀{white}   ║███║  ♫
{tab2}\t\t\t      {red2} ♫ ║(O)║   {red2}█░█ {red}█▀█{red2} █░▀█ {red}█▀█ {red2}  █▄█{red} █▄█ {red2}█▄█{red} █░▀█   ░░ {red2}  ▄█ {red}█ {red2}█▄▄ {red}█▀█ {red2}█▄█ {red}█▄█ {red2}██▄ {red}░█░{red2} ░█░ {red}██▄{red2}   ║(●)║ ♫ 
{tab2}\t\t\t     {red} ♪  ╚═══╝                                                                                     ╚═══╝  ♪
""")
        case "02005":
            print(f"""
{tab3}\t        {white} ♪ ╔═══╗                                                                                                                             ╔═══╗ ♪
{tab3}\t        ♫  ║███║  {red}{red}█▄▀{red2} ▄▀█ {red}█▄░█ {red2}▄▀█  {red} █░█ {red2}▄▀█ {red}█▄░█ {red2}▄▀█ {red}▀█ {red2}▄▀█ {red}█░█░█ {red2}▄▀█  {white} ▄▄ {red}  █▀█ {red2}█▀▀{red} █▄░█{red2} ▄▀█ {red}█  {red2} █▀▀ {red}█ {red2}█▀█{red} █▀▀ {red2}█░█ {red}█░░{red2} ▄▀█ {red}▀█▀{red2} █ {red}█▀█ {red2}█▄░█{white}  ║███║  ♫
{tab3}\t        {red2} ♫ ║(O)║  {red2}█░█{red} █▀█{red2} █░▀█{red} █▀█ {red2}  █▀█ {red}█▀█{red2} █░▀█ {red}█▀█ {red2}█▄ {red}█▀█{red2} ▀▄▀▄▀ {red}█▀█   ░░  {red2} █▀▄{red} ██▄ {red2}█░▀█{red} █▀█ {red2}█ {red}  █▄▄ {red2}█{red} █▀▄ {red2}█▄▄{red} █▄█ {red2}█▄▄ {red}█▀█ {red2}░█░ {red}█ {red2}█▄█ {red}█░▀█{red2}  ║(●)║ ♫
{tab3}\t       {red} ♪  ╚═══╝                                                                                                                             ╚═══╝  ♪
""")
        case "02006":
            print(f""" 
{tab}\t\t       {white} ♪ ╔═══╗                                                    ╔═══╗ ♪
{tab}\t\t       ♫  ║███║  {red}{red}█░░ {red2}█ {red}█▀ {red2}▄▀█  {white} ▄▄  {red} █▀▀{red2} █░█ {red}█▀█ {red2}█▀▀{red} █▄░█ {red2}█▀▀ {red}█▀▀{white}  ║███║  ♫
{tab}\t\t       {red2} ♫ ║(O)║  {red2}█▄▄ {red}█ {red2}▄█ {red}█▀█   ░░  {red2} █▄█{red} █▄█ {red2}█▀▄ {red}██▄ {red2}█░▀█ {red}█▄█ {red2}██▄{red2}  ║(●)║ ♫
{tab}\t\t      {red} ♪  ╚═══╝                                                    ╚═══╝  ♪
""")
        case "02007":
            print(f""" 
{tab2}\t             {white} ♪ ╔═══╗                                                                                                      ╔═══╗ ♪
{tab2}\t             ♫  ║███║   {red}{red}█▀▄▀█{red2} ▄▀█ {red}█▀▀{red2} █░█ {red}█▀▄▀█{red2} ▄▀█ {red}█▀▀{red2} █░█  {white} ▄▄  {red} █▀█ {red2}▀█▀{red} █▀█ {red2}▀█▀ {red}█▀█ {red2}█  {red} █▄▀ {red2}█ {red}█▄█ {red2}▄▀█ {red}█▀▀ {red2}▄▀█{red} █▀█{red2} █▀▀{white}   ║███║  ♫
{tab2}\t             {red2} ♫ ║(O)║   {red2}█░▀░█ {red}█▀█{red2} █▀░{red} █▄█ {red2}█░▀░█ {red}█▀█{red2} █▀░ {red}█▄█   ░░  {red2} █▄█ {red}░█░{red2} █▄█ {red}░█░{red2} █▄█ {red}█  {red2} █░█{red} █ ░{red2}█░ {red}█▀█{red2} █▄█ {red}█▀█{red2} █▀▄ {red}██▄{red2}   ║(●)║ ♫
{tab2}\t            {red} ♪  ╚═══╝                                                                                                      ╚═══╝  ♪
""")
        case "02008":
            print(f""" 
{tab}\t             {white} ♪ ╔═══╗                                                       ╔═══╗ ♪
{tab}\t             ♫  ║███║  {red}{red}█▀▄▀█{red2} █ {red}█▄░█ {red2}▄▀█ {red}█▀▄▀█{red2} █  {white} ▄▄  {red} █░░ {red2}█ {red}█░░{red2} █ {red}▄▀█ {red2}█▀▀{white}  ║███║  ♫
{tab}\t             {red2} ♫ ║(O)║  {red2}█░▀░█ {red}█ {red2}█░▀█{red} █▀█ {red2}█░▀░█ {red}█   ░░  {red2} █▄▄{red} █ {red2}█▄▄ {red}█{red2} █▀█ {red}█▄▄{red2}  ║(●)║ ♫
{tab}\t            {red} ♪  ╚═══╝                                                       ╚═══╝  ♪
""")
        case "02009":
            print(f""" 
{tab2}\t\t\t         {white} ♪ ╔═══╗                                                                                ╔═══╗ ♪
{tab2}\t\t\t         ♫  ║███║  {red}{red}█▀ {red2}▄▀█ {red}█░█░█{red2} ▄▀█ {red}█▄░█ {red2}█▀█  {red} █░█{red2} █ {red}█▀█ {red2}█▀█ {red}█▄█ {red2}█░█ {red}█▄▀ {red2}█  {white} ▄▄  {red} ▄▀█ {red2}█░█ {red}█ {red2}█▀▄{white}  ║███║  ♫
{tab2}\t\t\t         {red2} ♫ ║(O)║  {red2}▄█ {red}█▀█{red2} ▀▄▀▄▀ {red}█▀█{red2} █░▀█ {red}█▄█ {red2}  █▀█ {red}█ {red2}█▀▄ {red}█▄█{red2} ░█░ {red}█▄█ {red2}█░█ {red}█   ░░ {red2}  █▀█ {red}▀▄▀{red2} █ {red}█▄▀{red2}  ║(●)║ ♫
{tab2}\t\t\t        {red} ♪  ╚═══╝                                                                                ╚═══╝  ♪
""")
        case "02010":
            print(f"""
{tab}\t           {white} ♪ ╔═══╗                                                          ╔═══╗ ♪
{tab}\t           ♫  ║███║  {red}{red}█▀ {red2}█░█ {red}█▀▄▀█{red2} █ {red}█▄▀ {red2}▄▀█  {white} ▄▄  {red} █▀▀ {red2}█{red} █▀▀ {red2}▀█▀ {red}█ {red2}█▀█{red} █▄░█{white}  ║███║  ♫
{tab}\t           {red2} ♫ ║(O)║  {red2}▄█{red} █▄█ {red2}█░▀░█ {red}█ {red2}█░█ {red}█▀█   ░░  {red2} █▀░ {red}█ {red2}█▄▄ {red}░█░{red2} █ {red}█▄█ {red2}█░▀█{red2}  ║(●)║ ♫
{tab}\t          {red} ♪  ╚═══╝                                                          ╚═══╝  ♪
""")
        case "03001":
            print(f""" 
{tab}\t           {white} ♪ ╔═══╗                                                          ╔═══╗ ♪
{tab}\t           ♫  ║███║  {blue}{blue}░░█ {cyan}█▄█ {blue}█▀█  {white} ▄▄ {cyan}  █▀▄ {blue}█▀█ {cyan}█▀▀ {blue}▄▀█ {cyan}█▀▄▀█{blue} █░█ {cyan}█ {blue}█▀▀{cyan} █░█{white}  ║███║  ♫
{tab}\t           {cyan} ♫ ║(O)║  {cyan}█▄█ {blue}░█░ {cyan}█▀▀   ░░  {blue} █▄▀{cyan} █▀▄ {blue}██▄ {cyan}█▀█ {blue}█░▀░█{cyan} █▀█ {blue}█ {cyan}█▄█{blue} █▀█{cyan}  ║(●)║ ♫
{tab}\t          {blue} ♪  ╚═══╝                                                          ╚═══╝  ♪
""")
        case "03002":
            print(f"""
{tab}\t            {white} ♪ ╔═══╗                                                          ╔═══╗ ♪
{tab}\t            ♫  ║███║   {blue}{blue}█▀ {cyan}▀█▀ {blue}█▀█ {cyan}▄▀█ {blue}█▄█  {cyan} █▄▀ {blue}█{cyan} █▀▄ {blue}█▀ {white}  ▄▄  {cyan} ▀█▀ {blue}█▀█ {cyan}█▀█{white}   ║███║  ♫
{tab}\t            {cyan} ♫ ║(O)║   {cyan}▄█ {blue}░█░ {cyan}█▀▄{blue} █▀█ {cyan}░█░  {blue} █░█ {cyan}█ {blue}█▄▀ {cyan}▄█   ░░  {blue} ░█░ {cyan}█▄█ {blue}█▀▀{cyan}   ║(●)║ ♫
{tab}\t           {blue} ♪  ╚═══╝                                                          ╚═══╝  ♪
""")
        case"03003":
            print(f""" 
{tab2}\t\t             {white} ♪ ╔═══╗                                                                                       ╔═══╗ ♪
{tab2}\t\t             ♫  ║███║  {blue}{blue}█▀▄ {cyan}▄▀█{blue} █░█ {cyan}█ {blue}█▀▀ {cyan}█░█ {blue}█ {white}  ▄▄ {cyan}  █▀▀{blue} █▀█ {cyan}█▀█ {blue}█▀▀ {cyan}█▀▀ {blue}▀█▀ {cyan}▀█▀{blue} █{cyan} █▄░█ {blue}█▀▀ {cyan}  █▄█ {blue}█▀█ {cyan}█░█{white}  ║███║  ♫
{tab2}\t\t             {cyan} ♫ ║(O)║  {cyan}█▄▀{blue} █▀█ {cyan}▀▄▀{blue} █{cyan} █▄▄{blue} █▀█ {cyan}█   ░░  {blue} █▀░ {cyan}█▄█ {blue}█▀▄ {cyan}█▄█ {blue}██▄ {cyan}░█░ {blue}░█░ {cyan}█ {blue}█░▀█ {cyan}█▄█  {blue} ░█░ {cyan}█▄█ {blue}█▄█{cyan}  ║(●)║ ♫
{tab2}\t\t            {blue} ♪  ╚═══╝                                                                                       ╚═══╝  ♪
""")
        case "03004":
            print(f"""
{tab}\t       {white} ♪ ╔═══╗                                                                   ╔═══╗ ♪
{tab}\t       ♫  ║███║   {blue}{blue}░░█ {white}▄▄ {cyan}█░█ {blue}█▀█ {cyan}█▀█ {blue}█▀▀ {white}  ▄▄ {cyan}  █▄▄{blue} ▄▀█ {cyan}█▀ {blue}█▀▀  {cyan} █░░ {blue}█ {cyan}█▄░█ {blue}█▀▀{white}   ║███║  ♫
{tab}\t       {cyan} ♫ ║(O)║   {cyan}█▄█ ░░ {blue}█▀█ {cyan}█▄█ {blue}█▀▀ {cyan}██▄   ░░ {blue}  █▄█ {cyan}█▀█ {blue}▄█{cyan} ██▄  {blue} █▄▄ {cyan}█{blue} █░▀█{cyan} ██▄{cyan}   ║(●)║ ♫ 
{tab}\t      {blue} ♪  ╚═══╝                                                                   ╚═══╝  ♪
""")
        case "03005":
            print(f"""
{tab}\t          {white} ♪ ╔═══╗                                                              ╔═══╗ ♪
{tab}\t          ♫  ║███║   {blue}{white}▄▀{blue} █▀▀ {white}▀▄{cyan} █ {blue}█▀▄ {cyan}█░░ {blue}█▀▀  {white} ▄▄  {cyan} ▀█▀{blue} █▀█ {cyan}█▀▄▀█ {blue}█▄▄{cyan} █▀█ {blue}█▄█{white}   ║███║  ♫
{tab}\t          {cyan} ♫ ║(O)║   {white}▀▄ {cyan}█▄█{white} ▄▀ {blue}█ {cyan}█▄▀{blue} █▄▄ {cyan}██▄   ░░  {blue} ░█░ {cyan}█▄█ {blue}█░▀░█{cyan} █▄█ {blue}█▄█ {cyan}░█░{cyan}   ║(●)║ ♫ 
{tab}\t         {blue} ♪  ╚═══╝                                                              ╚═══╝  ♪
""")
        case "03006":
            print(f""" 
{tab2}\t\t\t         {white} ♪ ╔═══╗                                                                                ╔═══╗ ♪
{tab2}\t\t\t         ♫  ║███║   {blue}{blue}█▀▀{cyan} █░█{blue} █░█{cyan} █▄░█ {blue}█▀▀  {cyan} █░█ {blue}▄▀█  {white} ▄▄ {cyan}  ▄▀█ {blue}▀█▀  {cyan} ▀█▀ {blue}█░█ {cyan}█▀▀  {blue} █▀▀ {cyan}█▄░█{blue} █▀▄{white}   ║███║  ♫
{tab2}\t\t\t         {cyan} ♫ ║(O)║   {cyan}█▄▄ {blue}█▀█{cyan} █▄█ {blue}█░▀█ {cyan}█▄█  {blue} █▀█{cyan} █▀█   ░░  {blue} █▀█ {cyan}░█░  {blue} ░█░ {cyan}█▀█ {blue}██▄  {cyan} ██▄{blue} █░▀█ {cyan}█▄▀{cyan}   ║(●)║ ♫
{tab2}\t\t\t        {blue} ♪  ╚═══╝                                                                                ╚═══╝  ♪
""")
        case "03007":
            print(f""" 
{tab2}\t\t\t           {white} ♪ ╔═══╗                                                                           ╔═══╗ ♪
{tab2}\t\t\t           ♫  ║███║   {blue}{blue}█{cyan} █▄▀{blue} █▀█ {cyan}█▄░█  {white} ▄▄ {blue}  █░░{cyan} █▀█{blue} █░█{cyan} █▀▀  {blue} █▀ {cyan}█▀▀ {blue}█▀▀{cyan} █▄░█{blue} ▄▀█ {cyan}█▀█ {blue}█ {cyan}█▀█{white}   ║███║  ♫
{tab2}\t\t\t           {cyan} ♫ ║(O)║   {cyan}█{blue} █░█ {cyan}█▄█ {blue}█░▀█   ░░  {cyan} █▄▄ {blue}█▄█ {cyan}▀▄▀ {blue}██▄  {cyan} ▄█ {blue}█▄▄{cyan} ██▄{blue} █░▀█ {cyan}█▀█ {blue}█▀▄ {cyan}█ {blue}█▄█{cyan}   ║(●)║ ♫
{tab2}\t\t\t          {blue} ♪  ╚═══╝                                                                           ╚═══╝  ♪
""")
        case"03008":
                print(f"""
{tab}\t        {white} ♪ ╔═══╗                                                                 ╔═══╗ ♪
{tab}\t        ♫  ║███║  {blue}{blue}▀█▀{cyan} ▀▄▀ {blue}▀█▀  {white} ▄▄   {cyan} █░░{blue} █▀█{cyan} █▀{blue} █▀▀ {cyan}█▀█ {white}▀▀{blue} █░░{cyan} █▀█{blue} █░█ {cyan}█▀▀{blue} █▀█{white}  ║███║  ♫
{tab}\t        {cyan} ♫ ║(O)║  {cyan}░█░{blue} █░{cyan}█ {cyan}░█░ {white}  ░░   {blue} █▄▄{cyan} █▄█{blue} ▄█{cyan} ██▄{blue} █▀▄{white} ▀▀{cyan} █▄▄{blue} █▄█{cyan} ▀▄▀ {blue}██▄{cyan} █▀▄{cyan}  ║(●)║ ♫
{tab}\t       {blue} ♪  ╚═══╝                                                                 ╚═══╝  ♪
""")
        case "03009":
            print(f""" 
{tab2}\t\t\t             {white} ♪ ╔═══╗                                                                        ╔═══╗ ♪
{tab2}\t\t\t             ♫  ║███║  {blue}{blue}█▀█ {cyan}█▀▀ {blue}█▀▄ {cyan}  █░█ {blue}█▀▀ {cyan}█░░ {blue}█░█{cyan} █▀▀ {blue}▀█▀  {white} ▄▄  {cyan} █▀▀ {blue}█░█ {cyan}▀█▀ {blue}█░█ {cyan}█▀█ {blue}█▀▀{white}  ║███║  ♫
{tab2}\t\t\t             {cyan} ♫ ║(O)║  {cyan}█▀▄ {blue}██▄{cyan} █▄▀  {blue} ▀▄▀{cyan} ██▄{blue} █▄▄ {cyan}▀▄▀ {blue}██▄ {cyan}░█░   ░░  {blue} █▀░{cyan} █▄█ {blue}░█░{cyan} █▄█ {blue}█▀▄ {cyan}██▄{cyan}  ║(●)║ ♫
{tab2}\t\t\t            {blue} ♪  ╚═══╝                                                                        ╚═══╝  ♪
""")
        case "03010":
            print(f""" 
{tab}\t             {white} ♪ ╔═══╗                                                       ╔═══╗ ♪
{tab}\t             ♫  ║███║  {blue}{blue}█▀▀ {cyan}▄▀█ {blue}█░█ {cyan}█▀█  {white} ▄▄  {blue} █▀█{cyan} █░█ {blue}█▄░█ {cyan}█▄░█ {blue}█ {cyan}█▄░█ {blue}█▀▀{white}  ║███║  ♫
{tab}\t             {cyan} ♫ ║(O)║  {cyan}█▄█ {blue}█▀█ {cyan}█▀█ {blue}█▄█   ░░  {cyan} █▀▄ {blue}█▄█ {cyan}█░▀█ {blue}█░▀█{cyan} █{blue} █░▀█{cyan} █▄█{cyan}  ║(●)║ ♫
{tab}\t            {blue} ♪  ╚═══╝                                                       ╚═══╝  ♪
""")

def go_to_music_player():
    global currently_hovered_4queue, currently_hovered_4songList, current_page
    currently_hovered_4queue, currently_hovered_4songList, current_page = -1, 0, 1
    if song_queue.get_length():

        def get_lyrics(path: str) -> list:
            fillers = ("♪      ♫", "♪      ♬      ♩", "♩      ♪ " ,"♫      ♪      ♫")
            categories = ["PH", "Japan", "Korea"]
            path = path.split("/")
            path[1] = categories[int(path[2][1])-1]
            with open("/".join(path)) as f:
                temp_lyrics = f.readlines()
            lyrics = []
            blank_lines_count = 0
            for i in range(len(temp_lyrics)):
                if temp_lyrics[i].strip():
                    lyrics.append(temp_lyrics[i].strip())
                    blank_lines_count = 0
                else:
                    if blank_lines_count >= 1 and not temp_lyrics[i+1].strip():
                        lyrics.append(fillers[blank_lines_count-1])
                    else:
                        lyrics.append(temp_lyrics[i].strip())
                    blank_lines_count +=1
            return lyrics

        def get_upperAndlower_margin(lyrics_lines_num: int) -> tuple: 
            remaining_space = 32-lyrics_lines_num
            if not (remaining_space/2).is_integer(): upper_margin, lower_margin = math.ceil(remaining_space/2), math.ceil(remaining_space/2)-1
            else: upper_margin, lower_margin = remaining_space-(remaining_space//2), remaining_space-(remaining_space//2)
            return upper_margin, lower_margin

        def pause() -> None:
            global paused
            if paused:
                pygame.mixer.music.unpause()
                paused = False
            else:
                pygame.mixer.music.pause()
                paused = True

        def display_lyrics(line_2highlight: int, song_code: str, bar_sec: int, play_button = "█ █", marquee_space = 0) -> None:
            global highlighted_line_count, printed_song_count_4queue, instruction_counter, printed_instruction
            
            def print_song_from_queue(i : int):
                global printed_song_count_4queue, instruction_counter, printed_instruction
                if i == 0:
                    print(f"\t   {colors[highlighted_line_count]}║  {colors[highlighted_line_count-1]}𝐍 𝐎 𝐖   𝐏 𝐋 𝐀 𝐘 𝐈 𝐍 𝐆 :{reset}")
                elif i ==2:
                    print(f"\t   {colors[highlighted_line_count]}║  {colors[highlighted_line_count-1]}{'𝐔 𝐏  𝐍 𝐄 𝐗 𝐓 :'} {reset}")
                else:
                    if printed_song_count_4queue < song_queue.get_length():
                        print(f"\t   {colors[highlighted_line_count]}║{reset if i != 1 else w  if default_theme else queue_color if queue_color else reset}\t  {filtered_songsInQueue[printed_song_count_4queue]}{reset}")
                        printed_song_count_4queue+=1
                    else:  
                        color, color1 = colors[highlighted_line_count-1], colors[highlighted_line_count]
                        if printed_instruction < 4 and instruction_counter > 1:
                            keypress_instructions = [f"{color}SPACE - {color1}({reset}Pause/Resume{color1})", f"{color}N - {color1}({reset}Next Song{color1})",\
                                   f"{color}ESC - {color1}({reset}Back To Song List{color1})",f"{color}S - {color1}({reset}Shuffle{color1})"][printed_instruction]
                            printed_instruction+=1
                        else: 
                            keypress_instructions = f"{colors[highlighted_line_count]}"+f"{colors[highlighted_line_count]}{'𝐂 𝐎 𝐍 𝐓 𝐑 𝐎 𝐋 𝐒 :'}" if instruction_counter == 1 else " "
                        print(f"\t   {colors[highlighted_line_count]}║{reset if default_theme else queue_color if queue_color else reset}{'  ' if instruction_counter == 1 else '      '}{keypress_instructions}{reset}")
                        instruction_counter+=1

            def get_country_icon(song_code):
                with open(f"Country Icons/{song_code[:2]}.txt", encoding='UTF-8') as f:
                    return [line[:-1].replace("[[color]]", countryIcon_color[highlighted_line_count] if not default_theme else colors[highlighted_line_count]).replace("[[color1]]", countryIcon_color[-1]).replace("[[color3]]", colors[highlighted_line_count]\
                         if not default_theme and chosen_category != "All Songs" else colors[highlighted_line_count]) for line in f.readlines()]
                    
            if chosen_category == "PH" and not default_theme: 
                colors = [blue, fg(4)] ; countryIcon_color = [fg(3), fg(214), fg(202) ]
            elif chosen_category == "Korea" and not default_theme: 
                colors = [blue, cyan] ; countryIcon_color = [fg(196), fg(196), w ]
            elif chosen_category == "Japan"  and not default_theme: 
                colors = [r, red2] ; countryIcon_color = [fg(196), red2, w ]
            else: 
                colors = [g,fg(34)] 
                if chosen_category != "All Songs": countryIcon_color = [g, w]
                else: countryIcon_color = [g,fg(34),w] 

            if highlighted_line_count == 2: highlighted_line_count = 0
            os.system('cls')
            tab = "\t      " *8

            songs_in_queue = song_queue.get_elements()
            filtered_songsInQueue = []
            for song in songs_in_queue:
                temp_song_details = []
                for detail in song.split("  ")[:-1]:
                    if detail.strip() and not detail.strip().isnumeric():
                        temp_song_details+=[detail.strip()]
                filtered_songsInQueue+=[" - ".join(temp_song_details)]

            marquee_song = filtered_songsInQueue[1 if song_queue.get_length() > 1 else 0]
            print_song_title(song_code)
            left_parenthesis = f"{colors[highlighted_line_count]}( "
            print("\n"+" "*marquee_space, countryIcon_color[-1], \
                    f"{f'{left_parenthesis}{countryIcon_color[-1]}Next Song: ' if song_queue.get_length() > 1 else f'{left_parenthesis}{countryIcon_color[-1]}Now Playing: ' }"\
                    + colors[highlighted_line_count], marquee_song + f'{countryIcon_color[-1]} ){reset}', "\n\n")
            
            print(f"{tab}{colors[highlighted_line_count-1]}╔{'═'*(83)}╗{colors[highlighted_line_count]}\t   ╔═{reset}")
            country_icon = get_country_icon(song_code)
            for i in range(32):
                if i < upper_margin:
                    print(f"{country_icon[i] if i < len(country_icon) else tab}{colors[highlighted_line_count-1]}║  {' '.center(79)}  ║{colors[highlighted_line_count]}{reset}", end="")
                    print_song_from_queue(i)
                elif i < upper_margin+len(lyrics) :
                    if i-upper_margin==line_2highlight:
                        print(f"{ country_icon[i] if i < len(country_icon) else tab}{colors[highlighted_line_count-1]}║  {colors[highlighted_line_count]}{lyrics[line_2highlight].center(79)}  {colors[highlighted_line_count-1]}║{reset}", end="")
                    else:
                        if not lyrics[line_2highlight] and i-upper_margin == line_2highlight-1:
                            print(f"{country_icon[i] if i < len(country_icon) else tab}{colors[highlighted_line_count-1]}║{colors[highlighted_line_count]}  {lyrics[line_2highlight-1].center(79)} {reset} {colors[highlighted_line_count-1]}║{reset}", end="")
                        else:
                            print(f"{country_icon[i] if i < len(country_icon) else tab}{colors[highlighted_line_count-1]}║{reset}  {lyrics[i - upper_margin].center(79)}  {colors[highlighted_line_count-1]}║{reset}", end="")
                    print_song_from_queue(i)
                else:
                    print(f"{country_icon[i] if i < len(country_icon) else tab}{colors[highlighted_line_count-1]}║  {' '.center(79)}  ║{colors[highlighted_line_count]}{reset}", end="")
                    print_song_from_queue(i)
            printed_song_count_4queue = 0
            instruction_counter = 0
            printed_instruction = 0

            print(f"{tab}{colors[highlighted_line_count-1]}╚{'═'*(83)}╝{colors[highlighted_line_count]}\t   ╚═")

            display_musicPlayer_menu(play_button, colors[highlighted_line_count-1])
            print(f'{tab3}{border_color} ╚⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤╝{tab4}{sec_color}'+'{}'.format("0" if bar_sec < 60 else "1")+\
                        ":{}".format(f"0{bar_sec}" if bar_sec < 10 else bar_sec if bar_sec <60 else "00")+f' {bar_color}{x*bar_sec}{gray}{x*(60-bar_sec)}{reset}', end="\r")
            highlighted_line_count+=1
            
        global title, song_name, artist, song_code,lyrics, current_song, highlighted_line_count
        
        vocal_delays = {"02001": 4, "02002": 0, "02003": 0.5, "02004": 0.5, "02005": 0.7, "02006": 0.5, "02007": 0.3, "02008": 0, "02009": 0, "02010": 2.8, \
                            "03001": 0, "03002": 2, "03003": 2, "03004": 0.5, "03005": 0, "03006": 0, "03007": 1.3,"03008": 0, "03009": 0, "03010": 0,\
                            "01001": 0, "01002": 0, "01003": 0.8, "01004": 0, "01005": 0, "01006": 0, "01007": 0, "01008": 0, "01009": 0, "01010": 1}
        
        while song_queue.get_length():
            current_song = song_queue.get_elements()[0] #-------paaa
            song_code, artist, song_name, _ = [element.strip() for element in current_song.split("   ") if element]#------- sama pa rin
            title = "{}".format(f'{song_name:<50}')#-------
            lyrics = get_lyrics(f"Songs/{chosen_category}/{song_code}.txt") #-------
            upper_margin = get_upperAndlower_margin(len(lyrics))[0]
            os.system("cls")
            starting_time = time.time()
            play_song(f"Songs/{chosen_category}/{song_code}.mp3")
            display_lyrics(-1, song_code, 0)

            delay = 0
            while round(delay,1) != vocal_delays[song_code]:
                delay = time.time()-starting_time
                if keyboard.is_pressed("n"):
                    display_lyrics(-1, song_code, 0)
                    pygame.mixer.music.stop()
                    time.sleep(0.2)
                    song_queue.remove(current_song)
                    return go_to_music_player()
                if round(delay) in range(0,60):
                    print(f'{tab3}{border_color} ╚⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤╝{tab4}{sec_color}0:0{round(delay)} {bar_color}{x*round(delay)}{gray}{x*(60-round(delay))}{reset}', end="\r")
            
            bar_sec = 0
            lyrics_line_2highlight = 0
            song_wasPaused_4seekBar = False    
            marquee_space = 10

            while bar_sec <= 60:
                if lyrics_line_2highlight < len(lyrics):    
                    display_lyrics(lyrics_line_2highlight, song_code, bar_sec, "█ █", marquee_space = marquee_space )
                else:
                    lyrics_line_2highlight = len(lyrics)-1 
                    display_lyrics(lyrics_line_2highlight, song_code, bar_sec, "█ █", marquee_space = marquee_space)
                lyrics_starting_time = time.time()
                lyrics_time_delay = 0
                song_wasPaused_4lyrics = False
                while math.floor(lyrics_time_delay) != round(60/len(lyrics)):
                    if not song_wasPaused_4seekBar:     curr_bar_sec = time.time()-starting_time
                    else:                               curr_bar_sec = (time.time()-starting_time)+last_bar_sec
                    bar_sec = round(curr_bar_sec) 
                    if bar_sec <=60:
                        print(f'{tab3}{border_color} ╚⏤⏤⏤⏤⏤⏤⏤⏤⏤⏤╝{tab4}{sec_color}'+'{}'.format("0" if bar_sec < 60 else "1")+\
                        ":{}".format(f"0{bar_sec}" if bar_sec < 10 else bar_sec if bar_sec <60 else "00")+f' {bar_color}{x*bar_sec}{gray}{x*(60-bar_sec)}{reset}', end="\r")
                    if keyboard.is_pressed("space"):
                        display_lyrics(lyrics_line_2highlight, song_code, bar_sec, "███", marquee_space = marquee_space )
                        last_second, last_bar_sec = float(str(lyrics_time_delay)), float(str(curr_bar_sec))
                        pause()
                        time.sleep(0.2)
                        while not keyboard.is_pressed("space"):
                            pass
                        time.sleep(0.2)
                        song_wasPaused_4lyrics, song_wasPaused_4seekBar, new_lyrics_delay, starting_time = True, True , time.time(), time.time()
                        display_lyrics(lyrics_line_2highlight, song_code, bar_sec, "█ █", marquee_space = marquee_space)
                        pause()
                    elif keyboard.is_pressed("esc"):
                        display_lyrics(lyrics_line_2highlight, song_code, bar_sec, "███", marquee_space = marquee_space )
                        pygame.mixer.music.stop()
                        time.sleep(0.2)
                        return song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
                    elif keyboard.is_pressed("s") and song_queue.get_length() > 2:
                        song_queue.shuffle()
                        display_lyrics(lyrics_line_2highlight, song_code, bar_sec, "█ █", marquee_space = marquee_space)
                    elif keyboard.is_pressed("n"):
                        display_lyrics(lyrics_line_2highlight, song_code, bar_sec, "███", marquee_space = marquee_space )
                        pygame.mixer.music.stop()
                        time.sleep(0.2)
                        song_queue.remove(current_song)
                        return go_to_music_player()
                    if song_wasPaused_4lyrics:
                        lyrics_time_delay = (time.time()-new_lyrics_delay)+last_second
                    else: 
                        lyrics_time_delay = time.time()-lyrics_starting_time
                os.system('cls')
                lyrics_line_2highlight+=1
                if marquee_space != 170: marquee_space+=40
                else: marquee_space = 10
            song_queue.remove(current_song)    
        return song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)
    else:   
        return song_list_page.display_songList_page(currently_hovered_4songList = currently_hovered_4songList)


returned_value = display_main_menu()
if returned_value != "Exited":
    keyboard.add_hotkey('down', bring_down_hover_4songList_page)
    keyboard.add_hotkey('up', bring_up_hover_4songList_page)
    keyboard.add_hotkey('a', add_to_queue)
    keyboard.add_hotkey('backspace', remove_from_queue)
    keyboard.add_hotkey('right', view_songList_nextPage)
    keyboard.add_hotkey('left', view_songList_perviousPage)
    keyboard.add_hotkey('m', go_to_music_player)
    keyboard.add_hotkey('p', play_song_preview)
    keyboard.add_hotkey('esc', display_main_menu)
    keyboard.add_hotkey('x', display_theme_choices_or_thanksMessage)
    keyboard.wait("x")