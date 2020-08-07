# Reads all files from the folder SOURCE_DIR, then edits all HTML files into 
# publishable format, with our own navigation bar. The edited versions of the
# HTML files are written into the folder DEST_DIR. The remaining files in SOURCE_DIR,
# which may include CSS and data files are copied into DEST_DIR.

# Agasha Ratam
# Version Aug 7, 2020

import os
from bs4 import BeautifulSoup
import combiner_utils

SOURCE_DIR = 'source/'
FNAMES = ['ngrams.html']

DEST_DIR = 'dashboard/'
NEW_FNAMES = ['ngrams.html', 'index.html', 'wordcloud.html', 'lollipop.html']

def main():
	# Create list of HTML strings
	html_strings = []
	for fname in FNAMES:
		f = open(SOURCE_DIR + fname, 'r')
		html_strings.append(f.read())
		f.close()

	# Break down dashboard.html into three HTMLs
	# TODO: Change code when each vis is in a separate HTML file
	f = open('source/dashboard.html', 'r')
	s = f.read()
	f.close()

	ids = ['classifed-tweets-display', 'wordcloud', 'lollipop'] 
	for id_attr in ids:
		soup = BeautifulSoup(s, 'html.parser')
		dashboard_container = soup.body.find(attrs={'id': 'dashboard-container'})

		div = soup.body.find(attrs={'id': id_attr})	
		dashboard_container.replace_with(div)

		html_strings.append(combiner_utils.nice_prettify(soup))

	# Edit all HTML strings and write to the folder DEST_DIR
	for i in range(len(html_strings)):
		s = html_strings[i]
		edited = combiner_utils.edit_html(s)

		new_f = open(DEST_DIR + NEW_FNAMES[i], 'w')
		new_f.write(edited)
		new_f.close()

	# Copy non-HTML files from SOURCE_DIR to DEST_DIR
	for fname in os.listdir(SOURCE_DIR):
		if fname.endswith('.css') or fname.endswith('.json') or fname.endswith('.csv'):
			old_f = open(SOURCE_DIR + fname, 'r')

			new_f = open(DEST_DIR + fname, 'w')
			new_f.write(old_f.read())

			old_f.close()
			new_f.close()

	# Copy style.css
	f = open('style.css', 'r')
	new_f = open(DEST_DIR + 'style.css', 'w')
	new_f.write(f.read())

	f.close()
	new_f.close()
	
if __name__ == '__main__':
	main()
