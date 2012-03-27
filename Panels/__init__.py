import os

panels = []

for root, dirs, files in os.walk(os.path.curdir + '/Panels'):
	for file in files:
		if file.startswith('_'):
			continue
		if file.endswith('.py'):
			fileName = file[:file.find('.py')]
			panels.append(fileName)

import terminal
import boot
import explorer
import const
