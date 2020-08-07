# Agasha Ratam
# Version Aug 7, 2020

from bs4 import BeautifulSoup

def edit_html(html_s):	
	soup = BeautifulSoup(html_s, 'html.parser')

	# Delete navigation bar
	nav = soup.body.find('div', attrs={'role': 'navigation'})
	if nav:
		nav.extract()

	# Delete R source code
	r_code = soup.body.find(attrs={'id': 'flexdashboard-source-code'})
	if r_code:
		r_code.extract()

	# Add our own navigation bar by adding lines to the start of <body>
	template_f = open('dashboard_template.html', 'r')
	template_soup = BeautifulSoup(template_f.read(), 'html.parser')

	if soup.body.contents == []:
		soup.body.contents.extend(template_soup.body.contents)
	else:
		first = soup.body.contents[0]
		while template_soup.body.contents != []:
			first.insert_before(template_soup.body.contents[0])

	# Add stylesheet by adding lines to the end of <body>
	style = soup.new_tag('link', rel='stylesheet', href='style.css')
	soup.body.append(style)

	return nice_prettify(soup)

def nice_prettify(bs_tag):
	s = bs_tag.prettify()

	new = []
	for line in s.split('\n'):
		count = 0
		while len(line) > 0 and line[0] == ' ':
			count += 1
			line = line[1:]
		for i in range(count):
			line = '\t' + line
		new.append(line)
	
	return '\n'.join(new)

