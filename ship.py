#coding=gbk

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self, ai_settings, screen):	#screenָ���ɴ�Ҫ���Ƶ�ʲô�ط�
		"""��ʼ���ɴ����������ʼλ��"""
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#�ƶ���־
		self.moving_right = False
		self.moving_left = False
		
		#���طɴ�ͼ�񲢻�ȡ����Ӿ���
		self.image = pygame.image.load('images/ship.bmp')	#����һ����ʾ�ɴ���surface
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#��ÿ���·ɴ�������Ļ�ײ�����
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		#�ڷɴ�������center�д洢С��ֵ
		self.center = float(self.rect.centerx)
		
	def blitme(self):
		"""��ָ��λ�û��Ʒɴ�"""
		self.screen.blit(self.image, self.rect)
		
	def update(self):
		"""�����ƶ���־�������ɴ�λ��"""
		#����centerֵ������rect
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		elif self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		#����self.center����rect����
		self.rect.centerx = self.center
	
	def center_ship(self):
		"""�÷ɴ�����"""
		self.center = self.screen_rect.centerx
			
		
