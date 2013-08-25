class ChangeLog():
	changelog = []
	changelog.append("2.1.0: new queue function, bug fixes")
	changelog.append("2.4.1: Changed back to tdtool becuse of problem with pytelldus lib.")
	changelog.append("2.4.2: Added the option to choose between tdtool and td.py from commandline.")
	changelog.append("3.0.0: Moved code from __init__.py to TellstickCtrl.py, and changed database for use with django, rewritten startuprun to be more accurate, and some bug fixes.")
	changelog.append("3.0.1: Rewritten algoritm for on end off times in startup")
	changelog.append("3.0.2: Added string to log for queue")
	def Get(self):
		out = self.changelog
		return out
	




