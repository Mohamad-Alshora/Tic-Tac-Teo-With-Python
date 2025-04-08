import sys

def main():
    f = Game()
    f.play_game()

class Player:
    def __init__(self):
        self.name = '' 
        self.sympol = ''
    
    def choose_name(self, player):
        n = input(f'{player} Enter your name right here: ')
        self.name = n
        
    def choose_sympol(self):
        while True:
            sympol = f' {input(f'{self.name}, Enter your sympol right here (X or O): ').upper().strip()} '
            if sympol == ' X ' or sympol == ' O ':
                self.sympol = sympol
                break
            else:
                print('Please choice between (X and O)')

class Menu:
    def __init__(self):
        pass
    
    def display_main_menu(self):
        while True:
            print('''1. Start Game
2. Quit Game''')
            self.main_menu_user_choice = input('Enter your Choice (1 or 2): ').strip()
            if self.main_menu_user_choice == '1' or self.main_menu_user_choice == '2':
                return self.main_menu_user_choice
            print(f'you can just Enter 1 or 2')

    
    def display_endgame_menu(self):
        print('''1. Restart Game
2. Quit Game''')
        self.endgame_menu_user_choice = input('Enter your Choice (1 or 2): ').strip()
        if self.endgame_menu_user_choice == '1' or self.endgame_menu_user_choice == '2':
            return self.endgame_menu_user_choice
        print(f'you can just Enter 1 or 2')
        return ''

class Board:
    def __init__(self):
        self.board=[[' 1 ',' | ',' 2 ',' | ',' 3 '],
                    [' - ',' - ',' - ',' - ',' - '],
                    [' 4 ',' | ',' 5 ',' | ',' 6 '],
                    [' - ',' - ',' - ',' - ',' - '],
                    [' 7 ',' | ',' 8 ',' | ',' 9 ']]
        
    
    def display_board(self):
        for i in self.board:
            for n in i:
                print(n,end='')
            print('')
    
    def update_board(self, number, symbol):
        # Map the board position to the flat board index
        position_mapping = {
            '1': (0, 0), '2': (0, 2), '3': (0, 4),
            '4': (2, 0), '5': (2, 2), '6': (2, 4),
            '7': (4, 0), '8': (4, 2), '9': (4, 4)
        }

        row, col = position_mapping[number]
        if self.board[row][col] not in (' X ', ' O '):  # Check if the cell is empty
            self.board[row][col] = symbol
            return True
        else:
            print("Position already taken. Try again.")
            return False
    
    def reset_board(self):
        self.board=[[' 1 ',' | ',' 2 ',' | ',' 3 '],
                    [' - ',' - ',' - ',' - ',' - '],
                    [' 4 ',' | ',' 5 ',' | ',' 6 '],
                    [' - ',' - ',' - ',' - ',' - '],
                    [' 7 ',' | ',' 8 ',' | ',' 9 ']]

class Game:
    def __init__(self):
        self.board = Board()
        self.players = []
        self.menu = Menu()
        self.current_player_index = 0
    
    def start_game(self):
            self.user_choice = self.menu.display_main_menu()
            if len(self.user_choice) > 0:
                if self.user_choice == '2':
                    self.quit_game()
                elif self.user_choice == '1':
                    self.player1 = Player()
                    self.player2 = Player()
                    self.player1.choose_name('player1,')
                    self.player2.choose_name('player2,')
                    self.player1.choose_sympol()
                    if self.player1.sympol == ' X ':
                        self.player2.sympol = ' O '
                    else:
                        self.player2.sympol = ' X '
                    self.players.append(self.player1)
                    self.players.append(self.player2)
                    
    
    def play_game(self):
        self.start_game()
        while True:
            self.play_turn()
            if self.check_win() or self.check_draw():
                choice = self.menu.display_endgame_menu()
                if choice == '1' :
                    self.restart_game()
                elif choice == '2':
                    self.quit_game()
                    break
    
    def play_turn(self):
        self.board.display_board()
        self.player = self.players[self.current_player_index]
        print(f"{self.player.name}'s turn ({self.player.sympol})")
        while True:
            try:
                cell_choice = input(f'{self.player.name} Enter a number between 1 - 9: ')
                if cell_choice in [str(i) for i in range(1,10)]:
                    if self.board.update_board(cell_choice,self.player.sympol):
                        break
                else:
                    print('please Enter a number between 1 and 9 !!')
            except ValueError:
                print('Please Enter a number between 1 and 9 !!')
        self.switch_player()
        
    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index
        
    
    def check_draw(self):
        flat_board = [
            self.board.board[0][0], self.board.board[0][2], self.board.board[0][4],
            self.board.board[2][0], self.board.board[2][2], self.board.board[2][4],
            self.board.board[4][0], self.board.board[4][2], self.board.board[4][4]]
        
        if all(i in (' X ', ' O ') for i in flat_board):
            if not self.check_win():
                print('it\'s a draw')
                return True
            return True
    
    def append_player(self, player):
        self.players.append(player)
    
    def check_win(self):
        # Flatten the board for easier indexing 
        flat_board = [
            self.board.board[0][0], self.board.board[0][2], self.board.board[0][4],
            self.board.board[2][0], self.board.board[2][2], self.board.board[2][4],
            self.board.board[4][0], self.board.board[4][2], self.board.board[4][4]
        ]

        # Define winning combinations
        winning_combinations = [
            [0, 1, 2],  # Top row
            [3, 4, 5],  # Middle row
            [6, 7, 8],  # Bottom row
            [0, 3, 6],  # Left column
            [1, 4, 7],  # Middle column
            [2, 5, 8],  # Right column
            [0, 4, 8],  # Diagonal from top-left
            [2, 4, 6]   # Diagonal from top-right
        ]

        # Check for a win
        for combo in winning_combinations:
            if flat_board[combo[0]] == flat_board[combo[1]] == flat_board[combo[2]] and flat_board[combo[0]] in (' X ', ' O '):
                print(f"{self.player.name} '{flat_board[combo[0]]}' wins!")
                return True
        return False
    
    def restart_game(self):
        self.board.reset_board()
    
    def quit_game(self):
        print('Thank you for playing my Game :)')
        sys.exit()


if __name__ == '__main__':
    main()