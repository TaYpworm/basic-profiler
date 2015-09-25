#!/usr/bin/python

import numpy as np

class Profile(object):
	def __init__(self):
		self.cmd = None
		self.pid = None
		self.cpu_time = None
		self.elapsed_time = None
		# memory stats stored in MiB
		self.process_data = {
			'pcpu': [],
			'size': [],
			'rss': [],
			'vsz': []
		}

	def __repr__(self):
		return str(self.calc_statistics())

	'''
	Add a sample to the data structure.
	sample = whitespace delimited sample of format "pid pcpu cputime etime size rss vsz cmd"
	'''
	def process_sample(self, sample):
		# split sample on whitespace
		# command may contain whitespace, so limit splits to 7
		data = sample.strip().split(None, 7)
		if len(data) != 8:
			raise ValueError('Sample should have length 8')

		# pid = process id, int
		if not self.pid:
			self.pid = int(data[0])
		# pcpu = percent cpu, float
		self.process_data['pcpu'].append(float(data[1]))
		# cputime = time on cpu, cumulative, string
		self.cpu_time = data[2]
		# etime = total clock time, cumulative, string
		self.elapsed_time = data[3]
		# size = rough size if resident application written to swap, int
		self.process_data['size'].append(int(data[4]))
		# rss = resident set size, non-swapped physical memory task has used in KiB, float
		# stored in MiB
		self.process_data['rss'].append(self._kb_to_mb(float(data[5])))
		# vsz = virtual memory size in KiB, float
		# stored in MiB
		self.process_data['vsz'].append(self._kb_to_mb(float(data[6])))
		# cmd = command, string
		if not self.cmd:
			self.cmd = data[7]

	'''
	Convert from kilobytes to megabytes
	kb = kilobytes
	'''
	def _kb_to_mb(self, kb):
		return kb / 1024.0

	'''
	Calculate statistics and return as a dictionary.
	'''
	def calc_statistics(self):
		stats = {
			'cmd': self.cmd,
			'pid': self.pid,
			'cpu_time': self.cpu_time,
			'elapsed_time': self.elapsed_time
		}

		stats['percent_cpu'] = self._calc_stats(self.process_data['pcpu'])
		stats['resident_set_size'] = self._calc_stats(self.process_data['rss'])
		stats['virtual_memory_size'] = self._calc_stats(self.process_data['vsz'])

		return stats

	def _calc_stats(self, data):
		return {
			'average': np.mean(data),
			'median': np.median(data),
			'max': np.max(data),
			'min': np.min(data),
			'std_dev': np.std(data)	
		}