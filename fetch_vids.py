#!/usr/bin/env python3
import os
import datetime
from pathlib import Path
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

CURRENT_PATH = os.path.dirname(__file__)
SAVE_DIR = os.path.join(CURRENT_PATH, 'data')


def convert_to_secs(time):
	count = str(time).rsplit(':', 1)
	if len(count) == 2:
		dt = datetime.datetime.strptime(time, '%M:%S')
	else:
		dt = datetime.datetime.strptime(time, '%H:%M:%S')
	tp = dt - datetime.datetime(1900, 1, 1)
	seconds = tp.total_seconds()
	print('DATE TIME ==> {}'.format(seconds))
	return seconds


def trim_video(file, begin, end, video_counter):
	print('STATUS :: trimming \'{}\''.format(file))
	from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
	tmp = 'video_' + str(video_counter) + '.mp4'
	file_name = os.path.join(SAVE_DIR, tmp)
	ffmpeg_extract_subclip(file, int(begin), int(end), targetname=file_name)
	video_counter += 1
	del ffmpeg_extract_subclip
	return video_counter


def download_video(link, dire):
	import glob
	YouTube(link).streams.filter(progressive=True,
	    file_extension='mp4').first().download(dire)
	list_of_files = glob.glob(os.path.join(CURRENT_PATH, 'vids/*'))
	latest_file = max(list_of_files, key=os.path.getctime)
	print('Video download status: add {}'.format(latest_file))
	print(link)
	del glob
	return latest_file


class process_list:
	def __init__(self):
		self.cwd = os.path.dirname(__file__)
		self.media_dir = os.path.join(self.cwd, 'vids/')
		self.parsed_data = []
		self.video_name = []

	def check_path(self):
		if Path(self.media_dir).exists():
			print(">> '{}' directory exists".format(self.media_dir))
		else:
			print('Failed to detect {} directory. Creating one\n'.format(self.media_dir))
			os.mkdir(self.media_dir)

	def parse_file(self):
		"""
		Process file with information metadata about the video

		Return
		------
		processed information
		"""
		import re
		self.check_path()
		with open(os.path.join(self.cwd, 'video_list.txt'), 'r') as file:
			for i in (filter(None, (line.rstrip() for line in file))):
				ls = re.split(',', i.replace(' ', ''))
				self.parsed_data.append(ls)
		counter = 0
		for i in self.parsed_data:
			link = i[0]
			start = convert_to_secs(i[1])
			end = convert_to_secs(i[2])
			file = download_video(link, self.media_dir)
			counter = trim_video(file, start, end, counter)
		del re
		return self.parsed_data

	def video_dir(self):
		"""
		Return directory to where the video's will be stored at
		"""
		return self.media_dir


def process_video_list():
	pl = process_list()
	v_list = pl.parse_file()
	return


if __name__ == '__main__':
	process_video_list()
