import os, requests, argparse, scripts
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def youtube_scraper(name):
	try:
		page_soup = scripts.get_page("https://youtube.com/results?search_query=", name)
		getting_total_channels = page_soup.findAll("div", {"class":"yt-lockup yt-lockup-tile yt-lockup-channel vve-check clearfix yt-uix-tile"})
		channels = []

		if len(getting_total_channels) == 0:
			print('[-]No channels found with that name!')

		elif len(getting_total_channels) == 1:
			
			print("[+]I have found ",len(getting_total_channels)," channel:")
			print(" [+]https://youtube.com" + getting_total_channels[0].div.a['href'])

			target_url = "https://youtube.com" + getting_total_channels[0].div.a['href'] +"/about"
			target_page_soup = scripts.get_individual_pages_data(target_url)
			scripts.get_youtube_user_info(target_page_soup)
		
		else:
			print("[!]I have found ",len(getting_total_channels)," channels:")
			for i in range(len(getting_total_channels)):
				print(" ["+ str(i + 1) +"] https://youtube.com" + getting_total_channels[i].div.a['href'])
				channels.append(getting_total_channels[i].div.a['href'])

			print('[?]Select the channel number that u want to extract data from or type all')
			while True:
				chose_a_channel = input('>>>')
				try:
					if int(chose_a_channel) <= len(channels):
						target_url = "https://youtube.com" + channels[int(chose_a_channel) - 1] +"/about"
						target_page_soup = scripts.get_individual_pages_data(target_url)
						scripts.get_youtube_user_info(target_page_soup)
					else:
						print('[!]Number out of range')
					break
				except Exception:
					if chose_a_channel == 'all':
						for i in channels:
							target_url = "https://youtube.com" + i +"/about"
							target_page_soup = scripts.get_individual_pages_data(target_url)
							scripts.get_youtube_user_info(target_page_soup)
							print('\n')
						break
	except Exception:
		print("[-]This user doesn't exist!")

def twitter_scraper(name):
	try:
		page_soup = scripts.get_page("https://twitter.com/", name)
		scripts.get_twitter_user_info(page_soup, name)

		try:
			getting_bday = page_soup.find("span", {"title":"Public"})
			getting_linked_sites = page_soup.find("span", {"class":"ProfileHeaderCard-urlText u-dir"})
			
			bday = getting_bday.text.replace("    Born ", '').replace('\n', '')
			linked_sites = getting_linked_sites.a['title']
			
			print("  [+]Born in "+ bday +".")
			print("  [+]Linked site: "+ linked_sites)
		except Exception:
			pass			
	except Exception:
		print("[-]This user doesn't exist.")

def instagram_scraper(name):
	try:
		page_soup = scripts.get_page("https://instagram.com/", name)
		get_info = page_soup.find("script", {"type":"application/ld+json"})
		processed_data = str(get_info).split(',')
		for i in processed_data:
			edited = i.replace('\n', '').replace(' ', '').replace('\/', '/').replace('@','').replace('"', '').replace('</script>', '').replace('<scripttype=application/ld+json>', '').replace('{','').replace('}','')
			print('[+]' + edited)
	except Exception:
		print('[!]No user with that name was found!')

def github_scraper(name):
	try:
		r = requests.get('https://api.github.com/users/' + name, auth=('test804', 'pl,098OKM'))
		print('[!]Fetching data for ' + name)
		for i in r.text.split(','):
			print('  [+]'+ i.replace('"', '').replace('{', '').replace('}', ''))
		print('[!]Done!')
	except Exception:
		print('[-]No user found with that name!')

def main():
	parser = argparse.ArgumentParser(prog = 'python3 finder.py')
	parser.add_argument('-s', '--service', type = str, metavar = '', required = True, help = 'Servces: youtube, instagram, github, twitter or yt, insta, gh, tw')
	parser.add_argument('-u', '--username', type = str, metavar = '', required = True, help = 'Username. For yt, insta, twitter if the user have 2 names the space between should be replaced with "_" ')
	args = parser.parse_args()

	if args.service == 'github' or args.service == 'gh':
		github_scraper(args.username)
	elif args.service == 'youtube' or args.service == 'yt':
		youtube_scraper(args.username)
	elif args.service == 'twitter' or args.service == 'tw':
		twitter_scraper(args.username)
	elif args.service == 'instagram' or args.service == 'insta':
		instagram_scraper(args.username)
	else:
		print('[!]Unknscripts service!')
		parser.print_help()
		sys.exit(1)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\n[!] WARNING: interrupted by user\n')
		sys.exit(1)