import pygame, sys, time, random, math

pygame.init()

size = width, height = 550, 400

screen = pygame.display.set_mode(size)

###
### Fonctions diverses
###

def collisionSourisRect(rect):
	return (pygame.mouse.get_pos()[0] > rect.left and pygame.mouse.get_pos()[0] < rect.right) and (pygame.mouse.get_pos()[1] > rect.top and pygame.mouse.get_pos()[1] < rect.bottom)
###
###
###

def jeu():
	
	## Parametres du bg
	bg = pygame.image.load("background.png")
	bgRect = bg.get_rect()

	## Parametres de la lelcorne

	lelcorne = pygame.image.load("lelcorne.png")
	lelcorneRect = lelcorne.get_rect()
	lelcorneRect.move_ip([width/2-lelcorneRect.width/2, height - lelcorneRect.height -10])
	vitesse = 2
	avanceDroite = False
	avanceGauche = False
	mort = False

	## Parametres de l'anti-campeurs
	tempsImmo = time.time()
	interImmo = 2
	anciennePos = -1
	immo = False
	
	## Bruit de la Lelcorne

	bruit = pygame.mixer.Sound("lelcorne-sound.ogg")
	bruit.set_volume(0.2)
	bruitClock = pygame.time.Clock()

	## Parametres des sauces
	
	sauce = pygame.image.load("sauce.png")
	listeSauces = []
	interSpawn = 1
	vitesseSauce = 2
	spawnSauce = 0
	listeSaucesSuppr = []

	## Parametres de l'explosion
	#expl = pygame.image.load("explosion.png")
	#explRect = expl.get_rect()
	
	
	## Texte de score
	
	score = 0
	scoreFont = pygame.font.Font(None, 24)
	couleurScore = pygame.color.Color("White")
	
	## Texte de mort
	
	tempsMort = 0
	mortFont = pygame.font.Font(None, 70)
	couleurMort = pygame.color.Color("White")
	mortText = "#REKT"
	mortImage = mortFont.render(mortText, True, couleurScore)
	mortRect = mortImage.get_rect()
	mortRect.move_ip([(width - mortFont.size(mortText)[0])/2, (height - mortFont.size(mortText)[1])/2])
	
	## Texte rejouer
	
	rejouer = False
	rejouerFont = pygame.font.Font(None, 50)
	couleurRejouer = pygame.color.Color("White")
	couleurRejouerHover = pygame.color.Color("Red")
	rejouerText = "Rejouer ?"
	rejouerImage = mortFont.render(rejouerText, True, couleurRejouer)
	rejouerRect = rejouerImage.get_rect()
	rejouerRect.move_ip([(width - rejouerFont.size(rejouerText)[0])/2, height - mortRect.bottom + 50])

	while 1:

		move = [0,0]

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					avanceGauche = True
				if event.key == pygame.K_d:
					avanceDroite = True
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_q:
					avanceGauche = False
				if event.key == pygame.K_d:
					avanceDroite = False
				if event.key == pygame.K_r and mort:
					rejouer = True
				if event.key == pygame.K_ESCAPE:
					sys.exit()
			
		## Mouvement du perso
			
		if avanceGauche and lelcorneRect.left > 0 and not(mort):
			move[0] = - vitesse
		if avanceDroite and lelcorneRect.right < width and not(mort):
			move[0] = vitesse
					
		lelcorneRect = lelcorneRect.move(move)
		
		## Spawn des sauces : Kikkoman, Kikkoman!
	
		if time.time() - spawnSauce >= interSpawn:
			spawnSauce = time.time()
			nouvelleSauce = sauce.get_rect()
			nouvelleSauce.move_ip([random.randint(0, width-nouvelleSauce.width), -nouvelleSauce.height])
			listeSauces.append(nouvelleSauce)
	
		## Verif anti-campeurs

		if anciennePos == lelcorneRect.left:
			if not(immo):
				tempsImmo = time.time()
			immo = True
		else:
			immo = False
			tempsImmo = time.time()
		anciennePos = lelcorneRect.left

		## Die Lelcorne!

		for i in range(len(listeSauces)):
			if listeSauces[i].bottom > lelcorneRect.top:
				if (listeSauces[i].left >= lelcorneRect.left and listeSauces[i].left <= lelcorneRect.right) or (listeSauces[i].right >= lelcorneRect.left and listeSauces[i].right <= lelcorneRect.right):
					mort = True
					#tempsMort = time.time()
					#explRect.move_ip([(abs(listeSauces[i].right - lelcorneRect.left)+explRect.right)/2, (abs(listeSauces[i].bottom - lelcorneRect.top)+explRect.bottom)/2])
			if listeSauces[i].y > height:
				listeSaucesSuppr.append(i)		
			else:
				listeSauces[i] = listeSauces[i].move([0, vitesseSauce])
	
		if time.time() - tempsImmo >= interImmo and immo:
			mort = True

		## MAJ du score
	
		scoreText = "Score : " + str(score)
		scoreImage = scoreFont.render(scoreText, True, couleurScore)
		scoreRect = scoreImage.get_rect()
		scoreRect.move_ip([width - scoreFont.size(scoreText)[0] -5, height - scoreFont.size(scoreText)[1] -5])

		vitesseSauce = score/10 + 1

		if score % 10 == 0 and score != 0 and not(mort):
			bruit.play()
			bruitClock.tick()
		bruitClock.tick()
		if bruitClock.get_time() >= 3000:
			bruit.stop()
	
		screen.fill((0,0,0))
			
		## Blit des surfaces
	
		screen.blit(bg, bgRect)
		if not(mort):
			screen.blit(lelcorne, lelcorneRect)
			for sauceRect in listeSauces:
				screen.blit(sauce, sauceRect)
			if listeSauces != []:
				for i in listeSaucesSuppr:
					listeSauces.pop(i)
					score += 1
				listeSaucesSuppr = []
			screen.blit(scoreImage, scoreRect)

		else:
			screen.blit(scoreImage, scoreRect)
			if collisionSourisRect(rejouerRect) or rejouer:
				rejouerImage = rejouerFont.render(rejouerText, True, couleurRejouerHover)
				if pygame.mouse.get_pressed()[0] or rejouer:
					rejouer = False
					mort = False
					score = 0
					spawnSauce = 0
					listeSauces = []
					listeSaucesSuppr = []
					immo = False

			else:
				rejouerImage = rejouerFont.render(rejouerText, True, couleurRejouer)
			screen.blit(rejouerImage, rejouerRect)
			screen.blit(mortImage, mortRect)
			rejouer = False
	
		## On affiche maggle
	
		pygame.display.flip()

