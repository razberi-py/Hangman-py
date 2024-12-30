import random
import os
import time
import sys

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Colorama module not found. Please install it using 'pip install colorama'")
    exit()

# Color constants
RED = Fore.RED
GREEN = Fore.GREEN
BLUE = Fore.BLUE
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
RESET = Fore.RESET

# Box drawing characters
BOX_TOP_LEFT = '╔'
BOX_TOP_RIGHT = '╗'
BOX_BOTTOM_LEFT = '╚'
BOX_BOTTOM_RIGHT = '╝'
BOX_HORIZONTAL = '═'
BOX_VERTICAL = '║'
BOX_T_HORIZONTAL = '╦'
BOX_T_VERTICAL = '╩'
BOX_CROSS = '╬'
BOX_LEFT_T = '╠'
BOX_RIGHT_T = '╣'

# Improved Hangman ASCII art stages
hangman_stages = [
    '''
       _______
      |     |
      |     
      |    
      |    
      |    
    __|__
    ''',
    '''
       _______
      |     |
      |     O
      |    
      |    
      |    
    __|__
    ''',
    '''
       _______
      |     |
      |     O
      |     |
      |    
      |    
    __|__
    ''',
    '''
       _______
      |     |
      |     O
      |    /|
      |    
      |    
    __|__
    ''',
    '''
       _______
      |     |
      |     O
      |    /|\\
      |    
      |    
    __|__
    ''',
    '''
       _______
      |     |
      |     O
      |    /|\\
      |    / 
      |    
    __|__
    ''',
    '''
       _______
      |     |
      |     O
      |    /|\\
      |    / \\
      |    
    __|__
    '''
]

# Word lists
word_list_easy = [
    'apple', 'ball', 'cat', 'dog', 'egg', 'fish', 'goat', 'hat', 'ice', 'jam',
    'kite', 'lion', 'moon', 'nose', 'owl', 'pig', 'queen', 'rose', 'sun', 'tree',
    'van', 'wolf', 'xray', 'yak', 'zebra', 'bag', 'cake', 'duck', 'ear', 'frog',
    'gate', 'house', 'ink', 'jug', 'key', 'lamp', 'mouse', 'nest', 'orange', 'panda',
    'quill', 'rat', 'snake', 'tiger', 'vase', 'whale', 'yoyo', 'zip', 'ant', 'bird',
    'cow', 'drum', 'eel', 'flag', 'guitar', 'horse', 'igloo', 'jelly', 'kangaroo',
    'lemon', 'monkey', 'needle', 'octopus', 'pencil', 'quilt', 'rabbit', 'ship',
    'train', 'unicorn', 'violin', 'window', 'zoo', 'air', 'boat', 'cloud', 'doll',
    'engine', 'feather', 'garden', 'hammer', 'island', 'juice', 'king', 'leaf',
    'mirror', 'note', 'ocean', 'pumpkin', 'rain', 'star', 'turtle', 'umbrella',
    'vulture', 'water', 'xenon', 'yacht', 'zero'
]

word_list_medium = [
    'python', 'hangman', 'computer', 'programming', 'keyboard', 'monitor', 'laptop',
    'function', 'variable', 'integer', 'string', 'boolean', 'syntax', 'compiler',
    'interpreter', 'algorithm', 'array', 'dictionary', 'tuple', 'conditional',
    'iteration', 'loop', 'recursion', 'parameter', 'argument', 'exception', 'file',
    'class', 'object', 'method', 'attribute', 'inheritance', 'encapsulation',
    'polymorphism', 'abstraction', 'module', 'package', 'import', 'lambda', 'decorator',
    'generator', 'comprehension', 'operator', 'expression', 'statement', 'bytecode',
    'debugger', 'virtual', 'environment', 'repository', 'branch', 'commit', 'merge',
    'clone', 'fork', 'pull', 'push', 'issue', 'request', 'socket', 'server', 'client',
    'protocol', 'network', 'database', 'query', 'index', 'schema', 'table', 'record',
    'column', 'row', 'primary', 'foreign', 'normalization', 'transaction', 'backup',
    'restore', 'encryption', 'authentication', 'authorization', 'session', 'cookie',
    'cache', 'thread', 'process', 'concurrency', 'parallelism', 'asynchronous',
    'synchronous', 'mutex', 'semaphore', 'deadlock', 'latency', 'bandwidth'
]

