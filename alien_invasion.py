#coding=utf-8
#����һϵ��������Ϸ��Ҫ�õ��Ķ���
import sys

import pygame	#������Ϸ��������Ĺ���

from setting import Settings
from game_stats import GameStats
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from button import Button
from scoreboard import Scoreboard

def run_game():
	# ��ʼ����Ϸ������һ����Ļ����
	pygame.init()
	ai_settings = Settings()
	#��һ��Ԫ��Ϊ����������һ��surface(��Pygame��,surface����Ļ��һ����,������ʾ��ϷԪ��.)
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))  
	pygame.display.set_caption("Alien Invasion")
	
	#����һ�ҷɴ�
	ship = Ship(ai_settings, screen)
	#����һ�����ڴ洢�ӵ��ı���
	bullets = Group()
	#����һ�������˱���
	aliens = Group()
	
	#����������Ⱥ
	gf.create_fleet(ai_settings, screen, ship, aliens)
	#����һ�����ڴ洢��Ϸͳ����Ϣ��ʵ��
	stats = GameStats(ai_settings)
	#����һ����ť
	play_button = Button(ai_settings, screen, "Play")
	#����һ���Ʒ���
	sb = Scoreboard(ai_settings, screen, stats)
	
	#��ʼ��Ϸ��ѭ��
	while True:
		#���Ӽ��̺�����¼�
		gf.check_events(ai_settings, screen, stats, play_button, sb, 
			ship, aliens, bullets)
		
		if stats.game_active:
			#���·ɴ�λ��
			ship.update()
			#�����ӵ���λ��
			gf.update_bullets(ai_settings, screen, ship, sb, stats,  aliens, bullets)
			#���������˵�λ��
			gf.update_aliens(ai_settings, stats, screen, ship, sb, aliens, bullets)
		
		#���»�����Ļ
		gf.update_screen(ai_settings, screen, ship, sb, stats, aliens, bullets, play_button)
		
run_game()

