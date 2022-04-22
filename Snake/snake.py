import pygame,sys,random
from pygame.math import Vector2

game_start = 0	#game hasn't started yet
ins_score = 0
bonus = 0
active_bonus = 0
pauseState = 0
CurrentLevel = 1	#initialize current game level
speed = 200
levelUp = 0
lastLevelUp = 0	#store last level start score
playerTop = 0	#if current player has high score
CurrenHigh = 0	#Current High score
scoreLoss = 0	#if 1 so loss score
gOverSound = 1	#game over sound


class SNAKE:
	def __init__(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)] #self.body[0] is the head	[YES]
		#self.body = [Vector2(15,30),Vector2(14,30),Vector2(13,30)] #self.body[0] is the head

		self.direction = Vector2(0,0)	#it will by the player, by default it is 0,0
		#self.direction = Vector2(5,0)
		self.new_block = False

		self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
		self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
		self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
		self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
		self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
		self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
		self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
		self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

		self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
		self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

		self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
		self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
		self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
		self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
		self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
		self.overSound = pygame.mixer.Sound('Sound/nokiaGameOver.mp3')

	def draw_snake(self):
		self.update_head_graphics()
		self.update_tail_graphics()

		for index,block in enumerate(self.body):	#index is indexing and block is the actual object
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:	#roatating head
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:	#roatating tail
				screen.blit(self.tail,block_rect)
			else:			#rotating body
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:	#going just straight
					screen.blit(self.body_vertical,block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)

	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = self.head_left
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = self.head_up
		elif head_relation == Vector2(0,-1): self.head = self.head_down

	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]	#last is -1, before it -2
		if tail_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

	def move_snake(self):
		if self.new_block == True:
			body_copy = self.body[:]	#copy all elements
			body_copy.insert(0,body_copy[0] + self.direction)	#assign an block at begining with its direction or move
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]	#copy all element except last 1
			body_copy.insert(0,body_copy[0] + self.direction)	#assign an block at begining with its direction or move
			self.body = body_copy[:]

	def add_block(self):
		self.new_block = True

	def play_game_over(self):
		self.overSound.play()

	def play_crunch_sound(self):
		self.crunch_sound.play()

	def reset(self):	#reset the game to intial position
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(0,0)


class FRUIT:
	def __init__(self):
		self.randomize()
		self.randomR()


	def draw_fruit(self):
		fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
		#self.ren = random.randint(1, 3)
		global active_bonus

		if ins_score != 0 and ins_score%50 == 0 and active_bonus == 1:
			self.bonRen = random.randint(1, 3)
			self.renam = str(self.bonRen) + ".png"
			apple = pygame.image.load("Graphics/" + self.renam).convert_alpha()
			screen.blit(apple, fruit_rect)
			global bonus
			bonus = 1
			#active_bonus = 0
		else:
			self.renam = str(self.ren) + ".png"
			global scoreLoss
			if self.ren == 4:
				scoreLoss = 1
			else:
				scoreLoss = 0
			#self.foodImage = pygame.image.load("component/foods/" + self.foS).convert()
			apple = pygame.image.load("Graphics/"+self.renam).convert_alpha()
			#apple = pygame.image.load('Graphics/apple.png').convert_alpha()
			screen.blit(apple,fruit_rect)
			#pygame.draw.rect(screen,(126,166,114),fruit_rect)

	def randomize(self):
		self.x = random.randint(1,cell_number - 5)
		self.y = random.randint(1,cell_number - 5)
		self.pos = Vector2(self.x,self.y)

	def randomR(self):
		self.ren = random.randint(1, 4)