word_list_hard = [
    'xylophone', 'quizzical', 'juxtaposition', 'kaleidoscope', 'pneumonia',
    'onomatopoeia', 'synecdoche', 'schizophrenia', 'mnemonic', 'triskaidekaphobia',
    'hemorrhage', 'phlegmatic', 'zephyr', 'quorum', 'xenophobia', 'laryngitis',
    'rhythm', 'sphinx', 'awkward', 'buffoon', 'cobweb', 'espionage', 'gazebo',
    'haiku', 'iatrogenic', 'jazz', 'klutz', 'lymph', 'mystify', 'naphtha',
    'ostracize', 'pajama', 'quartz', 'rhubarb', 'schnapps', 'tsunami', 'vortex',
    'waltz', 'xenon', 'yippee', 'zodiac', 'affix', 'banjo', 'crypt', 'dwarves',
    'embezzle', 'fervid', 'galaxy', 'haphazard', 'injury', 'jackpot', 'kayak',
    'luxury', 'microwave', 'nightclub', 'oxygen', 'pneumatic', 'queue', 'rickshaw',
    'stretch', 'topaz', 'unzip', 'vodka', 'whiskey', 'youthful', 'zigzag', 'absurd',
    'blizzard', 'cycle', 'dizzying', 'equip', 'gossip', 'icebox', 'jockey', 'khaki',
    'lengths', 'megahertz', 'nowadays', 'oxidize', 'puzzling', 'quizzes', 'rhythmic',
    'scratch', 'thumbscrew', 'vaporize', 'wellspring', 'xenophobia', 'yachtsman', 'zealous'
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_boxed_message(message, color=RESET):
    lines = message.split('\n')
    width = max(len(line) for line in lines) + 4
    border_top = BOX_TOP_LEFT + BOX_HORIZONTAL * (width - 2) + BOX_TOP_RIGHT
    border_bottom = BOX_BOTTOM_LEFT + BOX_HORIZONTAL * (width - 2) + BOX_BOTTOM_RIGHT
    print(color + border_top)
    for line in lines:
        print(color + BOX_VERTICAL + ' ' + line.ljust(width - 4) + ' ' + BOX_VERTICAL)
    print(color + border_bottom + RESET)

def main_menu():
    while True:
        clear_screen()
        title = 'Welcome to Hangman!'
        print_boxed_message(title, YELLOW)
        print('\n' + BOX_LEFT_T + BOX_HORIZONTAL * 28 + BOX_RIGHT_T)
        print(BOX_VERTICAL + ' 1. Play Game                ' + BOX_VERTICAL)
        print(BOX_VERTICAL + ' 2. View High Scores         ' + BOX_VERTICAL)
        print(BOX_VERTICAL + ' 3. Exit                     ' + BOX_VERTICAL)
        print(BOX_BOTTOM_LEFT + BOX_HORIZONTAL * 28 + BOX_BOTTOM_RIGHT)
        choice = input('Enter your choice: ')
        if choice == '1':
            play_game()
        elif choice == '2':
            view_high_scores()
        elif choice == '3':
            print('Thank you for playing!')
            break
        else:
            print(RED + 'Invalid choice. Please try again.')
            time.sleep(2)

def play_game():
    while True:
        clear_screen()
        title = 'Select Game Mode:'
        print_boxed_message(title, CYAN)
        print('\n' + BOX_LEFT_T + BOX_HORIZONTAL * 28 + BOX_RIGHT_T)
        print(BOX_VERTICAL + ' 1. Single Player            ' + BOX_VERTICAL)
        print(BOX_VERTICAL + ' 2. Two Player               ' + BOX_VERTICAL)
        print(BOX_VERTICAL + ' 3. Party Mode               ' + BOX_VERTICAL)
        print(BOX_VERTICAL + ' 4. Back to Main Menu        ' + BOX_VERTICAL)
        print(BOX_BOTTOM_LEFT + BOX_HORIZONTAL * 28 + BOX_BOTTOM_RIGHT)
        choice = input('Enter your choice: ')
        if choice == '1':
            single_player()
            break
        elif choice == '2':
            two_player()
            break
        elif choice == '3':
            party_mode()
            break
        elif choice == '4':
            break
        else:
            print(RED + 'Invalid choice. Please try again.')
            time.sleep(2)

def single_player():
    while True:
        clear_screen()
        title = 'Select Difficulty Level:'
        print_boxed_message(title, GREEN)
        print('\n' + BOX_LEFT_T + BOX_HORIZONTAL * 28 + BOX_RIGHT_T)
        print(BOX_VERTICAL + ' 1. Easy                     ' + BOX_VERTICAL)
        print(BOX_VERTICAL + ' 2. Medium                   ' + BOX_VERTICAL)
        print(BOX_VERTICAL + ' 3. Hard                     ' + BOX_VERTICAL)
        print(BOX_VERTICAL + ' 4. Back to Game Mode        ' + BOX_VERTICAL)
        print(BOX_BOTTOM_LEFT + BOX_HORIZONTAL * 28 + BOX_BOTTOM_RIGHT)
        choice = input('Enter your choice: ')
        if choice == '1':
            word = random.choice(word_list_easy).lower()
            start_game(word, 'Easy')
            break
        elif choice == '2':
            word = random.choice(word_list_medium).lower()
            start_game(word, 'Medium')
            break
        elif choice == '3':
            word = random.choice(word_list_hard).lower()
            start_game(word, 'Hard')
            break
        elif choice == '4':
            break
        else:
            print(RED + 'Invalid choice. Please try again.')
            time.sleep(2)

def two_player():
    clear_screen()
    title = 'Two Player Mode'
    print_boxed_message(title, MAGENTA)
    print('Player 1, please enter the word for Player 2 to guess.')
    word = mask_input('Enter word: ').lower()
    print('Word set. Press Enter to continue.')
    input()
    start_game(word, 'Two Player')

def party_mode():
    clear_screen()
    title = 'Party Mode'
    print_boxed_message(title, BLUE)
    print('Welcome to Party Mode!')
    num_players = input('Enter the number of players: ')
    try:
        num_players = int(num_players)
        if num_players < 2:
            print(RED + 'Party Mode requires at least 2 players.')
            time.sleep(2)
            return
    except ValueError:
        print(RED + 'Please enter a valid number.')
        time.sleep(2)
        return
    players = []
    for i in range(1, num_players + 1):
        name = input(f'Enter name for Player {i}: ')
        players.append(name)
    current_player = 0
    while True:
        clear_screen()
        setter = players[current_player]
        guesser = players[(current_player + 1) % num_players]
        print_boxed_message(f"{setter}'s turn to set the word for {guesser}", YELLOW)
        word = mask_input(f'{setter}, please enter a word: ').lower()
        print('Word set. Press Enter to continue.')
        input()
        start_game(word, 'Party Mode', guesser)
        current_player = (current_player + 1) % num_players
        cont = input('Do you want to continue playing Party Mode? (yes/no): ').lower()
        if cont != 'yes':
            break

def mask_input(prompt):
    """Function to mask input with asterisks (*) as the user types."""
    print(prompt, end='', flush=True)
    pwd = ''
    while True:
        ch = getch()
        if ch == '\r' or ch == '\n':
            print('')
            break
        elif ch == '\b' or ord(ch) == 127:
            if len(pwd) > 0:
                pwd = pwd[:-1]
                print('\b \b', end='', flush=True)
        else:
            pwd += ch
            print('*', end='', flush=True)
    return pwd

def getch():
    """Read a single character from standard input without echo."""
    if os.name == 'nt':
        import msvcrt
        ch = msvcrt.getch().decode('utf-8', 'ignore')
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def start_game(word, difficulty='Easy', player_name='Player'):
    max_attempts = len(hangman_stages) - 1  # Max attempts based on hangman stages
    wrong_attempts = 0
    guessed_letters = []
    word_display = ['_' if letter.isalpha() else letter for letter in word]
    score = 0
    start_time = time.time()
    # Calculate hints based on word length
    max_hints = min(5, len(set(word)) // 2)  # Maximum of 5 hints
    hints_used = 0

    while wrong_attempts <= max_attempts:
        clear_screen()
        header = f'Hangman Game - {difficulty}'
        if player_name != 'Player':
            header += f" - {player_name}'s Turn"
        print_boxed_message(header, YELLOW)
        print(hangman_stages[wrong_attempts])
        print('\n' + BOX_TOP_LEFT + BOX_HORIZONTAL * (len(word_display)*2 + 2) + BOX_TOP_RIGHT)
        print(BOX_VERTICAL + ' ' + ' '.join(word_display) + ' ' + BOX_VERTICAL)
        print(BOX_BOTTOM_LEFT + BOX_HORIZONTAL * (len(word_display)*2 + 2) + BOX_BOTTOM_RIGHT)
        print('\nGuessed Letters: ' + ', '.join(sorted(guessed_letters)))
        print(f'Hints Used: {hints_used}/{max_hints}')
        print(f'Attempts Left: {max_attempts - wrong_attempts}')
        guess = input('Enter a letter, guess the word, or type "hint": ').lower()

        if guess == 'hint':
            if hints_used < max_hints:
                hints_used += 1
                score -= 15  # Reduce score for using a hint
                # Reveal a random unguessed letter
                unguessed_letters = [letter for letter in set(word) if letter not in guessed_letters]
                if unguessed_letters:
                    hint_letter = random.choice(unguessed_letters)
                    print('Hint: The word contains the letter "{}".'.format(hint_letter))
                    time.sleep(2)
                else:
                    print('No more hints available.')
                    time.sleep(2)
            else:
                print('You have used all your hints.')
                time.sleep(2)
        elif len(guess) == 1:
            if not guess.isalpha():
                print(RED + 'Please enter a valid letter.')
                time.sleep(2)
            elif guess in guessed_letters:
                print(RED + 'You have already guessed that letter.')
                time.sleep(2)
            elif guess in word:
                print(GREEN + 'Good guess!')
                guessed_letters.append(guess)
                score += 10  # Increase score for correct guess
                for idx, letter in enumerate(word):
                    if letter == guess:
                        word_display[idx] = guess
                if '_' not in word_display:
                    end_time = time.time()
                    total_time = end_time - start_time
                    print(GREEN + 'Congratulations! You have guessed the word correctly!')
                    print('Your score: {}'.format(score))
                    print('Time taken: {:.2f} seconds'.format(total_time))
                    if difficulty not in ['Two Player', 'Party Mode']:
                        save_high_score(score, difficulty, total_time)
                    time.sleep(2)
                    break
            else:
                print(RED + 'Wrong guess!')
                guessed_letters.append(guess)
                wrong_attempts += 1
                score -= 5  # Decrease score for wrong guess
                time.sleep(2)
        else:
            if guess == word:
                end_time = time.time()
                total_time = end_time - start_time
                print(GREEN + 'Congratulations! You have guessed the word correctly!')
                score += 50  # Bonus for guessing the word
                print('Your score: {}'.format(score))
                print('Time taken: {:.2f} seconds'.format(total_time))
                if difficulty not in ['Two Player', 'Party Mode']:
                    save_high_score(score, difficulty, total_time)
                time.sleep(2)
                break
            else:
                print(RED + 'Wrong guess!')
                wrong_attempts += 1
                score -= 5  # Decrease score for wrong guess
                time.sleep(2)
        if wrong_attempts > max_attempts:
            clear_screen()
            print_boxed_message('Game Over!', RED)
            print(hangman_stages[-1])
            print('\nThe word was: ' + word)
            print('Your score: {}'.format(score))
            time.sleep(3)
            break

def save_high_score(score, difficulty, total_time):
    name = input('Enter your name for the high score table: ')
    high_score_entry = '{}\t{}\t{}\t{:.2f}\t{}'.format(
        name, score, difficulty, total_time, time.strftime('%Y-%m-%d %H:%M:%S')
    )
    with open('highscores.txt', 'a') as f:
        f.write(high_score_entry + '\n')
    print('High score saved!')

def view_high_scores():
    clear_screen()
    title = 'High Scores'
    print_boxed_message(title, CYAN)
    if os.path.exists('highscores.txt'):
        with open('highscores.txt', 'r') as f:
            lines = f.readlines()
            if not lines:
                print('No high scores yet.')
            else:
                print('Name\tScore\tDifficulty\tTime(s)\tDate')
                print('-' * 60)
                for line in lines:
                    print(line.strip())
    else:
        print('No high scores yet.')
    input('\nPress Enter to return to the main menu.')

if __name__ == '__main__':
    main_menu()
