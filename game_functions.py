#coding=gbk

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def fire_bullets(ai_settings, screen, ship, bullets):
	"""���û�дﵽ���ƣ�����һ���ӵ�"""
	if len(bullets) < ai_settings.bullet_allowed:
		#����һ���ӵ������뵽������
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def check_keydown(event, ai_settings, screen, ship, bullets):
	"""��Ӧ��������"""
	if event.key == pygame.K_RIGHT:		#�����ƶ��ɴ�
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:	#�����ƶ��ɴ�
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullets(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:	#�ɰ���Q���˳���Ϸ
		sys.exit()

def check_keyup(event, ship):
	"""�����ɿ��¼�"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets):
	"""��Ӧ����������¼�"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos() #����һ��Ԫ�飬���а�����ҵ���ʱ����x ��y ����
			check_play_button(ai_settings, aliens, bullets, stats,
				sb, screen, ship, play_button, mouse_x, mouse_y)

def check_play_button(ai_settings, aliens, bullets, stats, sb, screen, ship, play_button, mouse_x, mouse_y):
	"""����ҵ�����ť��ʼ�µ���Ϸ"""
	#�����굥��λ���Ƿ���Play��ť��rect��
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		#������Ϸ
		ai_settings.initialize_dynamic_settings()
		#���ع��
		pygame.mouse.set_visible(False)
		#������Ϸ��Ϣ
		stats.reset_stats()
		stats.game_active = True
		
		#���üǷ���ͼ��
		sb.prep_score()
		sb.prep_level()
		sb.prep_high_score()
		sb.prep_ships()
		
		#����������б���ӵ��б�
		aliens.empty()
		bullets.empty()
		
		#����һȺ�µ������˲��÷ɴ�����
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		
	
def update_screen(ai_settings, screen, ship, sb, stats, aliens, bullets, play_button):
	"""������Ļ�ϵ�ͼ���л�����Ļ"""
	#ÿ��ѭ�����ػ���Ļ
	screen.fill(ai_settings.bg_color)	#�ñ���ɫ������Ļ
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	#��ʾ�÷�
	sb.show_score()
	#�����Ϸ���ڷǻ״̬���ͻ���Play��ť
	if not stats.game_active:
		play_button.draw_button()
		 
	#��������Ƶ���Ļ�ɼ�
	pygame.display.flip()
	
	
def check_bullet_alien_collisions(ai_settings, screen, stats, sb,  ship, aliens, bullets):
	"""��Ӧ�ӵ��������˼����ײ"""
	#����ӵ��Ƿ�����������ˣ�����ǵĻ���ɾ����Ӧ���ӵ���������
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions: #�Ʒ�
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	
	if len(aliens) == 0:	#��Ⱥ�����˶���������
		#ɾ�����е��ӵ�, �ӿ���Ϸ����, ���½�һȺ������
		bullets.empty()
		ai_settings.increase_speed()
		
		#��ߵȼ�
		stats.level += 1
		sb.prep_level()
		
		create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, ship, sb, stats,  aliens, bullets):
	"""�����ӵ���λ�ò�ɾ����ʧ���ӵ�"""
	#�����ӵ�λ��
	bullets.update()  #�Զ��Ա����ڵ�ÿ���ӵ�����update
		
	#ɾ���Ѿ���ʧ���ӵ�
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	
	check_bullet_alien_collisions(ai_settings, screen, stats, sb,  ship, aliens, bullets)
	

def get_number_rows(ai_settings, ship_height, alien_height):
	"""������Ļ�������ɶ�����������"""
	avaiable_space_y = (ai_settings.screen_height 
							- (3*alien_height) - ship_height)
	number_rows = int(avaiable_space_y / (2 * alien_height))
	return number_rows
			
def get_number_aliens_x(ai_settings, alien_width):
	"""����һ�п������ɶ���������, �����˵ļ��Ϊ�����˵Ŀ��"""
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""����һ�������˲����뵱ǰ����"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""����������Ⱥ"""
	#����һ�������˲�����һ�п������ɶ���������
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	#������һ��������
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x ):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
	"""�������˵����Եʱ��ȡ��Ӧ��ʩ"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""����Ⱥ���������ƣ����ı����ǵķ���"""
	for  alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
	"""��Ӧ��������ײ���ķɴ�"""
	if stats.ships_left > 0:
		#ship_left ��һ
		stats.ships_left -= 1
		#���¼Ƿ���
		sb.prep_ships()
	
		#����������б���ӵ��б�
		aliens.empty()
		bullets.empty()
	
		#����һȺ�µ������˲����ɴ��ŵ���Ļ����
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		#��ͣһ��
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, sb, aliens, bullets):
	"""����Ƿ��������˵�������Ļ�ײ�"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#��ɴ���ײ��һ������
			ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
			break

def update_aliens(ai_settings, stats, screen, ship, sb, aliens, bullets):
	"""����Ƿ���������λ����Ļ��Ե������������Ⱥ�����������˵�λ��"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#��������˺ͷɴ�֮�����ײ
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
	
	#����Ƿ��������˵�����Ļ�׶�
	check_aliens_bottom(ai_settings, stats, screen, ship, sb, aliens, bullets)

def check_high_score(stats, sb):
	"""����Ƿ��������߷�"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		stats.write_high_score()

			


	

	


		
