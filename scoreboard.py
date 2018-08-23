#coding=gbk
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	"""显示得分信息的类"""
	
	def __init__(self, ai_settings, screen, stats):
		"""初始化显示得分涉及的属性"""
		self.ai_settings = ai_settings
		self.screen_rect = screen.get_rect()
		self.screen = screen
		self.stats = stats
		
		#显示得分信息时使用的字体设置
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		
		#准备初始得分图像(最高分和当前得分）和等级包含的图像
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
	
	def prep_level(self):
		"""将等级转换为渲染的图像"""
		self.level_image = self.font.render("Level: "+str(self.stats.level), True,
			self.text_color, self.ai_settings.bg_color)
		#将等级放在得分的下面
		self.level_rect = self.level_image.get_rect()
		self.level_rect.centerx = self.screen_rect.centerx + 100
		self.level_rect.top = self.score_rect.top
	
	def prep_high_score(self):
		"""将最高得分转换为渲染的图像"""
		high_score = int(self.stats.high_score)
		high_score_str = "Highest Score: "+"{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,
			self.text_color, self.ai_settings.bg_color)
		#将最高得分放在屏幕右上角
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.right = self.screen_rect.right - 20
		self.high_score_rect.top = 20
	
	def prep_score(self):
		"""将得分转换为一幅渲染的图像"""
		rounded_score = int(self.stats.score)
		score_str = "Score: "+"{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color,
			self.ai_settings.bg_color)
		#将得分放在屏幕顶部中央
		self.score_rect = self.score_image.get_rect()
		self.score_rect.centerx = self.screen_rect.centerx - 200
		self.score_rect.top = 20
		
	
	def prep_ships(self):
		"""显示还余下多少艘飞船"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
		
	def show_score(self):
		"""在屏幕上显示得分和飞船"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)
