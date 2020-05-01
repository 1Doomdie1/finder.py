import sys, os 
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

def usage():
	print('[!] usage: python3 finder.py <service> <name>\n'\
	'[+] services: twiter, instagram, youtube')
	sys.exit()
	return

def twiter_scraper(name):
	try:
		my_url = "https://twitter.com/" + name
		uPage = uReq(my_url)
		read_page = uPage.read()
		uPage.close()
		page_soup = soup(read_page, "html.parser")

		getting_date_of_joining = page_soup.find("span", {"class":"ProfileHeaderCard-joinDateText js-tooltip u-dir"})
		getting_tweets_count = page_soup.find("li", {"class":"ProfileNav-item ProfileNav-item--tweets is-active"})
		getting_followings_count = page_soup.find("li", {"class":"ProfileNav-item ProfileNav-item--following"})
		getting_followers_count = page_soup.find("li", {"class":"ProfileNav-item ProfileNav-item--followers"})
		getting_location = page_soup.find("span", {"class":"ProfileHeaderCard-locationText u-dir"})
		getting_profile_header = page_soup.find("p", {"class":"ProfileHeaderCard-bio u-dir"})

		date_of_joining = getting_date_of_joining.text.replace('Joined ', '')
		tweets_cont = getting_tweets_count.a['title'].replace('Tweets', '').replace("Tweet", '')
		following_count = getting_followings_count.a['title'].replace('Following', '')
		followers_count = getting_followers_count.a['title'].replace('Followers', '')
		location = getting_location.text.replace('\n', '').replace('              ', '').replace('        ', '.').replace("\n", '')
		profile_header = getting_profile_header.text

		print("-> He/She is followed by " + followers_count + "people.")
		print("-> He/She is following "+ following_count + "people.")
		print("-> He/She has " + tweets_cont +"tweets.")
		print("-> He/She joined twitter on " + date_of_joining +".")

		try:
			getting_bday = page_soup.find("span", {"title":"Public"})
			getting_linked_sites = page_soup.find("span", {"class":"ProfileHeaderCard-urlText u-dir"})
			
			bday = getting_bday.text.replace("    Born ", '').replace('\n', '')
			linked_sites = getting_linked_sites.a['title']
			
			print("-> He/She is born in "+ bday +".")
			print("-> Linked site: "+ linked_sites)
		except Exception:
			pass			

		if len(location) == 0:
			pass
		else:
			print("-> He/She leaves in "+ location)

		if len(profile_header) == 0:
			pass
		else:
			print("-> Profile header: " + profile_header)

	except Exception:
		print("This user doesn't exist.")


def instagram_scraper(name):
	pass

