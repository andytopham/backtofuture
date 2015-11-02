#!/usr/bin/python
''' Load BBC radio stations for Volumio.'''
import subprocess, time, logging, datetime, requests
from bs4 import BeautifulSoup

PLAYLISTDIR = '/var/lib/mpd/music/WEBRADIO/'
LOGFILE = 'log/bbcradio.log'

class BBC2webradio:
	'''Volumio BBC radio stations setup.'''
	# These are the indicies to the url array.
	URLID = 0
	URLSTREAM = 1
	URLDETAILS = 2
	urls = [
		["BBCR2", "r2_aaclca.pls", "http://www.bbc.co.uk/radio/player/bbc_radio_two" ],
		["BBCR4", "r4_aaclca.pls", "http://www.bbc.co.uk/radio/player/bbc_radio_four" ],
		["BBCR4x", "r4x_aaclca.pls", "http://www.bbc.co.uk/radio/player/bbc_radio_four_extra"],
		["BBCR5", "r5l_aaclca.pls", "http://www.bbc.co.uk/radio/player/bbc_radio_five_live"],
		["BBCR6", "r6_aaclca.pls", "http://www.bbc.co.uk/radio/player/bbc_6music"]
		]
					
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		__all__ = ['stationcount', 'load', 'stationname']	#list functions available

	def stationcount(self):
		'''Return the number of radio station urls.'''
		return(len(self.urls))
		
	def load(self):
		'''Load the pls stations stored in the urls array into the webradio location. '''
		maxstation = self.stationcount()
		self.logger.warning("Getting BBC stations loaded")	
		for i in self.urls:
			self.logger.info("Fetching: "+i[self.URLID])
			try:
				source = ' http://www.bbc.co.uk/radio/listen/live/'+i[self.URLSTREAM]
				destination = PLAYLISTDIR+i[self.URLSTREAM]
				p = subprocess.Popen('wget -O '+destination+source, shell=True)
				p.wait()		# need to wait for the last cmd to finish 
			except HTTPError, e:
				self.logger.error("Failed to fetch address for "+i[self.URLID], exc_info=True)
				maxstation -= 1					# not as many as we planned
			stream = self.process_pls(destination)
			self.create_m3u(i[self.URLID], stream)
		return(maxstation)
	
	def process_pls(self, pls):
		'''Get the actual stream info from the already fetched pls files.'''
		self.logger.info("Opening the stream file: "+pls)
		try:
			source=open(pls,'r')
			source.readline()				# this dumps first line of file
			source.readline()				# dump
			this_line = source.readline()
#			print 'This line: ',this_line
			source.close()					# do we need this??
		except:
			logging.warning("Could not open: "+pls, exc_info=True)
#		return(re.escape((this_line[6:])))
		return(this_line[6:])
		
	def create_m3u(self, id, stream_file):
		'''Create one m3u file for this stream.'''
		m3u_destination = PLAYLISTDIR+id+'.m3u'
		f = open(m3u_destination, 'w')
		f.write('#EXTM3U\n')
		f.write('#EXTINF:-1,'+id+' - streaming\n') # -1 for streams
		f.write(stream_file)
		f.close()
		return(0)
		
	def _stationscanner(self):
		''' A test routine to find out how often the bbc updates the pls files.'''
		self.logger.info("Getting BBC stations loaded")		# refresh periodically
		subprocess.Popen("rm -f *.pls", shell=True)			# need the -f to force removal of unwritable files
		subprocess.Popen('mpc -q clear', shell=True)
		time.sleep(1)
		maxstation = self.stationcount()
		for string in self.bbcstation:
			self.logger.info("Fetching: "+string)
			try:
				p = subprocess.Popen('wget -q http://www.bbc.co.uk/radio/listen/live/'+string, shell=True)	# need to trap errors here.
				p.wait()		# need to wait for the last cmd to finish before we can read the file.
			except HTTPError, e:
				self.logger.error("Failed to fetch address for "+string)
				maxstation -= 1				# not as many as we planned
			else:
				source=open(string,'r')
				source.readline()		# this dumps first line of file
				source.readline()
				line=source.readline()
				source.close()			# do we need this??
				print line[90:]

	def stationname(self, station):
		"""Fetch the name of the currently playing BBC programme."""
		self.logger.info("stationname: Fetching BBC radio program name")
		row = self.urls[station]
		address = row[self.URLDETAILS]
		try:
			soup = BeautifulSoup(requests.get(address).text)
		except requests.ConnectionError:
			self.logger.error("Connection error getting prog info")
			return("Connection error ")
		else:
			try:
				programmename = unicode(soup.title.string)
			except:
				programmename = "Unpronounceable"
			self.logger.info("Program name:"+programmename)
			return(programmename)
				
if __name__ == "__main__":
	print "Running bbcradio class as a standalone app"
	logging.basicConfig(filename = LOGFILE,
						filemode = 'w',
						level = logging.INFO)	#filemode means that we do not append anymore
#	Default level is warning, level=logging.INFO log lots, level=logging.DEBUG log everything
	logging.warning(datetime.datetime.now().strftime('%d %b %H:%M')+". Running bbcradio class as a standalone app")

	myBBC = BBC2webradio()
	myBBC.load()
#	myBBC._stationscanner()