#coding=gbk

class GameStats():
	"""跟踪游戏统计信息"""
	def __init__(self, ai_settings):
		"""初始化统计信息"""
		self.ai_settings = ai_settings
		self.game_active = False	#游戏刚启动时处于非活动状态
		self.reset_stats()
	
	def reset_stats(self):
		"""初始化游戏运行期间可能变化的统计信息"""
		self.ships_left = self.ai_settings.ship_limit  #剩余的飞船数量
		self.score = 0
		self.level = 1
		self.get_high_score() 
	
	def get_high_score(self):
		"""从文件中读取最高分"""
		try:
			with open('score.txt') as score_object:
				score_str = score_object.read()
				self.high_score = int(score_str)
		except FileNotFoundError:
			print("File not found")
			self.high_score = 0
	
	def write_high_score(self):
		"""将最高分写入文件"""
		with open('score.txt', 'w') as score_object:
			score_object.write(str(self.high_score))
