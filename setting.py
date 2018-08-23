#coding=gbk

class Settings():
	"""�洢�����������ֵ���������"""
	def __init__(self):
		"""��ʼ����Ϸ������"""
		# ��Ļ����
		self.screen_width = 1200
		self.screen_height = 600
		self.bg_color = (230, 230, 230)
		
		
		#�ӵ�����: ������3���ء���15���ص����ɫ�ӵ�, �ӵ����ٶȱȷɴ��Ե�.
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullet_allowed = 3		#δ��ʧ���ӵ�����
		
		#����������
		self.fleet_drop_speed = 10 #������ײ����Ļ��Եʱ��������Ⱥ�����ƶ����ٶ�
		
		#�ɴ�����
		self.ship_limit = 3
		
		#�ӿ���Ϸ������ٶ�
		self.speedup_scale = 1.1
		
		#�����˵���������ٶ�
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
	
	def initialize_dynamic_settings(self):
		"""��ʼ������Ϸ�仯���仯������"""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		self.fleet_direction = 1 #1��ʾ���ƣ�-1��ʾ����
		self.alien_points = 1
	
	def increase_speed(self):
		"""����ٶ�"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
		
		
		
		
