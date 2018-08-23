#coding=gbk

class GameStats():
	"""������Ϸͳ����Ϣ"""
	def __init__(self, ai_settings):
		"""��ʼ��ͳ����Ϣ"""
		self.ai_settings = ai_settings
		self.game_active = False	#��Ϸ������ʱ���ڷǻ״̬
		self.reset_stats()
	
	def reset_stats(self):
		"""��ʼ����Ϸ�����ڼ���ܱ仯��ͳ����Ϣ"""
		self.ships_left = self.ai_settings.ship_limit  #ʣ��ķɴ�����
		self.score = 0
		self.level = 1
		self.get_high_score() 
	
	def get_high_score(self):
		"""���ļ��ж�ȡ��߷�"""
		try:
			with open('score.txt') as score_object:
				score_str = score_object.read()
				self.high_score = int(score_str)
		except FileNotFoundError:
			print("File not found")
			self.high_score = 0
	
	def write_high_score(self):
		"""����߷�д���ļ�"""
		with open('score.txt', 'w') as score_object:
			score_object.write(str(self.high_score))
