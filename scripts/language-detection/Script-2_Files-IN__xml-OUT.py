import re
import os
import pandas as pd
from lxml import etree
from textblob import TextBlob
from nltk import wordpunct_tokenize


# Schreibe die Sprache anhand der codeliste um 
codes = pd.read_csv('codes.csv')

file = 'd:\...\Desktop\DE_HH_INSPIRE_WFS_SVZ_Zaehlstellenbereiche-8977D62F-F31C-4D64-8312-387BABF8CAAD-zaehlstellenbereiche_svz-2.0.0.gml'

with open(file, 'rb') as f:

	data = f.read()
	root = etree.fromstring(data)
	text_chunks = root.xpath('//text()')
	cleaned_chunks = [s for s in text_chunks if s.strip()]
	# Daten müssen bereinigt werden: füge daher nur character in das Array
	no_numbers = []
	# Entferne alle Zahlen
	for chunk in cleaned_chunks:
		s = re.sub("\d+\.\d+", "", chunk)
		s = re.sub("\d+", "", s)
		no_numbers.append(s.strip())
	cleaned_result = [s for s in no_numbers if s.strip()]
	result_string = ' '.join([i for i in cleaned_result])
	tokens = wordpunct_tokenize(result_string)
	unique_tokens = list(set(tokens)) #füge alle einzigartigen Tokens (Wörter) in eine Liste
	final_tokens = [] #generiere leere Array final_token
	for token in unique_tokens: #führe das für alle einzigartigen Tokens aus
		if token.isalpha() and len(token) >= 3: #wenn in dem token alle character aus alphabetischen Zeichen bestehen + und mindestens 1 Zeichen vorhanden ist, die Länge des Tokens muss mind. 3 sein
			final_tokens.append(token) 
	final_result = ', '.join([i for i in final_tokens]) # Füge die Tokens zusammen
	# Sprachausgabenvariable
	language = ''
	# Check if result_string is not empty try to detect language
	if final_result != '' and len(final_tokens) >=3: #wenn nicht leer und tokens gleich oder mehr als 3 ist
		# Detect language using textblob
		lang_code = TextBlob(final_result).detect_language()
		# Get language name agaist language code
		for i in range(0, len(codes)):
			if codes.loc[i, 'Code'] == lang_code:
				language = codes.loc[i, 'Language']


def write_meta_file():
	# to write extracted attributes to metaFile.xml
	filename = os.path.splitext(file)[0]
	root_xml = etree.parse('TemplateMetaData.xml')

	for lang in root_xml.find('{http://www.isotc211.org/2005/gmd}language'):
		lang.attrib['codeListValue'] = language
		root_xml.write(filename+'.xml', encoding='UTF-8')

if __name__=='__main__':
		print ('Sprache: ' + language)
		write_meta_file()