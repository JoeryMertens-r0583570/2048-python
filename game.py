__author__ = 'Joery'
import tkinter
import math
import copy

from tkinter import messagebox


class Game( tkinter.Frame ):
    """
    2048 Game class.
    Handles keyboard listening and GUI for the 2048 game.  Still needs
    initialize, key_press and should_continue functions to work properly.
    You should not need to change anything in this file.
    """

    _tile_size = 128

    _background_color = "#cdc1b4"

    _colors = [
        ( "#eee4da", "#776e65" ),
        ( "#ede0c8", "#776e65" ),
        ( "#f2b179", "#f9f6f2" ),
        ( "#f59563", "#f9f6f2" ),
        ( "#f67c5f", "#f9f6f2" ),
        ( "#f65e3b", "#f9f6f2" ),
        ( "#edcf72", "#f9f6f2" ),
        ( "#edcc61", "#f9f6f2" ),
        ( "#edc850", "#f9f6f2" ),
        ( "#edc53f", "#f9f6f2" ),
        ( "#edc22e", "#f9f6f2" ),
        ( "#3c3a32", "#f9f6f2" )
    ]

    def __init__(self, initialize, key_press, should_continue,  master = tkinter.Tk(), dimension = 4 ):
        """
        Create a new game object
        :param initialize: student provided initialisation function
        :param key_press: student provided key_press function
        :param should_continue: student provided should_continue function
        :param master: Tk master pane
        :param dimension: game dimension
        :return: new game
        """
        tkinter.Frame.__init__( self, master )
        self._master = master
        self._master.title( "2048" )
        self._initialize = initialize
        self._key_press = key_press
        self._should_continue = should_continue
        self._dimension = dimension


    def play(self):
        """
        Starts the game play.
        """
        self._score = 0
        self._board = self._initialize( self._dimension )
        self._build_gui()
        self._setup_keyboard()
        self._update_gui()
        self._master.mainloop()

    def _setup_keyboard(self):
        """
        Bind the keyboard listeners.  Up, down, left and right keys are bound to
        keyboard_callback method.
        """
        self.bind_all( "<Up>", lambda e: self.keyboard_callback( e.keysym ) )
        self.bind_all( "<Down>", lambda e: self.keyboard_callback( e.keysym ) )
        self.bind_all( "<Left>", lambda e: self.keyboard_callback( e.keysym ) )
        self.bind_all( "<Right>", lambda e: self.keyboard_callback( e.keysym ) )

    def _pick_color(self, value):
        """
        Return suitable colors to style a square based on its value
        :param value: square's value
        :type value: int
        :return: tuple with background and foreground color
        :rtype ( String, String )
        """
        if value is None:
            return ( self._background_color, None )
        index = int( max( 0, min( len( self._colors ), math.log( value, 2 ) ) - 1 ) )
        return self._colors[ index ]

    def _update_gui(self):
        """
        Updates the GUI by updating all tile values and the score
        """
        def int_to_str( entry ):
            if entry is None:
                return ""
            else:
                return "%i" % entry

        for i in range( self._dimension ):
            for j in range( self._dimension ):
                colors = self._pick_color( self._board[i][j] )
                self._boxes[i][j].config( anchor = "center", text = int_to_str( self._board[i][j] ), bg = colors[0], fg = colors[1], font = "Helvetica 68 bold" )

        self._score_widget.config( text = "Score: %i" % self._score )

    def keyboard_callback(self, direction ):
        """
        Handle a keyboard event
        :param direction: Keyboard symbol pressed (Up, Down, Left or Right)
        :type direction: String
        """
        self._board, self._score = self._key_press( copy.deepcopy( self._board ), self._score, direction )
        self._update_gui()
        if not self._should_continue( self._board ):
            self.gameover()

    def _build_gui(self):
        """
        Build the GUI
        Adds a label for the score.  Creates a matrix with labels for all boxes.
        The labels of the boxes are wrapped in a frame to ensure they can be made square.
        """
        frame = tkinter.Frame( self._master, bg = "#bbada0" )
        frame.grid( stick = "nsew" )

        self._score_widget = tkinter.Label( frame, text = "Score: 0", font = "Helvetica 72 bold", fg = "#776e6d", bg = "#faf8ef" )
        self._score_widget.grid( row = 0, column = 0, columnspan = self._dimension, sticky = tkinter.W + tkinter.E + tkinter.S + tkinter.N, padx = 10, pady = 10 )

        self._boxes = []
        for i in range( self._dimension ):
            row = []
            for j in range( self._dimension ):
                row.append( self._build_block( frame, i, j ) )
            self._boxes.append( row )

    def _build_block(self, parent, x, y ):
        """
        Build the GUI block at column x and row y.
        :param parent: parent frame
        :param x: column
        :type x: int
        :param y: row
        :type y: int
        :return: label, wrapped in a frame positioned at x, y + 1 in the grid
        :rtype: tkinter.Label
        """
        frame = tkinter.Frame( parent, width = self._tile_size, height = self._tile_size )
        label = tkinter.Label( frame, text = "0", background = self._background_color )
        frame.grid_propagate( False )
        frame.columnconfigure( 0, weight = 1 )
        frame.rowconfigure(0, weight = 1 )
        frame.grid( row = y + 1, column = x, padx = 10, pady = 10 )
        label.grid( sticky = "wens" )
        return label

    def gameover(self):
        """
        Indicate to the user the game is over and quit the programm.
        """
        messagebox.showinfo( "Game over", "No more moves left!  You reached a score of %i" % self._score )
        self.quit()