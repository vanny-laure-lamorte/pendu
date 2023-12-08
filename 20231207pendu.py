#----------------------#
# Importer des modules #
#----------------------#

import pygame, random, sys
pygame.init()

#-------------------------------#
# Variables/constantes globales #
#-------------------------------#

# Fenêtre principale
H = 500
L = 700
ecran=pygame.display.set_mode((L,H))
pygame.display.set_caption('JEU DU PENDU')

# Couleurs
black = (0,0, 0)
white = (255,255,255)
blue = (76,117,192)
green = (0,129,65)
red = (216,0,1)
grey = (222,225,230)
dark_grey = (92,93,94)
gris = (52,53,65)

# Police 
police = pygame.font.Font(None, 36)
police_menu = pygame.font.Font(None, 50)
police_option = pygame.font.Font(None, 21)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)

word = ''
buttons = []
deviner = []
limbs = 0

# Importer des images pour le jeu du pendu
pendu_images = [pygame.image.load('images/pendu7.jpg'), pygame.image.load('images/pendu6.jpg'), pygame.image.load('images/pendu5.jpg'), pygame.image.load('images/pendu4.jpg'), pygame.image.load('images/pendu3.jpg'), pygame.image.load('images/pendu2.jpg'), pygame.image.load('images/pendu1.jpg')]

#---------------------------#
# Les fonctions principales #
#---------------------------#

def ecran_jeu():
    global deviner
    global pendu_images
    global limbs
    ecran.fill(white)

# Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:          
            label = btn_font.render(chr(buttons[i][5]), 1, dark_grey)
            ecran.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, deviner)
    label1 = guess_font.render(spaced, 1, black)
    rect = label1.get_rect()
    length = rect[2]
    
    ecran.blit(label1,(L/2 - length/2, 400))

    images = pendu_images[limbs]
    ecran.blit(images, (L/2 - images.get_width()/2 + 20, 150))

    lettres_choisies(deviner) 
    pygame.display.update()

# Choisir aléatoirement un mot à deviner dans un fichier "mots"

def mot_random():
    fichier = open("mots.txt")
    f = fichier.readlines()
    i = random.randrange(0, len(f) - 1)
    return f[i][:-1]

# Vérifier si la lettre proposée n'est pas déja dans le mot à deviner

def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False
    
# Renvoyer partiellement le mot à deviner avec les lettres déjà selectionnées

def spacedOut(word, deviner=[]):
    spacedWord = ''
    guessedLetters = deviner
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord          

# Vérifier si un bouton a été cliqué
def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None

# Afficher un message en cas de victoire ou défaite
def end(winner=False):
    global limbs
    lostTxt = "Vous avez perdu..."
    winTxt = 'Bravo ! Vous avez gagné'
    ecran_jeu()
    pygame.time.delay(1000)
    ecran.fill(white)

    if winner == True:
        label = lost_font.render(winTxt, 1, green)
    else:
        label = lost_font.render(lostTxt, 1, red)

    wordTxt = lost_font.render(word.upper(), 1, dark_grey)
    wordWas = lost_font.render("Voici le à deviner: ", 1, dark_grey)

    ecran.blit(wordTxt, (L/2 - wordTxt.get_width()/2, 295))
    ecran.blit(wordWas, (L/2 - wordWas.get_width()/2, 245))
    ecran.blit(label, (L / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()

# Réinitialiser les paramètres du jeu pour jouer à nouveau
def reset():
    global limbs
    global deviner
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    deviner = []
    word = mot_random()

# Setup buttons
increase = round(L / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([grey, x, y, 20, True, 65 + i])

word = mot_random()

#----------------------#
# Niveau de difficulté #
#----------------------#

def set_difficulty (value, difficulty):    
    pass

#-------------------#
# Jeu 1/2: Le pendu #
#-------------------#

def game_pendu ():  
    global inPlay, word, deviner, buttons, limbs
    inPlay = True
    word = mot_random()
    reset()
    
    while inPlay:

        ecran_jeu()
        pygame.time.delay(10)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
                elif pygame.K_a <= event.key <= pygame.K_z:
                    letter = chr(event.key).upper()
                    if letter not in deviner:
                        deviner.append(letter)
                        for btn in buttons:
                            if chr(btn[5]) == letter:
                                btn[4] = False
                        if hang(letter):
                            if limbs != 6:
                                limbs += 1
                            else:
                                end()
                        else:
                            if spacedOut(word, deviner).count('_') == 0:
                                end(True)   

def lettres_choisies(deviner):
    guessed_letters_text = 'Lettres déja proposées : ' + ', '.join(deviner)
    guessed_text =  btn_font.render(guessed_letters_text, True, dark_grey)
    ecran.blit(guessed_text, (20, H-35))

#---------------------------#
# Jeu 2/2: Insérer des mots #
#---------------------------#

def game_mot_deviner():    

    new_mot = ""
    ajout_termine = False    

    while not ajout_termine:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ajout_termine = True 
                main_menu() 
                break                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ajout_termine = True
                elif event.key == pygame.K_BACKSPACE:
                    new_mot = new_mot[:-1]
                elif event.unicode.isalpha():
                    new_mot += event.unicode  

        ecran.fill(blue) 
        title_font = pygame.font.Font(None, 50)
        pygame.draw.rect(ecran, grey, (0, 0, L, 100))
        afficher_texte = title_font.render("INSERER UNMOT À DEVINER", True, gris)
        ecran.blit(afficher_texte, (L // 2 - afficher_texte.get_width() // 2, H // 2 - 225), )        
        
        afficher_new_mot = police_menu.render(new_mot, True, white)
        text_x = L // 2 - afficher_new_mot.get_width() // 2
        text_y = H // 2 - afficher_new_mot.get_height() // 2       

        ecran.blit(afficher_new_mot, (text_x, text_y))
        pygame.display.flip()
        
    with open("mots.txt", 'a') as fichier:
        fichier.write(new_mot.strip () + "\n")
    
    main_menu ()
   
#----------------#
# Menu principal #
#----------------#

def display_menu():
    
    title_font = pygame.font.Font(None, 60)
    title_text = title_font.render('JEU DU PENDU', True, gris)
    title_rect = title_text.get_rect(center=(L // 2, 50))

    text_background1 = pygame.Rect(0, 0, L, 90)  
    pygame.draw.rect(ecran, grey, text_background1)
    hauteur_restante = H - text_background1.height
    text_background2 = pygame.Rect(0, text_background1.height, L, hauteur_restante)  
    pygame.draw.rect(ecran, blue, text_background2)   
    ecran.blit(title_text, title_rect)

# Affichage des options de menu
    options = ['Jouer au pendu', 'Insérer un mot à deviner']
    option_font = pygame.font.Font(None, 36)
    option_spacing = 70
    for index, option in enumerate(options):
        text = option_font.render(option, True, white)
        text_rect = text.get_rect(center=(L // 2, 250 + index * option_spacing))
        ecran.blit(text, text_rect)

    pygame.display.flip()

def main_menu():
    global inPlay
    
    display_menu()
    
    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
                inPlay = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                x, y = mouse_pos
                if 240 < x < 490 and 310 < y < 340:
                    game_mot_deviner()  
                elif 240 < x < 460 and 230 < y < 280: 
                    game_pendu()                    
                elif 510 < x < 600 and 230 < y < 280:
                    in_menu = False
                    inPlay = False  
                    pygame.quit()

if __name__ == '__main__':
    main_menu()

pygame.quit()