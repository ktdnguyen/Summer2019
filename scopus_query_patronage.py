##################################
# Instructions
##################################
#
#	This script performs a search of the Elsevier SCOPUS database.
#
#	The current iteration, as of 2019.02.27, allows you to specify:
#
#	0. keyword:
#		word or phrase to search
#	1. start_year,  end_year:
#		search start year > end year, from present, backward
#	2. oneYearFlag:
#		return single result for each year (view metadata but not download everything)
#		or loop over all results for each year (returns all results)
#	3. out_path, fout_name_stem
#		specify directory for output and name stem for exported files
#	4. query_term:
#		variable specifying discipline and items to search, over all time periods
#	5. query_term_year:
#		adds publication year onto query_term parameters. searches a particular year
#	6. view_type:
#		"STANDARD" or "COMPLETE" view.
#		refer here for more details: https://dev.elsevier.com/api_key_settings.html
#		and here too: https://dev.elsevier.com/guides/ScopusSearchViews.htm
#
# 	Recommended procedure
#
#	1. conduct meta-search
#		- select the appropriate keyword or phrase
#		- "STANDARD" search. conduct from Stanford IP so that q_count=200. otherwise =25.
#		- oneYearFlag = TRUE. loop over all years, but not over all entries in all years
#		- start_year = 2019 (present year)
#		- end_year = 1900 (or earliest year we want to check)
# 		- (automatic) choose an out_path and fout_name_stem that reflects these choices
#
#	2. once we know how many entries are involved, collect data
#		- keep the same keyword or phrase
#		- "COMPLETE" search. conduct from Stanford IP so that complete is possible.
#		- oneYearFlag = FALSE. loop over all years, but not over all entries in all years
#		- start_year = 2019 (present year)
#		- end_year = set to earliest year that keyword appeared in meta-search
# 		- (automatic) choose an out_path and fout_name_stem that reflects these choices
#
###################################
# json viewer
##################################
#
#	to scan json output, cut and paste json text into this viewer
#
#	http://jsonviewer.stack.hu/
#
#
##################################
# query parameters
##################################

search_term="patronage"

#view_type="COMPLETE"		# "COMPLETE": max q_count 25 when running from a Stanford IP
view_type="STANDARD"		# "STANDARD": max q_count 200 when running from a Stanford IP

start_year=2019				# start_year > end_year. run backwards from present
end_year=2017				# earliest occurence of keyword in SCOPUS
oneYearFlag = True			# oneYearFlag = True: only one query for each year

authorizedIPFlag=False		# accessing from an authorized IP, e.g. Stanford University

##################################
# import libraries
##################################
import requests
import io
import json
from datetime import datetime
import os


##################################
# function definitions
##################################
#import requests

def export_json(jsondat,out_path,fname_out_stem,year,file_count):

		# export JSON output
		fout_name=out_path+fout_name_stem+"_"+str(year)+"_"+str(file_count)+".json"
		fout = io.open(fout_name,'w',encoding="utf-8")
		fout.write(jsondat)
		fout.close()
		print("sucessfully exported "+fout_name)
		
		
		
##################################
# construct query & output path variables
##################################

keyword = "\""+search_term+"\""

d=datetime.now()
out_path = search_term+"_"+d.strftime("%y%m%d_%H%M")+"_SOCI_year_"+view_type+"/"
print(out_path)
if not os.path.exists(out_path):
	os.mkdir(out_path)
fout_name_stem=search_term+"_"+view_type
query_term="TITLE-ABS-KEY("+keyword+") AND SUBJAREA(SOCI)"
query_term_year = query_term+" AND PUBYEAR = "+str(end_year)
#cursor_value="*"
start_value=0

#out_path = "q3_sc_titleabskey_sbjarea/"
#fout_name_stem="sc_titleabskey_sbjarea"
#query_term="TITLE-ABS-KEY(social capital) AND SUBJAREA(SOCI)"
#start_value=0

#out_path = "q2_sc_titleabskey/"
#fout_name_stem="sc_titleabskey"
#query_term="TITLE-ABS-KEY(social capital)"
#start_value=0

# specify export parth 
#out_path = "q1_sc/"
#fout_name_stem="sc"
#query_term="social capital"


##################################
# request url and grab some meta-data
##################################

# more parameter selection for initializing payload and url
q_count=25					# >25 throws an error

if view_type=="STANDARD":
	q_count=200
	
if not authorizedIPFlag:		# if not accessing from an authorized IP, then override user-selected parameter settings and set parameters accepted by SCOPUS
	view_type=="STANDARD"
	q_count=25

api_key=open("scopus_apikey.txt").readline().split(":")[1].strip()
#print("api_key:",api_key)
root_url="https://api.elsevier.com/content/search/scopus"


# construct request payload
payload={
			"query":query_term,
			"apiKey":api_key,
			"view":view_type,
			"start":start_value,
			#"cursor":cursor_value,
			"count":q_count
		}

# request first url
r = requests.get(root_url,params=payload)
print(r.url)
print("\nstatus code: "+str(r.status_code))
print("output len: "+str(len(r.text)))

if r.status_code==400:
	print("\n\n================================================\n")
	print("Status Code=400. This query returned an INVALID_INPUT status.")
	print("The most likely reason for this is that the query exceeds the maximum number allowed for the service level.")
	print("\nWhen accessing from an authorized IP address (e.g. Stanford University), the maximium number of entries allowed per request are:")
	print("\tCOMPLETE: 25")
	print("\tSTANDARD: 200")
	print("\nWhen accessing from outside an authorized IP address, the maximium number of entries allowed per request are:")
	print("\tCOMPLETE: 0")
	print("\tSTANDARD: 25")
	print("\nIf you are accessing SCOPUS from outside an authorized IP address, set:")
	print("\tview_type: STANDARD")
	print("\tq_count: 25")
	print("\n================================================\n\n")

job = r.json()
total_count = job["search-results"]["opensearch:totalResults"]
print("total count: "+str(total_count))



##################################
# cycle through queries by year
##################################
agg_count=0
earliest_year=start_year
year_list = list(range(end_year,start_year+1))
year_list.reverse()

for year in year_list:

	current_count=-1
	total_count=0
	startIndex=0

	while(current_count<total_count):

		query_term_year = query_term+" AND PUBYEAR = "+str(year)
		print(query_term_year)
		payload["query"]=query_term_year
		payload["start"]=startIndex
			
		# request first url
		r = requests.get(root_url,params=payload)
		
		print(r.url)
		print(r.status_code)
		#print(len(r.text))

		job = r.json()
		total_count = int(job["search-results"]["opensearch:totalResults"])
		if total_count>0: earliest_year=year
		startIndex = int(job["search-results"]["opensearch:startIndex"])
		perPage = int(job["search-results"]["opensearch:itemsPerPage"])
		numEntries = len(job["search-results"]["entry"])
		current_count = startIndex+perPage
		agg_count+=numEntries
		print(str(year)+"\t"+"total count: "+str(total_count)+"\t aggregate count: "+str(agg_count)+"\t earliest year thus far: "+str(earliest_year))
		
		count_to_report=current_count
		if oneYearFlag:
			count_to_report=total_count
		
		export_json(r.text,out_path,fout_name_stem,year,count_to_report)
			
		# update startIndex for next cycle
		startIndex = current_count
		
		if oneYearFlag:
			current_count=total_count

