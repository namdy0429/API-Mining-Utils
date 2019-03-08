import os, math
from argparse import ArgumentParser
import requests

class ClientCodeCrawler:
	def __init__(self, token):
		self.token = token
		self.headers = {
			    'Accept': 'application/vnd.github.mercy-preview+json',
			    'Authorization': 'token ' + self.token
			}
		self.raw_headers = {
				'Accept': 'application/vnd.github.v3.raw',
    			'Authorization': 'token ' + self.token
		}

	def retrieveRepositories(self, num_repos=100, per_page=100):
		num_pages = int(math.ceil(float(num_repos)/per_page))
		repos = []
		for p in range(num_pages):
			params = (
			    ('q', 'topic:java language:java'),
			    ('sort', 'stars'),
			    ('order', 'desc'),
			    ('per_page', str(per_page)),
			    ('page', str(p))
			)

			response = requests.get('https://api.github.com/search/repositories', headers=self.headers, params=params)
			try:
				repos.extend([response.json()['items'][i]['full_name'] for i in range(num_repos)])
				print('Page {:d}: {:d} repositories retrieved.'.format(p, len(repos)))
			except:
				print('Page {:d}: Error {:d}.'.format(p, response.status_code))
		return repos

	def downloadFiles(self, api_name, repo, out_dir, is_overwrite, per_page=100):
		error_count = 0
		params = (
		    ('q', 'import ' + api_name + ' in:file extension:java repo:'+repo),
		    ('per_page', per_page),
		)

		try:
			code_list = requests.get('https://api.github.com/search/code', headers=self.headers, params=params)	
			print("---------------------------------------------------------------------")
			print("# of codes in {0}: {1}".format(repo, code_list.json()['total_count']))
			print("# of codes in {0}'s {1}th batch: {2}".format(repo, 1, len(code_list.json()['items'])))

			for i in range(code_list.json()['total_count']):
				if i != 0 and i % per_page == 0:
					params = (
					    ('q', 'import ' + api_import + ' in:file extension:java repo:'+repo),
					    ('per_page', str(per_page)),
					    ('page', str(i/per_page+1))
					)			
					code_list = requests.get('https://api.github.com/search/code', headers=self.headers, params=params)			
					print("# of codes in {0}'s {1}th batch: {2}".format(repo, i/per_page+1, len(code_list.json()['items'])))
				file_name = out_dir+'/'+code_list.json()['items'][i%per_page]['repository']['full_name'].replace('/','.')+'.'+code_list.json()['items'][i%per_page]['name']
				if is_overwrite:
					code = requests.get('https://api.github.com/repos/'+repo+"/contents/"+code_list.json()['items'][i%per_page]['path'], headers=self.raw_headers, allow_redirects=True)
					open(file_name, 'wb').write(code.content)
					print("Downloaded " + file_name)
				else:
					if not os.path.isfile(file_name):
						code = requests.get('https://api.github.com/repos/'+repo+"/contents/"+code_list.json()['items'][i%per_page]['path'], headers=self.raw_headers, allow_redirects=True)
						open(file_name, 'wb').write(code.content)
						print("Downloaded " + file_name)
			print("---------------------------------------------------------------------")
		except:
			print("---------------------------------------------------------------------")
			print('Error in {:s}.'.format(repo))
			print(code_list)
			print("---------------------------------------------------------------------")
			raise



if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument("-a", "--api", dest="api_name", help="Target API Name (e.g., javax.xml)")
	parser.add_argument("-o", "--out_dir", dest="out_dir", help="Output Directory to Store the Client Code Files")
	parser.add_argument("-t", "--token", dest="token", help="Github Access Token for Github API (https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line for more information)")
	parser.add_argument("-ow", "--overwrite", dest="is_overwrite", help="Set True to Overwrite Existing File", action='store_true', default=False)

	args = parser.parse_args()

	crawler = ClientCodeCrawler(args.token)
	repositories = crawler.retrieveRepositories()
	for repo in repositories:
		crawler.downloadFiles(args.api_name, repo, args.out_dir, args.is_overwrite)
	

