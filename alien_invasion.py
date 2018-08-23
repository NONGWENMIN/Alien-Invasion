#coding=utf-8
#创建一系列整个游戏都要用到的对象
import sys

import pygame	#包含游戏开发所需的功能

from setting import Settings
from game_stats import GameStats
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from button import Button
from scoreboard import Scoreboard

def run_game():
	# 初始化游戏并创建一个屏幕对象
	pygame.init()
	ai_settings = Settings()
	#以一个元组为参数，返回一个surface(在Pygame中,surface是屏幕的一部分,用于显示游戏元素.)
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))  
	pygame.display.set_caption("Alien Invasion")
	
	#创建一艘飞船
	ship = Ship(ai_settings, screen)
	#创建一个用于存储子弹的编组
	bullets = Group()
	#创建一个外星人编组
	aliens = Group()
	
	#创建外星人群
	gf.create_fleet(ai_settings, screen, ship, aliens)
	#创建一个用于存储游戏统计信息的实例
	stats = GameStats(ai_settings)
	#创建一个按钮
	play_button = Button(ai_settings, screen, "Play")
	#创建一个计分排
	sb = Scoreboard(ai_settings, screen, stats)
	
	#开始游戏主循环
	while True:
		#监视键盘和鼠标事件
		gf.check_events(ai_settings, screen, stats, play_button, sb, 
			ship, aliens, bullets)
		
		if stats.game_active:
			#更新飞船位置
			ship.update()
			#更新子弹的位置
			gf.update_bullets(ai_settings, screen, ship, sb, stats,  aliens, bullets)
			#更新外星人的位置
			gf.update_aliens(ai_settings, stats, screen, ship, sb, aliens, bullets)
		
		#重新绘制屏幕
		gf.update_screen(ai_settings, screen, ship, sb, stats, aliens, bullets, play_button)
		
run_game()

