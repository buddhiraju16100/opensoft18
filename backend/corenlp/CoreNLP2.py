import os
from stanfordcorenlp import StanfordCoreNLP

def list_match(l1,l2) : #Function to check whether lists have any element in common
	for a in l1:
		for b in l2:
			if a==b:
				return 1
	return 0

def word_match(l1,w) : #Function to check for 2d lists 
	for a in l1:
		if a[1]==w:
			return l1.index(a) +1
	return 0

def word_match_2(l1,w) : #Function to check for 1d lists
	for a in l1:
		if a==w:
			return l1.index(a) +1
	return 0

def core(rows,boundbox): # The main function of this file
	# Replace this addres by the place where you unzip the file of NLP installation
	nlp = StanfordCoreNLP(
		os.path.join(os.path.dirname(os.path.realpath(__file__)), "stanford-corenlp-full-2018-02-27"))

	#y axis assumed vertical/height and x- axis is horizontal/width

	qual_list=["allergist", "anaesthesiologist", "anasthesiologist", "anesthesiologist", "andrologist", "cardiologist", "consultant" "dermatologist", "dentist", "diabetologist", "dietician",  "electrophysiologist", "endocrinologists", "epidemiologist", "gastroenterologist", "geneticist", "geriatrician", "gynaecologist",  "gynecologist", "hematologist", "hepatologist", "immunologist", "intensivist", "neonatologist", "nephrologist", "neurologist", "neurosurgeon", "obstetrician", "onconlogist", "ophthalmologist", "orthopedist", "osteopaths", "otolaryngologists", "parasitologist", "pathologist", "pediatrician",  "perinatologist", "Periodontist", "physiatrists", "physician", "podiatrist", "psychiatrist", "psychologist", "pulmonologists", "radiologist", "specialist", "surgeon", "urologist", "veterinarian", "mbbs", "m.b.b.s.", "bmbs", "m.d.", "md", "b.m.b.s.", "mbchb", "m.b.c.h.b.", "mbbch", "m.b.b.c.h.", "ms", "m.s."]# possible speciliazation, add if any

	i=1 #working variable
	j=0 #working variable
	hosp=''	#hosp_name
	doc='' #doc_name
	addr='' #hosp_addr
	qual='' #doc_qualification		
	phone_no='' #phone_no
	email_id='' #email_id

	lis=["hospital","clinic","center","centre","diagnostic","diagnostics"] #usually this is what name of hospital has, check spellings and add more if any
	

	text = boundbox[0].bound_text
	

	lis1=nlp.ner(text) #NER is a Named entity recognition function in the core nlp API


	#print(lis1)
	
	element=lis1[0]
	

	for element in lis1 : # for phone number and email
		if(element[1]=="NUMBER") :
			if(len(element[0])>8) : #length of phone no.>=7
				phone_no=phone_no + ' ' + element[0]

		if(element[1]=="EMAIL") :
			email_id=email_id + ' ' + element[0]
			
	i=1	

	while boundbox[i].box_type=='W': #To check doctors qualification/specialization
		k= word_match_2(qual_list,(boundbox[i].bound_text.lower())) 
		if k>0:
			qual=qual + ' ' + qual_list[k-1]					
		i=i+1

	j=i

	while boundbox[i].tl.y<0.3*rows: # we will check in the top 30% of paper only
		i=i+1

	k=j
	l=1
	while k<i:
		#to find doctors name 
		
		if list_match(nlp.word_tokenize(boundbox[k].bound_text.lower()),["dr.","dr"]):
				#tokenise is a basic function seperates string into words/indivisual characters/symbols

			lis1=nlp.ner(boundbox[k].bound_text)
			l=0

			a=lis1[0]
			for a in lis1 :
				if a[1]=="PERSON" :
					l=1 
					doc=doc + ' ' + a[0]

				elif l==1 :
					break 

						

			lis1=nlp.pos_tag(boundbox[k].bound_text)
			l=0

				
			a=lis1[0]
			for a in lis1 :
				if a[1]=="NNP" :
					l=1 
					doc=doc + ' ' + a[0]

				elif l==1 :
					break 
						

			break
		k=k+1



	k=j	
	l=1

	while k <i:
		if (list_match (( nlp.word_tokenize ( boundbox[k].bound_text.lower())),lis)) :
			lis1=nlp.pos_tag(boundbox[k].bound_text)
						
			
			l=0
			a=lis1[0]
			for a in lis1 :	
				if a[0]  not in ['.',',','-'] :
					hosp=hosp + ' ' + a[0]
					l=1
				elif l==1 :
					break;
				
			
			break;
		k=k+1


	j=k+1
	while j<k+3:
		
		listy=nlp.ner(boundbox[j].bound_text)
		l=word_match(listy,"LOCATION")
		if(l<=0):
			word_match(listy,"CITY")
		if(l<=0):
			word_match(listy,"STATE_OR_PROVINCE")
		if(l<=0):
			word_match(listy,"COUNTRY")
					
		lis1=nlp.pos_tag(boundbox[j].bound_text)
		
		if l>0 :
			
			i=l-2
			while (lis1[i][0]!="NNP") and i>=0 :
				addr=lis1[i][0] + addr
				i=i-1
			
			addr =addr + ' ' + lis1[l-1][0]
			i=l

			while (lis1[i][0]!="NNP") and i<len(lis1) :
				addr= addr + lis1[i][0]
				i=i+1
		j=j+1

	nlp.close()

	output_list=[]
	output_list.append(hosp)#hosp_name
	output_list.append(doc) #doc_name
	output_list.append(addr) #hosp_addr
	output_list.append(qual) #doc_qualification
	output_list.append(phone_no) #contact_details
	output_list.append(email_id) #email_id

	return output_list