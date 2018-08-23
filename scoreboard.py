#coding=gbk
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	"""��ʾ�÷���Ϣ����"""
	
	def __init__(self, ai_settings, screen, stats):
		"""��ʼ����ʾ�÷��漰������"""
		self.ai_settings = ai_settings
		self.screen_rect = screen.get_rect()
		self.screen = screen
		self.stats = stats
		
		#��ʾ�÷���Ϣʱʹ�õ���������
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		
		#׼����ʼ�÷�ͼ��(��߷ֺ͵�ǰ�÷֣��͵ȼ�������ͼ��
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
	
	def prep_level(self):
		"""���ȼ�ת��Ϊ��Ⱦ��ͼ��"""
		self.level_image = self.font.render("Level: "+str(self.stats.level), True,
			self.text_color, self.ai_settings.bg_color)
		#���ȼ����ڵ÷ֵ�����
		self.level_rect = self.level_image.get_rect()
		self.level_rect.centerx = self.screen_rect.centerx + 100
		self.level_rect.top = self.score_rect.top
	
	def prep_high_score(self):
		"""����ߵ÷�ת��Ϊ��Ⱦ��ͼ��"""
		high_score = int(self.stats.high_score)
		high_score_str = "Highest Score: "+"{:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,
			self.text_color, self.ai_settings.bg_color)
		#����ߵ÷ַ�����Ļ���Ͻ�
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.right = self.screen_rect.right - 20
		self.high_score_rect.top = 20
	
	def prep_score(self):
		"""���÷�ת��Ϊһ����Ⱦ��ͼ��"""
		rounded_score = int(self.stats.score)
		score_str = "Score: "+"{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color,
			self.ai_settings.bg_color)
		#���÷ַ�����Ļ��������
		self.score_rect = self.score_image.get_rect()
		self.score_rect.centerx = self.screen_rect.centerx - 200
		self.score_rect.top = 20
		
	
	def prep_ships(self):
		"""��ʾ�����¶����ҷɴ�"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
		
	def show_score(self):
		"""����Ļ����ʾ�÷ֺͷɴ�"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)
