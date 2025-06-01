import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
LARGEUR, HAUTEUR = 600, 400
TAILLE_GRILLE = 20
WIN = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Serpent Dévorant")

# Define colors
NOIR = (0, 0, 0)
GRIS_CLAIR = (192, 192, 192)
GRIS_FONCE = (105, 105, 105)
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
ROUGE = (150, 0, 0)
ROUGE_CLAIR = (255, 0, 0)
BLEU_BEBE = (173, 216, 230)
BLEU_BEBE_TITRE = (5, 216, 230)
VIOLET = (128, 0, 128)
BLEU = (8, 255, 255)

# Define directions
HAUT = (0, -1)
BAS = (0, 1)
GAUCHE = (-1, 0)
DROITE = (1, 0)

# Define Snake class
class Serpent:
    def __init__(self):
        self.corps = [(LARGEUR // 2, HAUTEUR // 2)]
        self.direction = random.choice([HAUT, BAS, GAUCHE, DROITE])
        self.agrandir_serpent = False

    def bouger(self):
        x, y = self.corps[0]
        dx, dy = self.direction
        nouvelle_tete = ((x + dx * TAILLE_GRILLE) % LARGEUR, (y + dy * TAILLE_GRILLE) % HAUTEUR)
        if (nouvelle_tete in self.corps or
                nouvelle_tete[0] < TAILLE_GRILLE or nouvelle_tete[0] >= LARGEUR - TAILLE_GRILLE or
                nouvelle_tete[1] < TAILLE_GRILLE or nouvelle_tete[1] >= HAUTEUR - TAILLE_GRILLE):
            return True  # Collision détectée
        self.corps.insert(0, nouvelle_tete)
        if not self.agrandir_serpent:
            self.corps.pop()
        else:
            self.agrandir_serpent = False

    def agrandir(self):
        self.agrandir_serpent = True

    def dessiner(self, surface):
        for i, segment in enumerate(self.corps):
            couleur = BLEU if i > 0 else NOIR  # La tête du serpent est noire
            pygame.draw.rect(surface, couleur, (*segment, TAILLE_GRILLE, TAILLE_GRILLE))

# Define Food class
class Nourriture:
    def __init__(self, obstacles):
        self.position = self.position_aleatoire(obstacles)

    def position_aleatoire(self, obstacles):
        while True:
            x = random.randrange(TAILLE_GRILLE, LARGEUR - TAILLE_GRILLE, TAILLE_GRILLE)
            y = random.randrange(TAILLE_GRILLE, HAUTEUR - TAILLE_GRILLE, TAILLE_GRILLE)
            position = (x, y)
            if position not in [obstacle.position for obstacle in obstacles]:
                return position

    def dessiner(self, surface):
        pygame.draw.rect(surface, ROUGE_CLAIR, (*self.position, TAILLE_GRILLE, TAILLE_GRILLE))

# Define Obstacle class
class Obstacle:
    def __init__(self):
        self.position = self.position_aleatoire()

    def position_aleatoire(self):
        x = random.randrange(TAILLE_GRILLE, LARGEUR - TAILLE_GRILLE, TAILLE_GRILLE)
        y = random.randrange(TAILLE_GRILLE, HAUTEUR - TAILLE_GRILLE, TAILLE_GRILLE)
        return (x, y)

    def dessiner(self, surface):
        pygame.draw.rect(surface, VIOLET, (*self.position, TAILLE_GRILLE, TAILLE_GRILLE))

# Display game over message
def game_over(score, high_score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLANC)
    high_score_text = font.render(f"Meilleur score: {high_score}", True, BLANC)
    restart_text = font.render("Appuyez sur R pour redémarrer", True, BLANC)
    text_rect = score_text.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 20))
    high_score_rect = high_score_text.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
    restart_rect = restart_text.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 40))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Redémarrer le jeu
        WIN.fill(NOIR)  # Remplir l'écran avec la couleur noire
        WIN.blit(score_text, text_rect)
        WIN.blit(high_score_text, high_score_rect)
        WIN.blit(restart_text, restart_rect)
        pygame.display.update()

