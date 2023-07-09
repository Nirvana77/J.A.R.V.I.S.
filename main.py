# https://www.youtube.com/watch?v=pVZN03sNRxc
# https://www.youtube.com/watch?v=RAKpMYOlttA
# https://www.youtube.com/watch?v=OqFI_g8vAoc

import pandas as pd
import libs.openai_helper as openai
import libs.command_helper as commands

def load():
	print('Loading JARVIS...')
	print('loading commands...')

	openai.init()
	commands.init()


if __name__ == '__main__':
	load()

	commands.run()