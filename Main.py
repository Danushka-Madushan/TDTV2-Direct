import re
import requests
from msvcrt import getch
from os import system as execute

def Main():
	
	def finder(metadata, lst):
		_search_url = ("http://www.todaytvseries2.com/search-series?searchword={}&searchphrase=all&limit=0".format(metadata))
		_search_data = requests.get(_search_url).content.decode('utf-8')

		_tn_ = re.findall(r'<a href="/tv-series/(\S+)" title="([\D]*|[\S]*)">', _search_data)
		for _tn_element in _tn_:
			lst.append(_tn_element)

	_titledata = []

	while True:
		_user_search_ = input("\n Enter TV-Show Name : ")
		if 3 <= len(_user_search_) <= 200:
			finder(_user_search_, _titledata)
			_index_ = 1
			
			if not len(_titledata) == 0:
				print(" --------------------------------------------------------------------------------------------------")
				for x in range(len(_titledata)):
					print(f' : {str(_index_).zfill(2)} : {_titledata[x][1]} : http://www.todaytvseries2.com/tv-series/{_titledata[x][0]}')
					_index_ += 1
					print(" --------------------------------------------------------------------------------------------------")

				choice = int(input("\n Enter Series Number : "))

				if 0<choice<=len(_titledata):
					req = requests.get(f"http://www.todaytvseries2.com/tv-series/{_titledata[choice-1][0]}").content.decode("utf-8")

					title = re.search(r'<h1[ ]class="uk-article-title[ ]uk-badge1">(\D+|\S+)</h1>', req).group(1)
					sizenfo = re.findall(r'<div class="row1 footer"><div class="cell1">(\D+)</div><div class="cell1">([A-z]+)</div><div class="cell1">(.+p)</div><div class="cell1">(.+)</div><div class="cell1"><span class="imdbRatingPlugin"', req)
					seasons = re.findall(r'</span>[A-z]{8}[ ][A-z]{6}[ ]([0-9]{1,2})</h3>', req)
					seasons.sort()
					execute("cls")
					
					print(f" Tv-Series :{title}({sizenfo[0][0]}) {sizenfo[0][1]} {sizenfo[0][2]} {sizenfo[0][3]}\n")
					for x in seasons:
						print(f"{title}Season {x}")

					season = input("\n Enter Season : ")
					if season in seasons:
						epregex = (r'<div[ ]class="cell2">(S'+season.zfill(2)+'E[0-9]{2})</div><div[ ]class="cell3">([0-9]{2,3}[ ][A-z]{2})</div><div[ ]class="cell4"><a[ ]href="(\S+)"')
						links = re.findall(epregex ,req)
						links.sort()
						print(f"\n {len(links)} Episodes are Avilable in Season {season}")
						linkfile = open(f"Season {season}.txt", "w")
						for a in links:
							linkfile.write(a[0] + "  " + a[1] + " : " + a[2] + "\n")
						linkfile.close()
						print(f" All Links are Saved to [Season {season}.txt] !")
						getch()
						
					else:
						print(" Invalid Season!")
				break

			else:
				print("\n 0 TV-Series Found! :( Try Using Different Keywords!")
				getch()
				execute("cls")
				continue

		else:
			print("\n Search Term Must be a Minimum of 3 Characters and a Maximum of 200 Characters! ")
			getch()
			execute("cls")
			continue

if __name__ == "__main__":
	Main()
