#!/usr/bin/python3

import os
import subprocess
import re

DF_LOCATION = '/home/jarrad/opt/df'

TEMP_DIR = '/home/jarrad/Downloads/DF'

DFHACK_URL = 'https://github.com/DFHack/dfhack/releases/download/0.43.05-beta1/dfhack-0.43.05-beta1-Linux-64-gcc-4.8.1.tar.bz2'
DFHACK_FILE = 'dfhack.tar.bz2'

TWBT_URL = 'https://github.com/mifki/df-twbt/files/869889/twbt-5.78-linux.zip'
TWBT_FILE = 'twbt.zip'

SF_URL = 'https://github.com/DFgraphics/Spacefox/archive/43.05f.zip'
SF_FILE = 'sf.zip'


def run(cmdString, *args, **kwargs):
	kwargs['shell'] = True
	subprocess.run(cmdString, *args, **kwargs)


run('mkdir -p %s' % TEMP_DIR)


def downloadDFHack():
	os.chdir(TEMP_DIR)
	if os.path.exists(DFHACK_FILE):
		print('DFHack downloaded already, skipping.')
	else:
		print('Downloading DFHack')
		run('wget %s -O %s' % (DFHACK_URL, DFHACK_FILE))


def installDFHack():
	os.chdir(DF_LOCATION)
	print('Installing DFHack')
	run('tar -xf %s' % os.path.join(TEMP_DIR, DFHACK_FILE))
	print('DFHack installed.')


def downloadTWBT():
	os.chdir(TEMP_DIR)
	if os.path.exists(TWBT_FILE):
		print('TWBT downloaded already, skipping.')
	else:
		print('Downloading TWBT')
		run('wget %s -O %s' % (TWBT_URL, TWBT_FILE))
		print('TWBT downloaded.')


def installTWBT():
	TWBT_TEMP_DIR = 'TWBT'
	os.chdir(TEMP_DIR)
	run('rm -r %s' % TWBT_TEMP_DIR)
	run('mkdir -p %s' % TWBT_TEMP_DIR)
	os.chdir(TWBT_TEMP_DIR)
	run('unzip ../%s' % TWBT_FILE)
	run('cp 0.43.05-beta1/*.plug.so %s' %
		os.path.join(DF_LOCATION, 'hack', 'plugins'))
	run('cp *.png %s' % os.path.join(DF_LOCATION, 'data', 'art'))
	run('cp overrides.txt %s' % os.path.join(DF_LOCATION, 'data', 'init'))


def downloadSpaceFox():
	os.chdir(TEMP_DIR)
	if os.path.exists(SF_FILE):
		print('SF downloaded already, skipping.')
	else:
		print('Downloading SF.')
		run('wget %s -O %s' % (SF_URL, SF_FILE))


def installSpaceFox():
	SF_TEMP_DIR = 'spacefox'
	os.chdir(TEMP_DIR)
	run('rm -r %s' % SF_TEMP_DIR)
	run('mkdir -p %s' % SF_TEMP_DIR)
	os.chdir(SF_TEMP_DIR)
	run('unzip ../%s' % SF_FILE)
	os.chdir('Spacefox-43.05f')
	run('cp data/art/* %s' % os.path.join(DF_LOCATION, 'data', 'art'))
	initData = os.path.join(DF_LOCATION, 'data', 'init')
	run('cp data/init/colors.txt %s' % initData)
	run('cp data/init/d_init.txt %s' % initData)
	run('cp data/init/overrides.txt %s' % initData)


def configureDF():
	os.chdir(DF_LOCATION)
	with open('data/init/init.txt', 'r') as f:
		initFile = f.read()

	def setOption(name, value):
		nonlocal initFile
		regex = re.compile('\[%s:.*\]' % name)
		initFile = regex.sub('[%s:%s]' % (name, value), initFile)

	setOption('PRINT_MODE', 'TWBT')
	setOption('GRAPHICS', 'YES')
	setOption('FONT', 'Jecfox_10x16.png')
	setOption('FULLFONT', 'Jecfox_10x16.png')
	setOption('GRAPHICS_FONT', 'Spacefox_16x16_0ther.png')
	setOption('GRAPHICS_FULLFONT', 'Spacefox_16x16_0ther.png')

	with open('data/init/init.txt', 'w') as f:
		f.write(initFile)


downloadDFHack()
installDFHack()
downloadTWBT()
installTWBT()
downloadSpaceFox()
installSpaceFox()
configureDF()
