#-------------------------------------------------------------------------------
# Pyramid (Solitaire)
#
# Created:      June+July 2016
# Copyright:    (c) Chris Nielsen 2016
# To Do:
    #   1. Need animated cards on removal
    #   2. Sound effects
    #   3. Deal button should not appear before making sure there are no matches in the pyramid also.
    #       It is possible that there are matches in the pyramid, and we don't want the dealer button to appear pre-maturely.
    #    http://stackoverflow.com/questions/14044147/animated-sprite-from-few-images

#-------------------------------------------------------------------------------
"""To Do:
1. Place the deal button so that it better covers the draw button. DONE
2. Add a better buffer around the text cards DONE
7. Fix the word-word concatenation problem. Replace so that it is word- word. DONE
----------
cleared_row_sound now working yet

3. New graphics for the discard and draw pile placeholders
4. New graphic for the draw button
5. Add sounds
6. Mouseover cards allows the player to see the full verse text at the top
7. New exciting gray background
8. Mouseover button has an effect
9. Random King name for each new board
0. Keep track of stats in the background (per user)
1. User login screen.
2. End of game stats
3. Animations for removed cards
4. Highlight the cards that are selected
5. New rounded border card graphics with drop shadows
6. The last card played on the draw pile should not automatically reload from the discard pile



"""

import pygame, sys
from pygame.locals import *
from random import shuffle

exclude = []

pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (220,220,220)
DARK_GREY = (190,190,190)
DARKER_GREY = (140,140,140)
CHARCOAL = (50,50,50)

white = (255,255,255)
gray = (230,230,230)
black = (0,0,0)

# Define a deck of cards
deckofcards = [ "AH", "KH", "QH", "JH", "10H", "9H", "8H", "7H", "6H", "5H", "4H", "3H", "2H",
                "AS", "KS", "QS", "JS", "10S", "9S", "8S", "7S", "6S", "5S", "4S", "3S", "2S",
                "AD", "KD", "QD", "JD", "10D", "9D", "8D", "7D", "6D", "5D", "4D", "3D", "2D",
                "AC", "KC", "QC", "JC", "10C", "9C", "8C", "7C", "6C", "5C", "4C", "3C", "2C" ]


mainSurface_width = 1600
mainSurface_height = 950
mainSurface = pygame.display.set_mode((mainSurface_width, mainSurface_height), 0, 32)
mainSurface.fill((gray))
pygame.display.update()