class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()

	def update(self):
		self.snake.move_snake()
		self.check_collision()
		self.check_fail()

	def pauseGame(self):
		paused = True
		global pauseState
		pauseState = 1

		while paused:
			self.draw_elements()
			pygame.display.update()
			self.drawPause()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.drawPause()
					pygame.quit()
					#quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_c:
						paused = False
						pauseState = 0
					elif event.key == pygame.K_q:
						pygame.quit()
						quit()

	def draw_elements(self):
		self.draw_grass()
		self.fruit.draw_fruit()
		self.snake.draw_snake()
		self.draw_score()
		global pauseState
		if pauseState == 1 :
			self.drawPause()
			#print("ok")

	def cal_randomize(self):
		self.fruit.randomize()
	def cal_randomR(self):
		self.fruit.randomR()

	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize()
			self.snake.add_block()
			self.snake.play_crunch_sound()
			self.fruit.randomR()
			global ins_score
			global bonus
			global scoreLoss
			if scoreLoss == 1 and ins_score >= 10:
				ins_score = ins_score-10
				scoreLoss = 0
			elif bonus == 1:
				ins_score = ins_score+20
				bonus = 0
			else:
				ins_score = ins_score+10
			if ins_score%50 == 0:
				global active_bonus
				active_bonus = 1

		for block in self.snake.body[1:]:	#if randomize food got in snake body then rondomize again
			if block == self.fruit.pos:
				self.fruit.randomize()

	def HighScoreFun(self):
		file1 = open('appData.txt', 'r')
		hiScore = file1.read()
		file1.close()
		global playerTop
		#print(len(self.snake.body)-3)
		if ins_score > int(hiScore):  # update final score
			playerTop = 1
			value = ins_score
			file2 = open('appData.txt', 'w')
			file2.write(str(value))
			file2.close()

	def check_fail(self):
		global lastLevelUp
		global speed
		global CurrentLevel
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			global game_start
			game_start = 0
			global ins_score
			#ins_score = 0
			lastLevelUp = 0
			CurrentLevel = 1	#intialize level 0 again
			speed = 200
			self.HighScoreFun()
			#self.gameOverInterface()
			self.game_over()

		for block in self.snake.body[1:]:	#collision with snake itself
			if block == self.snake.body[0]:
				game_start = 0
				CurrentLevel = 1	##intialize level 0 again
				lastLevelUp = 0
				speed = 200
				#print("yes")
				self.HighScoreFun()
				#global ins_score
				if ins_score == 0:
					self.snake.reset()	#it reset each time although the game not started
				else:
					#ins_score = 0
					self.game_over()
				#self.gameOverInterface()

		
	def game_over(self):
		#self.snake.reset()
		paused = True
		global pauseState
		global gOverSound
		pauseState = 2

		while paused:
			#self.draw_elements()
			self.drawGameOver()
			pygame.display.update()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.drawGameOver()
					pygame.quit()
				# quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						gOverSound = 1
						paused = False
						pauseState = 0
						self.snake.reset()
					elif event.key == pygame.K_q:
						pygame.quit()
						quit()
	def drawGameOver(self):

		# score_text = str(len(self.snake.body) - 3)
		#print("got it")
		global  gOverSound
		if gOverSound == 1:
			self.snake.play_game_over()
			gOverSound = 0
		score_text = str("Game Over.Press Enter to play or Q to exit")
		global ins_score
		global playerTop
		#print(ins_score)



		#hiScoreText = str(hiScore)  # highscore
		#hiScoreText = "Hi:" + hiScoreText  # highscore
		# score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text, True, (56, 74, 12))
		score_x = 300
		score_y = 150
		score_rect = score_surface.get_rect(center=(score_x, score_y))
		screen.blit(score_surface, score_rect)
		if playerTop == 1:
			print("ok")
			hscore_text = str("Congrats! You achieved high score")
			hscore_surface = game_font.render(hscore_text, True, (56, 74, 12))
			hscore_x = 300
			hscore_y = 100
			hscore_rect = hscore_surface.get_rect(center=(hscore_x, hscore_y))
			screen.blit(hscore_surface, hscore_rect)
			playerTop = 0


		ins_score = 0


	def draw_grass(self):
		grass_color = (167,209,61)
		#grass_color = (0,0,0)
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			


	def draw_score(self):
		file1 = open('appData.txt', 'r')	#get saved high score
		hiScore = file1.read()
		#p_Hi = sFont.render(f"High Score: {hiScore}", True, (200, 200, 200))  # show high score
		#self.surface.blit(p_Hi, (5, 10))
		file1.close()

		#score_text = str(len(self.snake.body) - 3)
		global speed
		global levelUp
		global lastLevelUp
		global CurrentLevel
		if ins_score%200 == 0 and lastLevelUp != ins_score:
			speed = speed/1.5
			speed = int(speed)
			levelUp = 1
			lastLevelUp = ins_score
		score_text = str(ins_score)

		hiScoreText = str(hiScore)	#highscore
		hiScoreText = "Hi:"+hiScoreText	#highscore
		levelText = str(CurrentLevel)
		levelText = "Level:" + levelText
		#score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text,True,(56,74,12))
		highScore_surface = game_font.render(hiScoreText,True,(56,74,12))
		level_surface = game_font.render(levelText,True,(56,74,12))
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		high_score_x = 45	#high score coordinate
		high_score_y = 23
		level_x = 550
		level_y = 13
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		hScore_rect = highScore_surface.get_rect(center = (high_score_x,high_score_y))	#highscore
		level_rect = level_surface.get_rect(center = (level_x,level_y))	#highscore

		#apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		#bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)
		#bg_rect2 = pygame.Rect(5,5,apple_rect.width + score_rect.width + 6,apple_rect.height)	#high score boundary
		bg_rect2 = pygame.Rect(5,5,100,30)	#high score boundary
		bg_rect = pygame.Rect(495,543,100,30)	#high score boundary
		#levelBg = pygame.Rect(100,100,100,30)	#level boundary

		pygame.draw.rect(screen,(167,209,61),bg_rect)
		pygame.draw.rect(screen,(167,209,61),bg_rect2)	#highscore
		#pygame.draw.rect(screen,(167,209,61),levelBg)	#highscore

		screen.blit(score_surface,score_rect)
		screen.blit(highScore_surface,hScore_rect)	#highscore
		screen.blit(level_surface,level_rect)	#highscore

		#screen.blit(apple,apple_rect)	#draw apple beside score
		pygame.draw.rect(screen,(56,74,12),bg_rect,2)	#frame/border of rectangle
		pygame.draw.rect(screen,(56,74,12),bg_rect2,2)	#frame/border of high score
		#pygame.draw.rect(screen,(56,74,12),levelBg,2)	#frame/border level

	def drawPause(self):

		# score_text = str(len(self.snake.body) - 3)
		#print("got it")
		score_text = str("Press C to continue or Q to quit")
		#hiScore = 40

		#hiScoreText = str(hiScore)  # highscore
		#hiScoreText = "Hi:" + hiScoreText  # highscore
		# score_text = str(len(self.snake.body) - 3)
		score_surface = game_font.render(score_text, True, (56, 74, 12))
		#highScore_surface = game_font.render(hiScoreText, True, (56, 74, 12))
		score_x = 200
		score_y = 100
		#high_score_x = 200  # high score coordinate
		#high_score_y = 200
		score_rect = score_surface.get_rect(center=(score_x, score_y))
		#hScore_rect = highScore_surface.get_rect(center=(high_score_x, high_score_y))  # highscore

		# apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		# bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)
		# bg_rect2 = pygame.Rect(5,5,apple_rect.width + score_rect.width + 6,apple_rect.height)	#high score boundary
		#bg_rect2 = pygame.Rect(200, 200, 100, 30)  # high score boundary
		bg_rect = pygame.Rect(100, 100, 100, 30)  # high score boundary

		#pygame.draw.rect(screen, (167, 209, 61), bg_rect)
		#pygame.draw.rect(screen, (167, 209, 61), bg_rect2)  # highscore

		screen.blit(score_surface, score_rect)
		#screen.blit(highScore_surface, hScore_rect)  # highscore

		# screen.blit(apple,apple_rect)	#draw apple beside score
		#pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)  # frame/border of rectangle
		#pygame.draw.rect(screen, (56, 74, 12), bg_rect2, 2)  # frame/border of high score