# Draw checkerboard background
def draw_background(surface):
    for ligne in range(0, HAUTEUR, TAILLE_GRILLE):
        for colonne in range(0, LARGEUR, TAILLE_GRILLE):
            if (ligne // TAILLE_GRILLE + colonne // TAILLE_GRILLE) % 2 == 0:
                couleur = GRIS_CLAIR
            else:
                couleur = GRIS_FONCE
            pygame.draw.rect(surface, couleur, (colonne, ligne, TAILLE_GRILLE, TAILLE_GRILLE))

# Display title screen
def title_screen():
    WIN.fill(NOIR)  # Remplir l'écran avec la couleur noire
    font = pygame.font.Font(None, 36)
    texte = font.render("Bienvenue à Serpent Dévorant !", True, BLEU_BEBE_TITRE)
    rect_texte = texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 80))
    WIN.blit(texte, rect_texte)
    controls_text1 = font.render("Contrôles : Flèches / WASD pour se déplacer", True, BLANC)
    controls_rect1 = controls_text1.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 40))
    WIN.blit(controls_text1, controls_rect1)
    controls_text2 = font.render("R pour redémarrer, ESC pour pauser", True, BLANC)
    controls_rect2 = controls_text2.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
    WIN.blit(controls_text2, controls_rect2)
    prompt_text = font.render("Appuyez sur Entrée pour commencer", True, BLEU_BEBE_TITRE)
    prompt_rect = prompt_text.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 40))
    WIN.blit(prompt_text, prompt_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# Define main function
def main():
    title_screen()  # Afficher l'écran de titre

    clock = pygame.time.Clock()
    serpent = Serpent()
    nourriture = Nourriture([])
    obstacles = [Obstacle() for _ in range(3)]  # Créer une liste d'obstacles
    score = 0
    meilleur_score = charger_meilleur_score()
    fps = 5
    apples_eaten = 0

    en_cours = True
    en_pause = False
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and serpent.direction != BAS:
                    serpent.direction = HAUT
                elif event.key == pygame.K_s and serpent.direction != HAUT:
                    serpent.direction = BAS
                elif event.key == pygame.K_a and serpent.direction != DROITE:
                    serpent.direction = GAUCHE
                elif event.key == pygame.K_d and serpent.direction != GAUCHE:
                    serpent.direction = DROITE
                elif event.key == pygame.K_UP and serpent.direction != BAS:
                    serpent.direction = HAUT
                elif event.key == pygame.K_DOWN and serpent.direction != HAUT:
                    serpent.direction = BAS
                elif event.key == pygame.K_LEFT and serpent.direction != DROITE:
                    serpent.direction = GAUCHE
                elif event.key == pygame.K_RIGHT and serpent.direction != GAUCHE:
                    serpent.direction = DROITE
                elif event.key == pygame.K_ESCAPE:
                    en_pause = not en_pause
                    if en_pause:
                        pause()

        if not en_pause:
            collision = serpent.bouger()
            if collision or serpent.corps[0] in [obstacle.position for obstacle in obstacles]:
                if score > meilleur_score:
                    sauvegarder_meilleur_score(score)
                    meilleur_score = score
                game_over(score, meilleur_score)
                en_cours = False

            if serpent.corps[0] == nourriture.position:
                serpent.agrandir()
                nourriture.position = nourriture.position_aleatoire(obstacles)
                score += 1
                apples_eaten += 1
                fps += 1
                if apples_eaten == 2:
                    obstacles.append(Obstacle())  # Ajouter un nouvel obstacle
                    apples_eaten = 0

            # Dessiner tout
            draw_background(WIN)  # Dessiner l'arrière-plan en damier
            pygame.draw.rect(WIN, BLEU_BEBE, (0, 0, LARGEUR, TAILLE_GRILLE))  # Dessiner la bordure supérieure
            pygame.draw.rect(WIN, BLEU_BEBE, (0, 0, TAILLE_GRILLE, HAUTEUR))  # Dessiner la bordure gauche
            pygame.draw.rect(WIN, BLEU_BEBE, (0, HAUTEUR - TAILLE_GRILLE, LARGEUR, TAILLE_GRILLE))  # Dessiner la bordure inférieure
            pygame.draw.rect(WIN, BLEU_BEBE, (LARGEUR - TAILLE_GRILLE, 0, TAILLE_GRILLE, HAUTEUR))  # Dessiner la bordure droite
            serpent.dessiner(WIN)
            nourriture.dessiner(WIN)
            for obstacle in obstacles:
                obstacle.dessiner(WIN)

            # Afficher le score et le meilleur score
            font = pygame.font.Font(None, 24)
            score_text = font.render(f"Score: {score}", True, NOIR)
            meilleur_score_text = font.render(f"Meilleur score: {meilleur_score}", True, NOIR)
            WIN.blit(score_text, (10, 10))
            WIN.blit(meilleur_score_text, (10, 30))

            pygame.display.update()

        clock.tick(fps)  # Réglage des FPS

    pygame.quit()
    sys.exit()

# Fonction pour charger le meilleur score à partir d'un fichier
def charger_meilleur_score():
    try:
        with open("meilleur_score.txt", "r") as fichier:
            return int(fichier.read())
    except FileNotFoundError:
        return 0

# Fonction pour sauvegarder le meilleur score dans un fichier
def sauvegarder_meilleur_score(score):
    with open("meilleur_score.txt", "w") as fichier:
        fichier.write(str(score))

# Fonction pour mettre en pause le jeu
def pause():
    font = pygame.font.Font(None, 36)
    texte = font.render("En pause", True, BLANC)
    rect_texte = texte.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
    WIN.blit(texte, rect_texte)
    pygame.display.update()
    en_pause = True
    while en_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    en_pause = False

if __name__ == "__main__":
    main()

  