bg = pygame.image.load("C:\Python27\images\green_felt.jpg").convert()
bg = pygame.image.load(r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\gray_bg.jpg').convert()
mainSurface.blit(bg, (0, 0)) #Display image at 0, 0

# Sounds
card_select_sound = pygame.mixer.Sound(r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\assets\click9.wav')             # works
match_sound = pygame.mixer.Sound(r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\assets\match1.wav')                   # works
mismatch_sound = pygame.mixer.Sound(r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\assets\match6.wav')                # not used
draw_sound = pygame.mixer.Sound(r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\assets\click11.wav')                   # works
repopulate_draw_pile_sound = pygame.mixer.Sound(r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\assets\click1.wav')    # works
new_board_sound = pygame.mixer.Sound(r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\assets\shuffle_new_board.wav')
cleared_row_sound = pygame.mixer.Sound(r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\assets\match3.wav')
cleared_board_sound = pygame.mixer.Sound(r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\assets\finish_board1.wav')

# Fonts
##font = pygame.font.SysFont("Courier", 14)
font2 = pygame.font.SysFont("Courier", 20)

font = pygame.font.Font(r"C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Fonts\Roboto\Roboto-Medium.ttf", 14)
bold_font = pygame.font.Font(r"C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Fonts\Roboto\Roboto-Bold.ttf", 15)

score = 0
deals = 2
boards = 0

##score_boards_deals()

pygame.display.flip()   #Update screen


pygame.display.set_caption("Pyramid")
clock = pygame.time.Clock()

##current_deck = pygame.sprite.Group()
current_deck = pygame.sprite.LayeredUpdates()
discard_pile = pygame.sprite.LayeredUpdates()

# ---------------------------------------

class card(pygame.sprite.Sprite):
    def __init__(self, pyramidloc, suitandrank, intval, x, y, text, center_flag):
        pygame.sprite.Sprite.__init__(self)
        self.suitandrank = suitandrank
        try:
            if suitandrank.startswith('K'):
                imagepath = r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\assets\new_card_184x299_king.jpg'
                self.image = pygame.image.load(imagepath)   # Gives the sprite a graphic image
            else:
                imagepath = r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\assets\blank_card_184x299.jpg'
                self.image = pygame.image.load(imagepath)   # Gives the sprite a graphic image
        except:
            self.image = pygame.image.load(r'C:\Python27\images\AHtan.jpg') # Default image
        self.rect = self.image.get_rect()                   # Gets the rect size from the image
        self.rect.x = x                                     # Sets the screen position of the rect
        self.rect.y = y                                     # Sets the screen position of the rect

        self.pyramidloc = pyramidloc
        self.intval = intval
        if text:
            self.text = text
        else:
            self.text = ''
        self.center_flag = center_flag
        self.top = y
        self.left = x

        self.surface_width = 8 * 23         # 184
        self.surface_height = 13 * 23        # 299

        if "bottom_" in self.pyramidloc:
            self._layer = 7
        if "rowofsix_" in self.pyramidloc:
            self._layer = 6
        if "rowoffive_" in self.pyramidloc:
            self._layer = 5
        if "rowoffour_" in self.pyramidloc:
            self._layer = 4
        if "rowofthree_" in self.pyramidloc:
            self._layer = 3
        if "rowoftwo_" in self.pyramidloc:
            self._layer = 2
        if "toprow" in self.pyramidloc:
            self._layer = 1
        if "dp" in self.pyramidloc:     # draw pile
            self._layer = 0

        self.surface_top = int(self.top)
        self.surface_left = int(self.left)
        self.addText(self.text, center_flag)

        self.border_rectangle = pygame.draw.rect(self.image, (black), (0, 0, self.surface_width, self.surface_height), 1)


    def addText(self, text_string, center):
        """mainSurface.blit(self.font.render(text_string, True, (R,G,B)), (Distance from left of screen, Distance from top of screen))"""

        self.text_string = text_string
        line_space = 20                             # how much vertical space to allow for each line of text
        self.left_offset = 7                        # Create a text left offset so that the text is not right on the rect border
        self.top_offset =  40                       # Create a top space offset so that the text does not start at the very top

        if center == 1:
            centered_line = self.center_text(text_string)
        else:
            wrapped_lines = self.wrap_text(text_string)
            if len(wrapped_lines) > 1:
                for line in wrapped_lines:
                    self.text_box = font.render(line, True, (0,0,0))
##                    self.image.blit(self.text_box, (0,0))
                    self.image.blit(self.text_box, (self.left_offset, self.top_offset))
                    self.top_offset += line_space
            else:
                self.text_box = font.render(text_string, True, (0,0,0))
##                self.image.blit(self.text_box, (0,0))
                self.image.blit(self.text_box, (self.left_offset, self.top_offset))

    def center_text(self, text_string):
        """Center and bold this text."""
        card_border = 5
        text_width = bold_font.size(text_string)[0]
        half_text_width = text_width / 2

        rect_width = self.surface_width - card_border
        text_container = self.rect
        text_container_center = rect_width / 2
        string_len = len(text_string)

        self.text_box = bold_font.render(text_string, True, (0,0,0))
        self.image.blit(self.text_box, (text_container_center - half_text_width, self.top_offset))

        print "\nText:", text_string
        print "Text width:", text_width
        print "half_text_width:", half_text_width
        print "String length:", string_len
        print "Surface width:", rect_width
        print "text_container:", text_container
        print "text_container_center:", text_container_center

        return text_string


    def wrap_text(self, text_string):
        """Wrap text to fit inside a given width when rendered.
        :param text_string: The text to be wrapped.
        :param font: The font the text will be rendered in.
        :param self.surface_width: The width to wrap to.
        """
        card_border = 10
        text_lines = text_string.replace('\t', '    ').replace('-', '- ').split('\n')
        if self.surface_width is None or self.surface_width == 0:
            return text_lines

        wrapped_lines = []
        for line in text_lines:
            line = line.rstrip() + ' '
            if line == ' ':
                wrapped_lines.append(line)
                continue

            # Get the leftmost space ignoring leading whitespace
            start = len(line) - len(line.lstrip())
            start = line.index(' ', start)
            while start + 1 < len(line):
                # Get the next potential splitting point
                next = line.index(' ', start + 1)
                if font.size(line[:next])[0] <= self.surface_width - card_border:
                    start = next
                else:
                    wrapped_lines.append(line[:start])
                    line = line[start+1:]
                    start = line.index(' ')
            line = line[:-1]
            if line:
                wrapped_lines.append(line)

        print "text_string:", text_string
        print "text_lines:", text_lines
        print "wrapped_lines:", wrapped_lines

        return wrapped_lines


# ---------------------------------------

def instantiateAllDefaultcards():
    # Create all card instances with default values

    global toprow
    global rowoftwo_1, rowoftwo_2
    global rowofthree_1, rowofthree_2, rowofthree_3
    global rowoffour_1, rowoffour_2, rowoffour_3, rowoffour_4
    global rowoffive_1, rowoffive_2, rowoffive_3, rowoffive_4, rowoffive_5
    global rowofsix_1, rowofsix_2, rowofsix_3, rowofsix_4, rowofsix_5, rowofsix_6
    global bottom_1, bottom_2, bottom_3, bottom_4, bottom_5, bottom_6, bottom_7
    global dp1, dp2, dp3, dp4, dp5, dp6, dp7, dp8, dp9, dp10, dp11, dp12, dp13, dp14, dp15, dp16, dp17, dp18, dp19, dp20, dp21, dp22, dp23, dp24

    toprow          = card("toprow", "", 0, 0, 0, '', 0)
    rowoftwo_1      = card("rowoftwo_1", "", 0, 0, 0, '', 0)
    rowoftwo_2      = card("rowoftwo_2", "", 0, 0, 0, '', 0)
    rowofthree_1    = card("rowofthree_1", "", 0, 0, 0, '', 0)
    rowofthree_2    = card("rowofthree_2", "", 0, 0, 0, '', 0)
    rowofthree_3    = card("rowofthree_3", "", 0, 0, 0, '', 0)
    rowoffour_1     = card("rowoffour_1", "", 0, 0, 0, '', 0)
    rowoffour_2     = card("rowoffour_2", "", 0, 0, 0, '', 0)
    rowoffour_3     = card("rowoffour_3", "", 0, 0, 0, '', 0)
    rowoffour_4     = card("rowoffour_4 ", "", 0, 0, 0, '', 0)
    rowoffive_1     = card("rowoffive_1", "", 0, 0, 0, '', 0)
    rowoffive_2     = card("rowoffive_2", "", 0, 0, 0, '', 0)
    rowoffive_3     = card("rowoffive_3", "", 0, 0, 0, '', 0)
    rowoffive_4     = card("rowoffive_4", "", 0, 0, 0, '', 0)
    rowoffive_5     = card("rowoffive_5", "", 0, 0, 0, '', 0)
    rowofsix_1      = card("rowofsix_1", "", 0, 0, 0, '', 0)
    rowofsix_2      = card("rowofsix_2", "", 0, 0, 0, '', 0)
    rowofsix_3      = card("rowofsix_3", "", 0, 0, 0, '', 0)
    rowofsix_4      = card("rowofsix_4", "", 0, 0, 0, '', 0)
    rowofsix_5      = card("rowofsix_5", "", 0, 0, 0, '', 0)
    rowofsix_6      = card("rowofsix_6", "", 0, 0, 0, '', 0)
    bottom_1        = card("bottom_1", "", 0, 0, 0, '', 0)
    bottom_2        = card("bottom_2", "", 0, 0, 0, '', 0)
    bottom_3        = card("bottom_3", "", 0, 0, 0, '', 0)
    bottom_4        = card("bottom_4", "", 0, 0, 0, '', 0)
    bottom_5        = card("bottom_5", "", 0, 0, 0, '', 0)
    bottom_6        = card("bottom_6", "", 0, 0, 0, '', 0)
    bottom_7        = card("bottom_7", "", 0, 0, 0, '', 0)

    # Draw pile
    dp1  = card("dp1", "", 0, 0, 0, '', 0)
    dp2  = card("dp2", "", 0, 0, 0, '', 0)
    dp3  = card("dp3", "", 0, 0, 0, '', 0)
    dp4  = card("dp4", "", 0, 0, 0, '', 0)
    dp5  = card("dp5", "", 0, 0, 0, '', 0)
    dp6  = card("dp6", "", 0, 0, 0, '', 0)
    dp7  = card("dp7", "", 0, 0, 0, '', 0)
    dp8  = card("dp8", "", 0, 0, 0, '', 0)
    dp9  = card("dp9", "", 0, 0, 0, '', 0)
    dp10 = card("dp10", "", 0, 0, 0, '', 0)
    dp11 = card("dp11", "", 0, 0, 0, '', 0)
    dp12 = card("dp12", "", 0, 0, 0, '', 0)
    dp13 = card("dp12", "", 0, 0, 0, '', 0)
    dp14 = card("dp14", "", 0, 0, 0, '', 0)
    dp15 = card("dp15", "", 0, 0, 0, '', 0)
    dp16 = card("dp16", "", 0, 0, 0, '', 0)
    dp17 = card("dp17", "", 0, 0, 0, '', 0)
    dp18 = card("dp18", "", 0, 0, 0, '', 0)
    dp19 = card("dp19", "", 0, 0, 0, '', 0)
    dp20 = card("dp20", "", 0, 0, 0, '', 0)
    dp21 = card("dp21", "", 0, 0, 0, '', 0)
    dp22 = card("dp22", "", 0, 0, 0, '', 0)
    dp23 = card("dp23", "", 0, 0, 0, '', 0)
    dp24 = card("dp24", "", 0, 0, 0, '', 0)


# ---------------------------------------

def play_sound(sound_effect):
    current_length = sound_effect.get_length()
    print "Sound effect length:", current_length
    if pygame.mixer.get_busy():
        pass
    else:
        sound_effect.play()

# ---------------------------------------


def score_boards_deals():
    score_start = 660
    score_label = bold_font.render("score "+str(score), True, black)
    boards_label = bold_font.render("boards "+str(boards), True, black)
    deals_label = bold_font.render("deals "+str(deals), True, black)

    # distance between score and boards: 115
    # distance between boards and deals: 125
    dbsb = 115
    dbbd = 125

    mainSurface.blit(score_label, (score_start, mainSurface_height - 30))
    board_start = score_start + dbsb
    mainSurface.blit(boards_label, (board_start, mainSurface_height - 30))
    deal_start = board_start + dbbd
    mainSurface.blit(deals_label, (deal_start, mainSurface_height - 30))

# ---------------------------------------

def get_card_text(sr):
    """Take in one card suit and rank for example 'AH'.
    Return the text and center flag corresponding to that card.
    """
    global suit_rank_card_text
    global center_flags
    card_text = suit_rank_card_text[sr]
    center_flag = center_flags[sr]
    return card_text, center_flag

# ---------------------------------------

def match_to_suit_and_rank():
    """Using deck of cards, assign text key value pairs to every
    suit/rank. For example 'AH', 'AC', etc.
    Used in conjunction with get_card_text()?
    """
    match_deck = get_match_dictionary()
    suit_rank_card_text = {}

    # All keys = 1, values = 0
    center_flags = {}

    for sr in deckofcards:
        if sr.startswith('A'):
            card_text = match_deck.keys()[0]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 1
        if sr.startswith('2'):
            card_text = match_deck.keys()[1]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 1
        if sr.startswith('3'):
            card_text = match_deck.keys()[2]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 1
        if sr.startswith('4'):
            card_text = match_deck.keys()[3]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 1
        if sr.startswith('5'):
            card_text = match_deck.keys()[4]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 1
        if sr.startswith('6'):
            card_text = match_deck.keys()[5]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 1
        if sr.startswith('Q'):
            card_text = match_deck.values()[0]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 0
        if sr.startswith('J'):
            card_text = match_deck.values()[1]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 0
        if sr.startswith('10'):
            card_text = match_deck.values()[2]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 0
        if sr.startswith('9'):
            card_text = match_deck.values()[3]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 0
        if sr.startswith('8'):
            card_text = match_deck.values()[4]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 0
        if sr.startswith('7'):
            card_text = match_deck.values()[5]
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 0

        # Look up King value
        if sr.startswith('K'):
            card_text = "King of Kings"
            suit_rank_card_text[sr] = card_text
            center_flags[sr] = 1

    return suit_rank_card_text, center_flags

# ---------------------------------------

def get_match_dictionary():

    # Define six keys that correspond to six values
    keys = ["Philippians 4:6-7", "Philippians 4:8", "Philippians 4:4-5", "Philippians 4:13", "Philippians 4:19", "Philippians 4:12" ]
    values = ["Do not be anxious about anything, but in everything, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.",
              "Finally, brothers and sisters, whatever is true, whatever is noble, whatever is right, whatever is pure, whatever is lovely, whatever is admirable-if anything is excellent or praiseworthy-think about such things.",
              "Rejoice in the Lord always. I will say it again: Rejoice! Let your gentleness be evident to all. The Lord is near.",
              "I can do all things through him who gives me strength.",
              "And my God will meet all your needs according to his glorious riches in Christ Jesus.",
              "I know what it is to be in need, and I know what it is to have plenty. I have learned the secret of being content in any and every situation, whether well fed or hungry, whether living in plenty or in want."
              ]
    match_deck = dict(zip(keys, values))

##    for k, v in match_deck.iteritems():
##        print k, "\t", v
    return match_deck

# ---------------------------------------
def get_pyramid_locations():

    global pyramid_height
    global pyramid_left
    global pyramid_right

    top = 600
    left = 100
    pyramid_left = left
    spacer = 204           #  surface_width + 20
    row_vertical_spacer = 85
    row_horizontal_spacer = 102

    row6_top = top - row_vertical_spacer
    row6_left = left + row_horizontal_spacer

    row5_top = row6_top - row_vertical_spacer
    row5_left = row6_left + row_horizontal_spacer

    row4_top = row5_top - row_vertical_spacer
    row4_left = row5_left + row_horizontal_spacer

    row3_top = row4_top - row_vertical_spacer
    row3_left = row4_left + row_horizontal_spacer

    row2_top = row3_top - row_vertical_spacer
    row2_left = row3_left + row_horizontal_spacer

    toprow_top = row2_top - row_vertical_spacer
    toprow_left = row2_left + row_horizontal_spacer
    pyramid_height = toprow_top

    pyramid_location = {}

    pyramid_location["toprow"] = (toprow_left, toprow_top)

    pyramid_location["rowoftwo_1"] = (row2_left, row2_top)
    row2_left = row2_left + spacer
    pyramid_location["rowoftwo_2"] = (row2_left, row2_top)

    pyramid_location["rowofthree_1"] = (row3_left, row3_top)
    row3_left = row3_left + spacer
    pyramid_location["rowofthree_2"] = (row3_left, row3_top)
    row3_left = row3_left + spacer
    pyramid_location["rowofthree_3"] = (row3_left, row3_top)

    pyramid_location["rowoffour_1"] = (row4_left, row4_top)
    row4_left = row4_left + spacer
    pyramid_location["rowoffour_2"] = (row4_left, row4_top)
    row4_left = row4_left + spacer
    pyramid_location["rowoffour_3"] = (row4_left, row4_top)
    row4_left = row4_left + spacer
    pyramid_location["rowoffour_4"] = (row4_left, row4_top)

    pyramid_location["rowoffive_1"] = (row5_left, row5_top)
    row5_left = row5_left + spacer
    pyramid_location["rowoffive_2"] = (row5_left, row5_top)
    row5_left = row5_left + spacer
    pyramid_location["rowoffive_3"] = (row5_left, row5_top)
    row5_left = row5_left + spacer
    pyramid_location["rowoffive_4"] = (row5_left, row5_top)
    row5_left = row5_left + spacer
    pyramid_location["rowoffive_5"] = (row5_left, row5_top)

    pyramid_location["rowofsix_1"] = (row6_left, row6_top)
    row6_left = row6_left + spacer
    pyramid_location["rowofsix_2"] = (row6_left, row6_top)
    row6_left = row6_left + spacer
    pyramid_location["rowofsix_3"] = (row6_left, row6_top)
    row6_left = row6_left + spacer
    pyramid_location["rowofsix_4"] = (row6_left, row6_top)
    row6_left = row6_left + spacer
    pyramid_location["rowofsix_5"] = (row6_left, row6_top)
    row6_left = row6_left + spacer
    pyramid_location["rowofsix_6"] = (row6_left, row6_top)

    pyramid_location["bottom_1"] = (left, top)
    left = left + spacer
    pyramid_location["bottom_2"] = (left, top)
    left = left + spacer
    pyramid_location["bottom_3"] = (left, top)
    left = left + spacer
    pyramid_location["bottom_4"] = (left, top)
    left = left + spacer
    pyramid_location["bottom_5"] = (left, top)
    left = left + spacer
    pyramid_location["bottom_6"] = (left, top)
    left = left + spacer
    pyramid_location["bottom_7"] = (left, top)
    pyramid_right = left

    return pyramid_location


# ---------------------------------------

def text_card_setup():
    pygame.init()
    pygame.display.set_caption('Box Test')
    mainSurface = pygame.display.set_mode((1600,950), 0, 32)
    mainSurface.fill((gray))
##    bg = pygame.image.load(r'C:\Users\Chris\Desktop\Python Scripts\my scripts\Games\Pyramid\green_felt.jpg').convert()
##    mainSurface.blit() #Display image at 0, 0
##    pygame.display.update()

    # ----------------------------

    top = 600
    left = 100
    spacer = 204           #  Pane.surface_width + 20
    row_vertical_spacer = 85
    row_horizontal_spacer = 102


    row6_top = top - row_vertical_spacer
    row6_left = left + row_horizontal_spacer

    row5_top = row6_top - row_vertical_spacer
    row5_left = row6_left + row_horizontal_spacer

    row4_top = row5_top - row_vertical_spacer
    row4_left = row5_left + row_horizontal_spacer

    row3_top = row4_top - row_vertical_spacer
    row3_left = row4_left + row_horizontal_spacer

    row2_top = row3_top - row_vertical_spacer
    row2_left = row3_left + row_horizontal_spacer

    toprow_top = row2_top - row_vertical_spacer
    toprow_left = row2_left + row_horizontal_spacer


    toprow = Pane()
    toprow.addRect(toprow_top, toprow_left)      # top, left
    toprow.addText("Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.", 0)


    rowoftwo_1 = Pane()
    rowoftwo_1.addRect(row2_top, row2_left)      # top, left
    rowoftwo_1.addText("Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.", 0)

    row2_left = row2_left + spacer
    rowoftwo_2 = Pane()
    rowoftwo_2.addRect(row2_top, row2_left)      # top, left
    rowoftwo_2.addText("Philippians 4:6-7", 1)


    rowofthree_1 = Pane()
    rowofthree_1.addRect(row3_top, row3_left)      # top, left
    rowofthree_1.addText("And my God will meet all your needs according to the riches of his glory in Christ Jesus.", 0)

    row3_left = row3_left + spacer
    rowofthree_2 = Pane()
    rowofthree_2.addRect(row3_top, row3_left)      # top, left
    rowofthree_2.addText("Philippians 4:6-7", 1)

    row3_left = row3_left + spacer
    rowofthree_3 = Pane()
    rowofthree_3.addRect(row3_top, row3_left)      # top, left
    rowofthree_3.addText("I can do all things through him who gives me strength.", 0)



    rowoffour_1 = Pane()
    rowoffour_1.addRect(row4_top, row4_left)      # top, left
    rowoffour_1.addText("Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.", 0)

    row4_left = row4_left + spacer
    rowoffour_2 = Pane()
    rowoffour_2.addRect(row4_top, row4_left)      # top, left
    rowoffour_2.addText("Philippians 4:6-7", 1)

    row4_left = row4_left + spacer
    rowoffour_3 = Pane()
    rowoffour_3.addRect(row4_top, row4_left)      # top, left
    rowoffour_3.addText("I can do all things through him who gives me strength.", 0)

    row4_left = row4_left + spacer
    rowoffour_4 = Pane()
    rowoffour_4.addRect(row4_top, row4_left)      # top, left
    rowoffour_4.addText("Philippians 4:13", 1)




    rowoffive_1 = Pane()
    rowoffive_1.addRect(row5_top, row5_left)      # top, left
    rowoffive_1.addText("Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.", 0)

    row5_left = row5_left + spacer
    rowoffive_2 = Pane()
    rowoffive_2.addRect(row5_top, row5_left)      # top, left
    rowoffive_2.addText("Philippians 4:6-7", 1)

    row5_left = row5_left + spacer
    rowoffive_3 = Pane()
    rowoffive_3.addRect(row5_top, row5_left)      # top, left
    rowoffive_3.addText("I can do all things through him who gives me strength.", 0)

    row5_left = row5_left + spacer
    rowoffive_4 = Pane()
    rowoffive_4.addRect(row5_top, row5_left)      # top, left
    rowoffive_4.addText("Philippians 4:13", 1)

    row5_left = row5_left + spacer
    rowoffive_5 = Pane()
    rowoffive_5.addRect(row5_top, row5_left)      # top, left
    rowoffive_5.addText("I can do all things through him who gives me strength.", 0)



    rowofsix_1 = Pane()
    rowofsix_1.addRect(row6_top, row6_left)      # top, left
    rowofsix_1.addText("Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.", 0)

    row6_left = row6_left + spacer
    rowofsix_2 = Pane()
    rowofsix_2.addRect(row6_top, row6_left)      # top, left
    rowofsix_2.addText("Philippians 4:6-7", 1)

    row6_left = row6_left + spacer
    rowofsix_3 = Pane()
    rowofsix_3.addRect(row6_top, row6_left)      # top, left
    rowofsix_3.addText("I can do all things through him who gives me strength.", 0)

    row6_left = row6_left + spacer
    rowofsix_4 = Pane()
    rowofsix_4.addRect(row6_top, row6_left)      # top, left
    rowofsix_4.addText("Philippians 4:13", 1)

    row6_left = row6_left + spacer
    rowofsix_5 = Pane()
    rowofsix_5.addRect(row6_top, row6_left)      # top, left
    rowofsix_5.addText("I can do all things through him who gives me strength.", 0)

    row6_left = row6_left + spacer
    rowofsix_6 = Pane()
    rowofsix_6.addRect(row6_top, row6_left)      # top, left
    rowofsix_6.addText("Philippians 4:13", 1)




    bottom_1 = Pane()
    bottom_1.addRect(top, left)      # top, left
    bottom_1.addText("Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.", 0)

    left = left + spacer
    bottom_2 = Pane()
    bottom_2.addRect(top, left)      # top, left
    bottom_2.addText("Philippians 4:6-7", 1)

    left = left + spacer
    bottom_3 = Pane()
    bottom_3.addRect(top, left)      # top, left
    bottom_3.addText("I can do all things through him who gives me strength.", 0)

    left = left + spacer
    bottom_4 = Pane()
    bottom_4.addRect(top, left)      # top, left
    bottom_4.addText("Philippians 4:19", 1)

    left = left + spacer
    bottom_5 = Pane()
    bottom_5.addRect(top, left)      # top, left
    bottom_5.addText("I can do all things through him who gives me strength.", 0)

    left = left + spacer
    bottom_6 = Pane()
    bottom_6.addRect(top, left)      # top, left
    bottom_6.addText("Philippians 4:13", 1)

    left = left + spacer
    bottom_7 = Pane()
    bottom_7.addRect(top, left)      # top, left
    bottom_7.addText("Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God. And the peace of God, which transcends all understanding, will guard your hearts and your minds in Christ Jesus.", 0)

    pygame.display.update()

##    while True:
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                pygame.quit();
##                sys.exit();


# ---------------------------------------

def getShuffledDeck():
##    deckofcards = [ "AH", "KH", "QH", "JH", "10H", "9H", "8H", "7H", "6H", "5H", "4H", "3H", "2H",
##                    "AS", "KS", "QS", "JS", "10S", "9S", "8S", "7S", "6S", "5S", "4S", "3S", "2S",
##                    "AD", "KD", "QD", "JD", "10D", "9D", "8D", "7D", "6D", "5D", "4D", "3D", "2D",
##                    "AC", "KC", "QC", "JC", "10C", "9C", "8C", "7C", "6C", "5C", "4C", "3C", "2C" ]

    shuffle(deckofcards)
    pyramid_cards = deckofcards[0:28]
    draw_pile = deckofcards[28:52]
    return pyramid_cards, draw_pile

# ---------------------------------------

def checkCardLock(cardloc):
    # Checks to see if the card is locked behind other cards.
    # Returns "locked" if locked or "unlocked" if unlocked
    # cardloc is a card object

    # Draw pile
    if current_deck.get_layer_of_sprite(cardloc) == 0:
        return "unlocked"

    # Layer 7
    if current_deck.get_layer_of_sprite(cardloc) == 7:
        return "unlocked"

    # Layer 6
    elif current_deck.get_layer_of_sprite(cardloc) == 6:
        print "\tcheckCardLock:", cardloc.pyramidloc, cardloc.suitandrank, cardloc.intval, "Layer:", current_deck.get_layer_of_sprite(cardloc)

        bottom_row_list = returnLayer(7)
        print "\tcheckCardLock: bottom_row_list:", bottom_row_list

        if cardloc.pyramidloc == "rowofsix_1" and 'bottom_1' not in bottom_row_list and 'bottom_2' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowofsix_2" and 'bottom_2' not in bottom_row_list and 'bottom_3' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowofsix_3" and 'bottom_3' not in bottom_row_list and 'bottom_4' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowofsix_4" and 'bottom_4' not in bottom_row_list and 'bottom_5' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowofsix_5" and 'bottom_5' not in bottom_row_list and 'bottom_6' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowofsix_6" and 'bottom_6' not in bottom_row_list and 'bottom_7' not in bottom_row_list:
            return "unlocked"
        else:
            return "locked"

    # Layer 5
    elif current_deck.get_layer_of_sprite(cardloc) == 5:
        print "\tcheckCardLock:", cardloc.pyramidloc, cardloc.suitandrank, cardloc.intval, "Layer:", current_deck.get_layer_of_sprite(cardloc)

        bottom_row_list = returnLayer(6)
        print "\tcheckCardLock: rowofsix_row_list:", bottom_row_list

        if cardloc.pyramidloc == "rowoffive_1" and 'rowofsix_1' not in bottom_row_list and 'rowofsix_2' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowoffive_2" and 'rowofsix_2' not in bottom_row_list and 'rowofsix_3' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowoffive_3" and 'rowofsix_3' not in bottom_row_list and 'rowofsix_4' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowoffive_4" and 'rowofsix_4' not in bottom_row_list and 'rowofsix_5' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowoffive_5" and 'rowofsix_5' not in bottom_row_list and 'rowofsix_6' not in bottom_row_list:
            return "unlocked"
        else:
            return "locked"

    # Layer 4
    elif current_deck.get_layer_of_sprite(cardloc) == 4:
        print "\tcheckCardLock:", cardloc.pyramidloc, cardloc.suitandrank, cardloc.intval, "Layer:", current_deck.get_layer_of_sprite(cardloc)

        bottom_row_list = returnLayer(5)
        print "\tcheckCardLock: rowoffive_row_list:", bottom_row_list

        if cardloc.pyramidloc == "rowoffour_1" and 'rowoffive_1' not in bottom_row_list and 'rowoffive_2' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowoffour_2" and 'rowoffive_2' not in bottom_row_list and 'rowoffive_3' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowoffour_3" and 'rowoffive_3' not in bottom_row_list and 'rowoffive_4' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowoffour_4" and 'rowoffive_4' not in bottom_row_list and 'rowoffive_5' not in bottom_row_list:
            return "unlocked"
        else:
            return "locked"

    # Layer 3
    elif current_deck.get_layer_of_sprite(cardloc) == 3:
        print "\tcheckCardLock:", cardloc.pyramidloc, cardloc.suitandrank, cardloc.intval, "Layer:", current_deck.get_layer_of_sprite(cardloc)

        bottom_row_list = returnLayer(4)
        print "\tcheckCardLock: rowoffour_row_list:", bottom_row_list

        if cardloc.pyramidloc == "rowofthree_1" and 'rowoffour_1' not in bottom_row_list and 'rowoffour_2' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowofthree_2" and 'rowoffour_2' not in bottom_row_list and 'rowoffour_3' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowofthree_3" and 'rowoffour_3' not in bottom_row_list and 'rowoffour_4' not in bottom_row_list:
            return "unlocked"
        else:
            return "locked"


    # Layer 2
    elif current_deck.get_layer_of_sprite(cardloc) == 2:
        print "\tcheckCardLock:", cardloc.pyramidloc, cardloc.suitandrank, cardloc.intval, "Layer:", current_deck.get_layer_of_sprite(cardloc)

        bottom_row_list = returnLayer(3)
        print "\tcheckCardLock: rowofthree_row_list:", bottom_row_list

        if cardloc.pyramidloc == "rowoftwo_1" and 'rowofthree_1' not in bottom_row_list and 'rowofthree_2' not in bottom_row_list:
            return "unlocked"
        elif cardloc.pyramidloc == "rowoftwo_2" and 'rowofthree_2' not in bottom_row_list and 'rowofthree_3' not in bottom_row_list:
            return "unlocked"
        else:
            return "locked"

    # Top row
    elif current_deck.get_layer_of_sprite(cardloc) == 1:
        print "\tcheckCardLock:", cardloc.pyramidloc, cardloc.suitandrank, cardloc.intval, "Layer:", current_deck.get_layer_of_sprite(cardloc)

        bottom_row_list = returnLayer(2)
        print "\tcheckCardLock: rowoftwo_row_list:", bottom_row_list
        if cardloc.pyramidloc == "toprow" and 'rowoftwo_1' not in bottom_row_list and 'rowoftwo_2' not in bottom_row_list:
            return "unlocked"
        else:
            return "locked"

    else:
        return "locked"

# ---------------------------------------

def returnLayerSR(layer):
    # For the given layer (int), return a list of suitandranks
    # i.e. ['AS', '9D', '3C']
    sprite_layer_list = current_deck.get_sprites_from_layer(layer)
    row_list = []
    for s in sprite_layer_list:
        row_list.append(s.suitandrank)
    return row_list

# ---------------------------------------

def returnLayer(layer):
    # For the given layer (int), return a list of pyramid locations.
    # i.e. ['rowofthree_1', 'rowofthree_2', 'rowofthree_3']
    sprite_layer_list = current_deck.get_sprites_from_layer(layer)
    row_list = []
    for s in sprite_layer_list:
        row_list.append(s.pyramidloc)
    return row_list

# ---------------------------------------

def returnCardValue(suitandrank):
    # Pass in a suitandrank from the shuffled_deck that looks like "9H"
    # Read the first letter of the string and return the int value
    if suitandrank[0] == "A":
        return 1
    if suitandrank[0] == "K":
        return 13
    if suitandrank[0] == "Q":
        return 12
    if suitandrank[0] == "J":
        return 11
    if suitandrank[0] == "1":
        return 10
    if suitandrank[0] == "9":
        return 9
    if suitandrank[0] == "8":
        return 8
    if suitandrank[0] == "7":
        return 7
    if suitandrank[0] == "6":
        return 6
    if suitandrank[0] == "5":
        return 5
    if suitandrank[0] == "4":
        return 4
    if suitandrank[0] == "3":
        return 3
    if suitandrank[0] == "2":
        return 2

# ---------------------------------------

def drawPyramid(pyramid_cards):

    pyramid_locations = get_pyramid_locations()
##    card_text, center_flag = get_card_text(sr)


    pyramid_order =["toprow", "rowoftwo_1", "rowoftwo_2", "rowofthree_1", "rowofthree_2", "rowofthree_3",
                    "rowoffour_1", "rowoffour_2", "rowoffour_3", "rowoffour_4", "rowoffive_1", "rowoffive_2",
                    "rowoffive_3", "rowoffive_4", "rowoffive_5", "rowofsix_1", "rowofsix_2", "rowofsix_3",
                    "rowofsix_4", "rowofsix_5", "rowofsix_6", "bottom_1", "bottom_2", "bottom_3", "bottom_4",
                    "bottom_5", "bottom_6", "bottom_7"]

    pyramid_vars = [toprow, rowoftwo_1, rowoftwo_2, rowofthree_1, rowofthree_2, rowofthree_3, rowoffour_1,
                    rowoffour_2, rowoffour_3, rowoffour_4, rowoffive_1, rowoffive_2, rowoffive_3, rowoffive_4,
                    rowoffive_5, rowofsix_1, rowofsix_2, rowofsix_3, rowofsix_4, rowofsix_5, rowofsix_6, bottom_1,
                    bottom_2, bottom_3, bottom_4, bottom_5, bottom_6, bottom_7]


    i = 0
    while i < len(pyramid_order):
        # rowofsix_6 = card("rowofsix_6", "Jack of Spades", 11, 355,255)
        pyramid_vars[i] = card(pyramid_order[i],
                               pyramid_cards[i],
                               returnCardValue(pyramid_cards[i]),
                               pyramid_locations[pyramid_order[i]][0],
                               pyramid_locations[pyramid_order[i]][1],
                               get_card_text(pyramid_cards[i])[0],
                               get_card_text(pyramid_cards[i])[1])

        current_deck.add(pyramid_vars[i])
        i += 1

# ---------------------------------------

def drawPile(draw_pile):

    global draw_button_rect

    drawpile = pygame.draw.rect(mainSurface, GRAY, (pyramid_right, pyramid_height,50,90), 0)
    discardpileGraphic = pygame.image.load(r'C:\Python27\images\discard.png').convert_alpha()
    discardpileGraphic = pygame.transform.scale(discardpileGraphic, (180, 295))

    mainSurface.blit(discardpileGraphic, (pyramid_right, pyramid_height))
    draw_button_rect = pygame.Rect(330,220,50,50)

    draw_pile_stack = ['dp1', 'dp2', 'dp3', 'dp4', 'dp5', 'dp6', 'dp7', 'dp8', 'dp9', 'dp10', 'dp11', 'dp12', 'dp13', 'dp14', 'dp15', 'dp16', 'dp17', 'dp18', 'dp19', 'dp20', 'dp21', 'dp22', 'dp23', 'dp24']
    draw_pile_vars = [dp1, dp2, dp3, dp4, dp5, dp6, dp7, dp8, dp9, dp10, dp11, dp12, dp13, dp14, dp15, dp16, dp17, dp18, dp19, dp20, dp21, dp22, dp23, dp24]

    i = 0
    while i < len(draw_pile):
        # rowofsix_6 = card("rowofsix_6", "Jack of Spades", 11, 355,255)
        draw_pile_vars[i] = card(draw_pile_stack[i],
                                 draw_pile[i],
                                 returnCardValue(draw_pile[i]),
                                 pyramid_left,
                                 pyramid_height,
                                 get_card_text(draw_pile[i])[0],
                                 get_card_text(draw_pile[i])[1])
        current_deck.add(draw_pile_vars[i])
        i += 1

# ---------------------------------------

def boardSetup():

    global layer_cleared
    global draw_pile_rect_loc
    draw_pile_rect_loc = pygame.Rect(0,0,0,0)
    layer_cleared = [1, 2, 3, 4, 5, 6, 7]

    # Draw everything here. This is where all cards need to be assigned deck_values
    instantiateAllDefaultcards()

    shuffled_deck = getShuffledDeck()
    pyramid_cards = shuffled_deck[0]
    draw_pile = shuffled_deck[1]
    print "pyramid_cards contains:\n", pyramid_cards
    print "Draw pile contains:\n", draw_pile
    drawPyramid(pyramid_cards)
    drawPile(draw_pile)

    current_deck.draw(mainSurface)
    current_deck.update()

    draw_button = pygame.image.load(r'C:\Python27\images\button.png').convert_alpha()
##    draw_button_rect = pygame.Rect(300,pyramid_height-92,50,50)
    mainSurface.blit(draw_button, (330,220))

    score_boards_deals()

    pygame.display.update()

# ---------------------------------------

def evaluateDeck():

    print "evaluateDeck()"
    open_card_list = []

    # All cards in bottom_layer are OPEN
    # Add the COMPLEMENT for each open card to open_card_list
    bl = layer_cleared[-1]
    bottom_layer = current_deck.get_sprites_from_layer(bl)
    for c in bottom_layer:
        open_card_list.append(13 - c.intval)
    print "The bottom row in layer_cleared is:", bl, returnLayerSR(bl)

    # bl is also the number of cards that the layer starts with
    # The layer above this is bl-1
    # one_layer_above only needs to be checked if there are 2 cards missing from bottom_layer
    if bl - len(bottom_layer) >= 2:
        # At least two cards are missing from the bottom layer, so check the next layer up
        one_layer_above = current_deck.get_sprites_from_layer(bl-1)
        print "one_layer_above contains:", bl-1, returnLayerSR(bl-1)
        for c in one_layer_above:
            unlocked = checkCardLock(c)
            if unlocked == "unlocked":
                open_card_list.append(13 - c.intval)
        if bl-1 - len(one_layer_above) >= 2:
            two_layer_above = current_deck.get_sprites_from_layer(bl-2)
            print "two_layer_above contains:", bl-2, returnLayerSR(bl-2)
            for c in two_layer_above:
                unlocked = checkCardLock(c)
                if unlocked == "unlocked":
                    open_card_list.append(13 - c.intval)
            if bl-2 - len(two_layer_above) >= 2:
                three_layer_above = current_deck.get_sprites_from_layer(bl-3)
                print "three_layer_above contains:", bl-3, returnLayerSR(bl-3)
                for c in three_layer_above:
                    unlocked = checkCardLock(c)
                    if unlocked == "unlocked":
                        open_card_list.append(13 - c.intval)
                if bl-3 - len(two_layer_above) >= 2:
                    four_layer_above = current_deck.get_sprites_from_layer(bl-4)
                    print "four_layer_above contains:", bl-4, returnLayerSR(bl-4)
                    for c in four_layer_above:
                        unlocked = checkCardLock(c)
                        if unlocked == "unlocked":
                            open_card_list.append(13 - c.intval)

    print "open_card_list contains:", open_card_list
    dp = []
    draw_pile_layer = discard_pile.get_sprites_from_layer(0)
    for c in draw_pile_layer:
        dp.append(c.intval)

    pyramid_set = set(open_card_list)
    drawpile_set = set(dp)

    overlap = pyramid_set & drawpile_set
    print "Overlap:", overlap
    if not overlap:
        print "There are no more moves."
        return 1
    else:
        return 0


# ---------------------------------------

def main():


    global draw_pile_rect_loc
    global draw_button_rect
    global deals_button_Rect
    global layer_cleared
    global score, boards, deals
    deals_button_Rect = pygame.Rect(0,0,0,0)


    global suit_rank_card_text
    global center_flags
    suit_rank_card_text, center_flags = match_to_suit_and_rank()

    for k, v in sorted(suit_rank_card_text.iteritems()):
        print k, "\t", center_flags[k], "\t", v

    score_boards_deals()
    boardSetup()
##    text_card_setup()

    two_cards = []

    # Gameplay while loop
    while True:

        # Event loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:


                # Get the mouse click position
                mouse_pos = pygame.mouse.get_pos()

                spritelist = current_deck.get_sprites_at(mouse_pos), len(current_deck.get_sprites_at(mouse_pos))
                discard_pile_sprites = discard_pile.get_sprites_at(mouse_pos), len(discard_pile.get_sprites_at(mouse_pos))

                listofdiscardsprites = discard_pile_sprites[0]
                if listofdiscardsprites:
                    print "---------------------------------------"
                    print "Mouseclick touches these discard cards:"
                    for s in listofdiscardsprites:
                        print s.pyramidloc, s.suitandrank, s.intval, "Layer:", discard_pile.get_layer_of_sprite(s)


                listofsprites = spritelist[0]
                if listofsprites:
                    print "---------------------------------------"
                    print "Mouseclick touches these cards:"
                    for s in listofsprites:
                        print s.pyramidloc, s.suitandrank, s.intval, "Layer:", current_deck.get_layer_of_sprite(s)

                if listofsprites:
                    bottom_card_clicked = listofsprites[-1:][0]
                elif listofdiscardsprites:
                    bottom_card_clicked = listofdiscardsprites[-1:][0]
                else:
                    bottom_card_clicked = None

                if bottom_card_clicked:
                    bottom_card_clicked_layer = current_deck.get_layer_of_sprite(bottom_card_clicked)
                    print "\nThe actual card clicked is:\n", bottom_card_clicked.pyramidloc, bottom_card_clicked.suitandrank, bottom_card_clicked.intval, "Layer:", bottom_card_clicked_layer

                    # Logic that keeps track of the two cards that have been clicked
                    if len(two_cards) < 2:
                        thirteen = 0
                        two_cards.append(bottom_card_clicked)
                        print "--Two_cards:", two_cards
                        for t in two_cards:
                            print t.suitandrank, t.intval, current_deck.get_layer_of_sprite(t)
                            thirteen += t.intval
                            if t.suitandrank[0] == "K":
                                print "This is a KING!"
                                two_cards = [t]       # overwrite the contents of two_cards with just the king
                                thirteen = t.intval
                            print "Thirteen?", thirteen
                    else:
                        thirteen = 0
                        two_cards = []
                        two_cards.append(bottom_card_clicked)
                        print "--Two_cards cleared:", two_cards
                        for t in two_cards:
                            print t.suitandrank, t.intval, current_deck.get_layer_of_sprite(t)
                            thirteen += t.intval
                            if t.suitandrank[0] == "K":
                                print "This is a KING!"
                                two_cards = [t]       # overwrite the contents of two_cards with just the king
                                thirteen = t.intval
                            print "Thirteen?", thirteen


                    lock_status = checkCardLock(bottom_card_clicked)
                    print "Locked or unlocked:", lock_status

                    # Logic that removes cards. Cards have to be unlocked and add up to 13.
                    if lock_status == "unlocked" and thirteen == 13:
                        play_sound(match_sound)

                        for t in two_cards:
                            discard_pile.remove(t)
                            # Check right here to see if the pyramid layer in current_deck is now empty (for the points bonus)
                            t_layer = current_deck.get_layer_of_sprite(t)
                            current_deck.remove(t)
                            if t_layer > 0:     # layer 0 is the draw pile layer
                                removefromrow = returnLayer(t_layer)
                                print "removefromrow", removefromrow
                                if t_layer in layer_cleared and len(removefromrow) == 0:
                                    layer_cleared.pop()
                                    pygame.time.wait(500)
                                    play_sound(cleared_row_sound)
                                    print "layer_cleared now contains:", layer_cleared
                                    # Add point bonuses for clearing a row
                                    if t_layer == 7:
                                        score += 25
                                    if t_layer == 6:
                                        score += 50
                                    if t_layer == 5:
                                        score += 75
                                    if t_layer == 4:
                                        score += 100
                                    if t_layer == 3:
                                        score += 150
                                    if t_layer == 2:
                                        score += 250
                                    if t_layer == 1:
                                        score += 500
                                        boards += 1
                                        # This is also the point at which the board is cleared.
                                        # So we need to rebuild the pyramid and draw_pile
                                        current_deck.empty()
                                        discard_pile.empty()
                                        current_deck.clear(mainSurface, bg)
                                        discard_pile.clear(mainSurface, bg)
                                        boardSetup()
                                        play_sound(cleared_board_sound)

                        two_cards = []

                        # Add 5 points for making a match
                        score += 5
                        print "The score is:", score

                        # Clear the old text by redrawing the background image on the mainSurface
                        mainSurface.blit(bg, (0, 0)) #Display image at 0, 0

                        # Then Update the score
                        score_boards_deals()


                        # and redraw everything on the screen
                        draw_button = pygame.image.load(r'C:\Python27\images\button.png').convert_alpha()
                        mainSurface.blit(draw_button, (330,220))

                        current_deck.clear(mainSurface, bg)
                        current_deck.draw(mainSurface)
                        discard_pile.clear(mainSurface, bg)
                        discardpileGraphic = pygame.image.load(r'C:\Python27\images\discard.png').convert_alpha()
                        discardpileGraphic = pygame.transform.scale(discardpileGraphic, (180, 295))
                        mainSurface.blit(discardpileGraphic, (pyramid_right, pyramid_height))
                        discard_pile.draw(mainSurface)
                        pygame.display.flip()


                        # Check to see if the drawpile is empty yet, because of the last card match
                        cardsindrawpile = returnLayer(0)
                        print "Draw pile contains:", cardsindrawpile
                        if not cardsindrawpile:
                            draw_pile_loc = pygame.image.load(r'C:\Python27\images\drawpile.png').convert_alpha()
                            draw_pile_loc = pygame.transform.scale(draw_pile_loc, (180, 295))
                            mainSurface.blit(draw_pile_loc, (pyramid_left, pyramid_height))
                            draw_pile_rect_loc = pygame.Rect(pyramid_left, pyramid_height, 180, 295)

                        pygame.display.update()
                    else:
                        play_sound(card_select_sound)
                        print "Current row list:", returnLayer(bottom_card_clicked_layer)

                # Logic to move cards from the draw_pile to the discard pile
                if draw_button_rect.collidepoint((mouse_pos)):
                    play_sound(draw_sound)
                    print "Clicked the discard button!!"
                    two_cards = []      # Clear two_cards since card was discarded
                    draw_pile_layer = current_deck.get_sprites_from_layer(0)
                    if draw_pile_layer:
                        top_of_draw_pile = draw_pile_layer[-1]
                        print "top_of_draw_pile", top_of_draw_pile, type(top_of_draw_pile)
                        print "top_of_draw_pile", top_of_draw_pile.pyramidloc, top_of_draw_pile.suitandrank, top_of_draw_pile.intval

                        current_deck.remove(top_of_draw_pile)

                        top_of_draw_pile.rect.x = pyramid_right
                        top_of_draw_pile.rect.y = pyramid_height
                        discard_pile.add(top_of_draw_pile)

                        current_deck.clear(mainSurface, bg)
                        current_deck.draw(mainSurface)
                        discard_pile.clear(mainSurface, bg)
                        discard_pile.draw(mainSurface)

                        # Check to see if the drawpile is empty yet, because of using the discard button
                        cardsindrawpile = returnLayer(0)
                        print "Draw pile contains:", cardsindrawpile
                        if not cardsindrawpile:
                            draw_pile_loc = pygame.image.load(r'C:\Python27\images\drawpile.png').convert_alpha()
                            draw_pile_loc = pygame.transform.scale(draw_pile_loc, (180, 295))
                            mainSurface.blit(draw_pile_loc, (pyramid_left, pyramid_height))
                            draw_pile_rect_loc = pygame.Rect(pyramid_left, pyramid_height, 180, 295)

                        pygame.display.update()

                # Logic to handle the repopulating of the draw pile from the discard pile
                if draw_pile_rect_loc.collidepoint((mouse_pos)):
                    play_sound(repopulate_draw_pile_sound)
                    print "Time to move the cards back over..."
                    # The drawpile.png graphic only lasts on screen until it is clicked to repopulate from the discard pile
                    # This is the place to check if there are no moves in the draw pile and initiate a new deal
                    nomoremoves = evaluateDeck()
                    if nomoremoves == 1:        # Show deal button
                        if deals == 2:
                            two_deals_button = pygame.image.load(r'C:\Python27\images\2button.png').convert_alpha()
                            deals_button_Rect = pygame.Rect(335,225,26,26)
                            mainSurface.blit(two_deals_button, (335,225))
                        if deals == 1:
                            one_deal_button = pygame.image.load(r'C:\Python27\images\1button.png').convert_alpha()
                            deals_button_Rect = pygame.Rect(335,225,26,26)
                            mainSurface.blit(one_deal_button, (335,225))
                        if deals == 0:
                            print "No more moves. Game over."
                            game_over = font2.render("Game over. No more moves.", True, (255, 255, 255))
                            mainSurface.blit(game_over, (80,403))

                    for c in reversed(list(discard_pile)):
                        c.rect.x = pyramid_left
                        c.rect.y = pyramid_height
                        current_deck.add(c)
                        discard_pile.remove(c)

                    draw_pile_rect_loc = pygame.Rect(0,0,0,0)
                    discard_pile.clear(mainSurface, bg)
                    discard_pile.draw(mainSurface)
                    current_deck.clear(mainSurface, bg)
                    current_deck.draw(mainSurface)
                    discardpileGraphic = pygame.image.load(r'C:\Python27\images\discard.png').convert_alpha()
                    discardpileGraphic = pygame.transform.scale(discardpileGraphic, (180, 295))
                    mainSurface.blit(discardpileGraphic, (pyramid_right, pyramid_height))
                    pygame.display.update()

                # Logic to deal a new board
                if deals_button_Rect.collidepoint((mouse_pos)):
                    play_sound(new_board_sound)
                    play_sound(new_board_sound)
                    play_sound(new_board_sound)

                    mainSurface.blit(bg, (0, 0)) #Display image at 0, 0
                    deals -= 1
                    deals_button_Rect = pygame.Rect(0,0,0,0)

                    current_deck.empty()
                    discard_pile.empty()
                    current_deck.clear(mainSurface, bg)
                    discard_pile.clear(mainSurface, bg)
                    boardSetup()

                    # Then Update the score
                    score_boards_deals()

                else:
                    pass
##                    print "Not clicked"


if __name__ == '__main__':
    main()

# Transparent graphics
##http://www.wikihow.com/Make-a-Transparent-Image-Using-Gimp
##http://nerdparadise.com/tech/python/pygame/blitopacity/
##surface = pygame.image.load('....') # Load alpha bitmap
##rect = pygame.rect.Rect(x, y, width, height) # Area to get
##target.blit(surface.subsurface(rect), (0, 0)) # Blit into another surface