###
###
###

def menu():

	## BG du menu 

	bgMenu = pygame.image.load("bgmenu.png")
	bgMenuRect = bgMenu.get_rect()

	## Texte de lancement

	jouerFont = pygame.font.Font(None, 50)
	couleurJouer = pygame.color.Color("Black")
	couleurJouerHover = pygame.color.Color("Red")
	jouerText = "Jouer ! (Entree)"
	jouerImage = jouerFont.render(jouerText, True, couleurJouer)
	jouerRect = jouerImage.get_rect()
	jouerRect.move_ip([width - jouerFont.size(jouerText)[0], (height - jouerFont.size(jouerText)[1])/2])

	jouer = False
	
	while not(jouer):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					sys.exit()
				if event.key == pygame.K_RETURN:
					jouer = True
			
			
		if collisionSourisRect(jouerRect):
			jouerImage = jouerFont.render(jouerText, True, couleurJouerHover)
			if pygame.mouse.get_pressed()[0]:
				jouer = True
		else:
			jouerImage = jouerFont.render(jouerText, True, couleurJouer)
	
		screen.fill((255,255,255))
		
		screen.blit(bgMenu, bgMenuRect)
		screen.blit(jouerImage, jouerRect)
	
		pygame.display.flip()

	jeu()
	
## Action !

menu()
		
