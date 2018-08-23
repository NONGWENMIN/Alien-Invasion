#coding=gbk

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def fire_bullets(ai_settings, screen, ship, bullets):
	"""如果没有达到限制，则发射一颗子弹"""
	if len(bullets) < ai_settings.bullet_allowed:
		#创建一颗子弹并加入到编组中
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def check_keydown(event, ai_settings, screen, ship, bullets):
	"""响应按键操作"""
	if event.key == pygame.K_RIGHT:		#向右移动飞船
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:	#向左移动飞船
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullets(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:	#可按下Q键退出游戏
		sys.exit()

def check_keyup(event, ship):
	"""处理松开事件"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos() #返回一个元组，其中包含玩家单击时鼠标的x 和y 坐标
			check_play_button(ai_settings, aliens, bullets, stats,
				sb, screen, ship, play_button, mouse_x, mouse_y)

def check_play_button(ai_settings, aliens, bullets, stats, sb, screen, ship, play_button, mouse_x, mouse_y):
	"""在玩家单击按钮后开始新的游戏"""
	#检查鼠标单击位置是否在Play按钮的rect内
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		#重置游戏
		ai_settings.initialize_dynamic_settings()
		#隐藏光标
		pygame.mouse.set_visible(False)
		#重置游戏信息
		stats.reset_stats()
		stats.game_active = True
		
		#重置记分牌图像
		sb.prep_score()
		sb.prep_level()
		sb.prep_high_score()
		sb.prep_ships()
		
		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		
		#创建一群新的外星人并让飞船居中
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
	
def update_screen(ai_settings, screen, ship, sb, stats, aliens, bullets, play_button):
	"""更新屏幕上的图像并切换新屏幕"""
	#每次循环都重绘屏幕
	screen.fill(ai_settings.bg_color)	#用背景色铺满屏幕
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	#显示得分
	sb.show_score()
	#如果游戏处于非活动状态，就绘制Play按钮
	if not stats.game_active:
		play_button.draw_button()
		 
	#让最近绘制的屏幕可见
	pygame.display.flip()
	
	
def check_bullet_alien_collisions(ai_settings, screen, stats, sb,  ship, aliens, bullets):
	"""响应子弹和外星人间的碰撞"""
	#检查子弹是否击中了外星人，如果是的话，删除相应的子弹和外星人
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions: #计分
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	
	if len(aliens) == 0:	#整群外星人都被消灭了
		#删除现有的子弹, 加快游戏节奏, 并新建一群外星人
		bullets.empty()
		ai_settings.increase_speed()
		
		#提高等级
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, ship, sb, stats,  aliens, bullets):
	"""更新子弹的位置并删除消失的子弹"""
	#更新子弹位置
	bullets.update()  #自动对编组内的每个子弹调用update
		
	#删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	check_bullet_alien_collisions(ai_settings, screen, stats, sb,  ship, aliens, bullets)
	

def get_number_rows(ai_settings, ship_height, alien_height):
	"""计算屏幕可以容纳多少行外星人"""
	avaiable_space_y = (ai_settings.screen_height 
							- (3*alien_height) - ship_height)
	number_rows = int(avaiable_space_y / (2 * alien_height))
	return number_rows
			
def get_number_aliens_x(ai_settings, alien_width):
	"""计算一行可以容纳多少外星人, 外星人的间距为外星人的宽度"""
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""创建一个外星人并加入当前的行"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	#创建一个外星人并计算一行可以容纳多少外星人
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	#创建第一行外星人
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x ):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
	"""有外星人到达边缘时采取相应措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""将整群外星人下移，并改变他们的方向"""
	for  alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
	"""响应被外星人撞到的飞船"""
	if stats.ships_left > 0:
		#ship_left 减一
		stats.ships_left -= 1
		#更新记分牌
		sb.prep_ships()
	
		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
	
		#创建一群新的外星人并将飞船放到屏幕中央
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		#暂停一会
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, sb, aliens, bullets):
	"""检查是否有外星人到达了屏幕底部"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#像飞船被撞到一样处理
			ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
			break

def update_aliens(ai_settings, stats, screen, ship, sb, aliens, bullets):
	"""检查是否有外星人位于屏幕边缘，更新外星人群中所有外星人的位置"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
	
	#检查是否有外星人到达屏幕底端
	check_aliens_bottom(ai_settings, stats, screen, ship, sb, aliens, bullets)

def check_high_score(stats, sb):
	"""检查是否产生了最高分"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		stats.write_high_score()

			


	

	


		
