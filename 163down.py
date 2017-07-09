#!/usr/bin/env python3
#coding: utf-8
#网易公开课视频多线程批量下载

from ThreadPool import *
from dl_multithreading import download as m_download
import urllib.request as urllib
import re
import os
import sys

_re = re.compile(r'&nbsp;&nbsp;&nbsp;&nbsp;(\S+)\s*<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\s*<a href="(\S+)" target')
_re_name = re.compile(r'系列名称：(\S+)</p>.+下载地址')

def parse_videos(url):
	data = b'url=' + urllib.quote(url).encode('ascii')
	html = urllib.urlopen('http://yipeiwu.com/getvideo.html', data=data).read().decode('utf-8')
	name = _re_name.findall(html)
	if name:
		name = name[0]
	else:
		return False
	result = _re.findall(html)
	return name,result

def fn_format(v):
	ext = os.path.splitext(v[1])[1]
	fn = v[0]
	fn = fn.split(':')
	return '%s %s' % (fn[0], fn[1].split('．')[-1] + ext)

def count(videos):
	return sum(map(lambda x:not bool(x),videos))

def download(videos, i, dn, length):
	v = videos[i]
	fn = fn_format(v)
	path = os.path.join('.', dn, fn)
	d = m_download(v[1], path)
	last_info = ''
	for status in d:
		if type(status) == tuple:
			s = '%s %s/%s:' % status
			info = '%s %s' % (s, v[0])
		elif status == 'Merging...':
			info = '%s -> Merging to... -> %s' % (v[0], fn)
		if info != last_info:
			print(info)
			last_info = info
	videos[i] = None
	num = count(videos)
	print('%s/%s %s -> %s' % (num, length, v[0], path))

def main():
	if len(sys.argv) == 1:
		url = input('URL> ')
	else:
		url = sys.argv[1]
	name, videos = parse_videos(url)
	length = len(videos)
	if not os.path.isdir(name): os.makedirs(name)
	for i in range(length):
		download(videos, i, name, length)

if __name__ == '__main__':
	main()