from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

def get_page(url, name):
	my_url = url + str(name)
	uPage = uReq(my_url)
	read_page = uPage.read()
	uPage.close()
	page_soup = soup(read_page, "html.parser")
	return page_soup

def get_individual_pages_data(url):
	target_uPage = uReq(url)
	target_read_page = target_uPage.read()
	target_uPage.close()
	target_page_soup = soup(target_read_page, "html.parser")
	return target_page_soup

def beautify_yt_link(link_to_beautifi):
	for i in link_to_beautifi:
		link = i.a["href"].split('&')
		if link[0].startswith('/redirect?q='):
			print('    [+]' + link[0].replace('/redirect?q=','').replace('%3A',':').replace('%2F','/'))
		elif link[0].startswith('/redirect?redir_token=') and link[2].startswith('q='):
			print('    [+]' + link[2].replace('q=', '').replace('%3A',':').replace('%2F','/'))
		elif link[0].startswith('/redirect?event=') and link[2].startswith('redir_token='):
			print('    [+]' + link[1].replace('q=', '').replace('%3A',':').replace('%2F','/'))
		elif link[0].startswith('/redirect?redir_token=') and link[2].startswith('event='):
			print('    [+]' + link[1].replace('q=', '').replace('%3A',':').replace('%2F','/'))
		elif link[0].startswith('/redirect?event=') and link[2].startswith('q='):
			print('    [+]' + link[2].replace('q=', '').replace('%3A',':').replace('%2F','/'))
		else:
			pass

def get_twitter_user_info(page_soup, name):
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
	
	print("[!]Fetching data for " + name)
	print("  [+]Followed by " + followers_count + "people.")
	print("  [+]Following "+ following_count + "people.")
	print("  [+]" + tweets_cont +"tweets.")
	print("  [+]Joined twitter on " + date_of_joining +".")
	
	if len(location) != 0:
		print("  [+]Leaves in "+ location)
		
	if len(profile_header) != 0:
		print("  [+]Profile header: " + profile_header)

def get_youtube_user_info(target_page_soup):
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
			beautify_yt_link(links)
		except Exception:
			print("[-]Site doesn't have any linked sites")