def youtube_scraper(name):
	try:
		my_url = "https://youtube.com/results?search_query=" + name
		uPage = uReq(my_url)
		read_page = uPage.read()
		uPage.close()
		page_soup = soup(read_page, "html.parser")

		getting_total_channels = page_soup.findAll("div", {"class":"yt-lockup yt-lockup-tile yt-lockup-channel vve-check clearfix yt-uix-tile"})
		channels_num = len(getting_total_channels)

		channels = []

		if channels_num == 0:
			print('[-]No channels found with that name!')

		elif channels_num == 1:
			print("[+]I have found " + str(channels_num) + " channel:")
			print(" [+]https://youtube.com" + getting_total_channels[0].div.a['href'])
			ch = getting_total_channels[0].div.a['href']
			channels.append(ch)

			while True:
				target_url = "https://youtube.com" + channels[0] +"/about"
				target_uPage = uReq(target_url)
				target_read_page = target_uPage.read()
				target_uPage.close()
				target_page_soup = soup(target_read_page, "html.parser")

				getting_subs = target_page_soup.find("span", {"class":"yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip"})
				getting_total_views = target_page_soup.findAll("span", {"class":"about-stat"})
				getting_joining_date = target_page_soup.findAll("span", {"class":"about-stat"})
				
				subs = getting_subs.text.replace('.', '')
				views = getting_total_views[0].text.replace(" • ", "")
				join_date = getting_joining_date[1].text

				if len(target_page_soup.title) == 0:
					print("[-]The channel doesn't have an 'About' section")
				else:
					print(' [#]' + subs + ' subs.')
					print(' [#]'+ views)
					print(' [#]' + join_date)
					try:
						get_loc = target_page_soup.find("span", {"class":"country-inline"})
						get_links = target_page_soup.find("ul", {"class":"about-secondary-links"})
						
						links = get_links.findAll("li", {"class":"channel-links-item"})
						loc = get_loc.text.replace('\n', '').replace(' ' * 8, '')
						print(' [+]Location: ' + loc)
						
						print(' [+]Usefull links:')
						for i in links:
							link = i.a["href"]
							if link.startswith('/redirect?q='):
								a = link.replace('%3A', ':').replace('%2F','/')
								print('    [#]' + a[12:-95])
							elif link.startswith('/redirect?q=') and link.endswith('&event=channel_description'):
								a = link.replace('%3A', ':').replace('%2F','/')
								print('    [#]' + a[12:-95])
							elif link.startswith('/redirect?q=') and link.endswith('&event=channel_banner'):
								a = link.replace('%3A', ':').replace('%2F','/')
								print('    [#]' + a[12:-90])
							elif link.startswith('/redirect?event=channel_description&redir_token='):
								a = link.replace('%3A', ':').replace('%2F','/')
								print('    [#]' + a[107:])
							elif link.startswith('/redirect?redir_token='):
								a = link.replace('%3A', ':').replace('%2F','/')
								print('    [#]' + a[107:])
							elif link.startswith('/redirect?redir_token=') and link.endswith('&event=channel_banner'):
								a = link.replace('%3A', ':').replace('%2F','/')
								print('    [#]' + a[81:-21])
							elif link.startswith('/redirect?redir_token=') and link.endswith('&event=channel_description'):
								a = link.replace('%3A', ':').replace('%2F','/')
								print('    [#]' + a[81:-26])
							elif link.startswith('/redirect?event=channel_banner&redir_token='):
								a = link.replace('%3A', ':').replace('%2F','/')
								print('    [#]' + a[102:])
							else:
								a = link.replace('%3A', ':').replace('%2F','/')
								print('    [#]' + a[32:-69])
					except Exception:
						print("[-]Site doesn't have any linked sites")
				break

		else:
			print("[!]I have found " + str(channels_num) + " channels:")
			for i in range(channels_num):
				print(" ["+ str(i + 1) +"] https://youtube.com" + getting_total_channels[i].div.a['href'])
				ch = getting_total_channels[i].div.a['href']
				channels.append(ch)

			print('[?]Select the channel number that u want to extract data from or type all')
			while True:
				chose_a_channel = input('>>>')
				try:
					if int(chose_a_channel) <= len(channels):
						target_url = "https://youtube.com" + channels[int(chose_a_channel) - 1] +"/about"
						target_uPage = uReq(target_url)
						target_read_page = target_uPage.read()
						target_uPage.close()
						target_page_soup = soup(target_read_page, "html.parser")
						
						getting_subs = target_page_soup.find("span", {"class":"yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip"})
						getting_total_views = target_page_soup.findAll("span", {"class":"about-stat"})
						getting_joining_date = target_page_soup.findAll("span", {"class":"about-stat"})
						
						subs = getting_subs.text.replace('.', '')
						views = getting_total_views[0].text.replace(" • ", "")
						join_date = getting_joining_date[1].text


						if len(target_page_soup.title) == 0:
							print("[!]The channel doesn't have an 'About' section")
						else:
							print(' [#]' + subs + ' subs.')
							print(' [#]'+ views)
							print(' [#]' + join_date)

							try:
								get_loc = target_page_soup.find("span", {"class":"country-inline"})
								get_links = target_page_soup.find("div", {"class":"about-metadata branded-page-box-padding clearfix"})
								
								links = get_links.findAll("li", {"class":"channel-links-item"})
								loc = get_loc.text.replace('\n', '').replace(' ' * 8, '')
								print(' [+]Location: ' + loc)
								
								print(' [+]Usefull links:')
								for i in links:
									link = i.a["href"]
									if link.startswith('/redirect?q='):
										a = link.replace('%3A', ':').replace('%2F','/')
										print('    [#]' + a[12:-95])
									elif link.startswith('/redirect?q=') and link.endswith('&event=channel_description'):
										a = link.replace('%3A', ':').replace('%2F','/')
										print('    [#]' + a[12:-95])
									elif link.startswith('/redirect?q=') and link.endswith('&event=channel_banner'):
										a = link.replace('%3A', ':').replace('%2F','/')
										print('    [#]' + a[12:-90])
									elif link.startswith('/redirect?event=channel_description&redir_token='):
										a = link.replace('%3A', ':').replace('%2F','/')
										print('    [#]' + a[107:])
									elif link.startswith('/redirect?redir_token='):
										a = link.replace('%3A', ':').replace('%2F','/')
										print('    [#]' + a[107:])
									elif link.startswith('/redirect?redir_token=') and link.endswith('&event=channel_banner'):
										a = link.replace('%3A', ':').replace('%2F','/')
										print('    [#]' + a[81:-21])
									elif link.startswith('/redirect?redir_token=') and link.endswith('&event=channel_description'):
										a = link.replace('%3A', ':').replace('%2F','/')
										print('    [#]' + a[81:-26])
									elif link.startswith('/redirect?event=channel_banner&redir_token='):
										a = link.replace('%3A', ':').replace('%2F','/')
										print('    [#]' + a[102:])
									else:
										a = link.replace('%3A', ':').replace('%2F','/')
										print('    [#]' + a[32:-69])
							except Exception:
								print("[-]Site doesn't have any linked sites")
					break
				except Exception:
					if chose_a_channel == 'all':
						for i in channels:
							target_url = "https://youtube.com" + i +"/about"
							target_uPage = uReq(target_url)
							target_read_page = target_uPage.read()
							target_uPage.close()
							target_page_soup = soup(target_read_page, "html.parser")

							getting_subs = target_page_soup.find("span", {"class":"yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip"})
							getting_total_views = target_page_soup.findAll("span", {"class":"about-stat"})
							getting_joining_date = target_page_soup.findAll("span", {"class":"about-stat"})
							
							subs = getting_subs.text.replace('.', '')
							views = getting_total_views[0].text.replace(" • ", "")
							join_date = getting_joining_date[1].text

							if len(target_page_soup.title) == 0:
								print("[!]The channel doesn't have an 'About' section")
							else:
								print('[+]Info form channel: ' + target_page_soup.title.text.replace('  ', '').replace('\n', '').replace(' - YouTube', ''))
								print(' [#]' + subs + ' subs.')
								print(' [#]'+ views)
								print(' [#]' + join_date)

								try:
									get_loc = target_page_soup.find("span", {"class":"country-inline"})
									get_links = target_page_soup.find("div", {"class":"about-metadata branded-page-box-padding clearfix"})
									
									links = get_links.findAll("li", {"class":"channel-links-item"})
									loc = get_loc.text.replace('\n', '').replace(' ' * 8, '')
									print(' [+]Location: ' + loc)
									
									print(' [+]Usefull links:')
									for i in links:
										link = i.a["href"]
										if link.startswith('/redirect?q='):
											a = link.replace('%3A', ':').replace('%2F','/')
											print('    [#]' + a[12:-95])
										elif link.startswith('/redirect?q=') and link.endswith('&event=channel_description'):
											a = link.replace('%3A', ':').replace('%2F','/')
											print('    [#]' + a[12:-95])
										elif link.startswith('/redirect?q=') and link.endswith('&event=channel_banner'):
											a = link.replace('%3A', ':').replace('%2F','/')
											print('    [#]' + a[12:-90])
										elif link.startswith('/redirect?event=channel_description&redir_token='):
											a = link.replace('%3A', ':').replace('%2F','/')
											print('    [#]' + a[107:])
										elif link.startswith('/redirect?redir_token='):
											a = link.replace('%3A', ':').replace('%2F','/')
											print('    [#]' + a[107:])
										elif link.startswith('/redirect?redir_token=') and link.endswith('&event=channel_banner'):
											a = link.replace('%3A', ':').replace('%2F','/')
											print('    [#]' + a[81:-21])
										elif link.startswith('/redirect?redir_token=') and link.endswith('&event=channel_description'):
											a = link.replace('%3A', ':').replace('%2F','/')
											print('    [#]' + a[81:-26])
										elif link.startswith('/redirect?event=channel_banner&redir_token='):
											a = link.replace('%3A', ':').replace('%2F','/')
											print('    [#]' + a[102:])
										else:
											a = link.replace('%3A', ':').replace('%2F','/')
											print('           | ' + a[32:-69])
								except Exception:
									print("[-]Site doesn't have any linked sites")
							print('\n')
						break
					else:
						print('')
	except Exception:
		print("This user doesn't exist!")

def main():
	if len(sys.argv) != 3:
		usage()
	s = sys.argv
	service, name= s[1],s[2]
	if service == 'facebook' or service == 'fb':
		facebook_scraper(name)
	elif service == 'twitter' or service == 'tw':
		twiter_scraper(name)
	elif service == 'instagram' or service == 'insta':
		instagram_scarper(name)
	elif service == 'youtube' or service == 'yt':
		youtube_scraper(name)
	else:
		print(f'[-] ERROR: unknown service: {service}')
		os._exit(1)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print('\n[!] WARNING: interrupted by user\n')
		os._exit(1)