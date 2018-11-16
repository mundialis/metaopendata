import re
import csv
import glob
import pandas as pd
from lxml import etree
from textblob import TextBlob

#Lese Sprachcodeliste ein
codes = pd.read_csv('langcode.csv')

# Ziehe alle .gml Dateien aus dem Verzeichnis
gml_files = glob.glob('*.gml') #Alternativ in Pfadeingabe umschreiben

# Schreibe in CSV-Datei
with open('ouput.csv','w',newline='') as csvfile: #lasse keine Zeile frei
	# Abgrenzung zwischen Spalten ist ":", weil das "," auch als Trennzeichen der Wörter dient, daher ungeeignet
	csvwriter = csv.writer(csvfile, delimiter=':')
	# Füge die folgenden 3 Spaltennamen hinzu
	csvwriter.writerow(['Dateiname','Sprache','Wörter'])
	# interne Ausgabe wie weit der Zähler ist
	count = 1
	# Arbeite eine Datei nach der anderen ab
	for file in gml_files:
		# Gib den aktuellen Progress aus
		print('Processing {}/{} - {}'.format(count, len(gml_files), file))
		print(file)
		# Öffne die Gml-Datei
		with open(file, 'rb') as f:
			data = f.read()
			# Lies die gml-Datei als xml tree
			root = etree.fromstring(data)
			# Nimm den gesamten Text aus der Gml-Datei
			text_chunks = root.xpath('//text()')
			# Entferne Leerzeichen
			cleaned_chunks = [s for s in text_chunks if s.strip()]
				
			# Daten müssen bereinigt werden: füge daher nur character in das Array
			no_numbers = []
			# Entferne alle Zahlen
			for chunk in cleaned_chunks:
				s = re.sub("\d+\.\d+", "", chunk)
				s = re.sub("\d+", "", s)
				no_numbers.append(s.strip())
			# Etnferne Leerzeichen
			cleaned_result = [s for s in no_numbers if s.strip()]
			# Füge String zusammen
			result_string = ' '.join([i for i in cleaned_result])
			# print(result_string)
			tokens = wordpunct_tokenize(result_string)
			unique_tokens = list(set(tokens)) #füge alle einzigartigen Tokens (Wörter) in eine Liste
			
			final_tokens = [] #generiere Array final_token
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
				#Gleiche language name mit code-ISO-Norm ab und matche
				for i in range(0, len(codes)):
					if codes.loc[i, 'Code'] == lang_code:
						language = codes.loc[i, 'Language']
		#Schreibe das resultat in eine csv
		csvwriter.writerow([file, language, final_result])
		#Erhöhte count
		count += 1

		if __name__=='__main__':
				print ('Sprache: ' + language)
