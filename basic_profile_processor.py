#!/usr/bin/python

from datetime import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
from profile import Profile
import sys

def main(args):
	# time formatting
	format = '%Y%m%d%H%M%S'
	# assume args contains a list of basic_profile outputs files
	for file_name in args:
		profile = read_profile(file_name)
		time = datetime.today().strftime(format)
		out_prefix = str(profile.pid) + '_'
		write_profile(out_prefix + 'stats_' + time + '.json', profile)
		write_plot(out_prefix + 'plot_' + time + '.png', profile)

'''
Read the profile from file into a Profile object.
'''
def read_profile(file_name):
	f = open(file_name, 'r')
	profile = Profile()
	for line in f:
		profile.process_sample(line)

	return profile

'''	
Create a plot with two subplots.
The top plot will plot percent cpu usage over time.
The bottom plot will plot resident memory over time. 
'''
def write_plot(file_name, profile):
	
	plt.figure(1)
	x = np.arange(0, len(profile.process_data['pcpu']))

	plt.subplot(211)
	plt.ylabel('Percent CPU (%)')
	plt.plot(x, profile.process_data['pcpu'], color='r')

	plt.subplot(212)
	plt.ylabel('Resident Memory (MiB)')
	plt.xlabel('Time (min)')
	plt.plot(x, profile.process_data['rss'], color='r')

	plt.savefig(file_name)

'''
Write the profile statistics to a json file.
'''
def write_profile(file_name, profile):
	f = open(file_name, 'w')
	json.dump(profile.calc_statistics(), f, sort_keys=True, indent=2)

if __name__ == '__main__':
	main(sys.argv[1:])