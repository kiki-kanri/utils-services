import subprocess

from kikiutils.check import isfile
from kikiutils.string import random_str

from main.settings import ROOT


class ConvertVideoConfig:
	def __init__(self, target_ext: str):
		self.tmp_dir_path = str(ROOT / f'files/tmp/convert/{random_str(64, 64)}')

		self.converted_video_path = f'{self.tmp_dir_path}/converted_video.{target_ext}'
		self.target_ext = target_ext
		self.video_path = f'{self.tmp_dir_path}/video'


def convert_video(config: ConvertVideoConfig):
	try:
		subprocess.run([
			'ffmpeg',
			'-i',
			config.video_path,
			'-c:v',
			'libx264',
			'-c:a',
			'aac',
			config.converted_video_path
		])

		return isfile(config.converted_video_path)
	except:
		pass