pygame.mixer.pre_init(44100,-16,2,512)	#make instant sound exactly when collision
pygame.init()
#cell_size = 40
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))	#screen size
clock = pygame.time.Clock()
#apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,speed)	#Translation after each 150 milisecond
#pygame.time.set_timer(SCREEN_UPDATE,75)	#Translation after each 150 milisecond

def speedup():
	pygame.time.set_timer(SCREEN_UPDATE, speed)

main_game = MAIN()
fr = FRUIT()

food_time = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == SCREEN_UPDATE:
			speedup()	#intial speedup after gameOver
			main_game.update()
		if event.type == pygame.KEYDOWN:	#ready for key stroke event
			game_start = 1	#game has started
			if event.key == pygame.K_UP:
				if main_game.snake.direction.y != 1:
					main_game.snake.direction = Vector2(0,-1)	#update direction
			if event.key == pygame.K_RIGHT:
				if main_game.snake.direction.x != -1:
					main_game.snake.direction = Vector2(1,0)
			if event.key == pygame.K_DOWN:
				if main_game.snake.direction.y != -1:
					main_game.snake.direction = Vector2(0,1)
			if event.key == pygame.K_LEFT:
				if main_game.snake.direction.x != 1:
					main_game.snake.direction = Vector2(-1,0)
			if event.key == pygame.K_p:
				main_game.pauseGame()

	#if food_time == 100 or food_time > 100:

	food_time = food_time + 1
	#global active_bonus
	if (food_time == 5000 or food_time > 5000) and game_start == 1:
		#food_ran = FRUIT()
		if active_bonus == 1:
			active_bonus = 0
		#main_game.FRUIT.randomize()
		#fr.randomize()
		main_game.cal_randomize()	#new food position
		main_game.cal_randomR()		#new food item
		main_game.draw_elements()
		food_time = 0
		#speed = 50
	if levelUp == 1 and CurrentLevel < 5:
		levelUp = 0
		CurrentLevel = CurrentLevel+1
		speedup()

	screen.fill((175,215,70))
	#screen.fill((0,0,0))
	#main_game.HighScoreFun()
	main_game.draw_elements()
	#main_game.drawPause()
	pygame.display.update()
	clock.tick(500)