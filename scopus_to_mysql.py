

#############################
# import
#############################
import io
import os
import json
import mysql.connector
import datetime
from shutil import copyfile

#############################
# parameters
#############################

# hand enter
keyword="patronage"
fname_userpw="mysql_idpw.txt"
host_name="localhost"
db_name="scopus_patronage"
data_prefix="patronage_190612_1844_SOCI_year_STANDARD"
mysql_datain_fdir="C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/scopus/"+keyword+"/datain/"

# created from hand entered parameters
scopus_corpus_fdir="../data_scopus_"+keyword+"/"
corpus_name="corpus_"+keyword
corpus_out_fname=data_prefix+"_corpus.csv"
scopus_rawdata_fdir=scopus_corpus_fdir+data_prefix+"/"
now = datetime.datetime.now()

#dataout_fdir="../data_out/"

field_list=[
	# fields in STANDARD & COMPLETE
	"dc:identifier",			# id
	"dc:title",					# title
	"dc:creator",				# author
	"prism:publicationName",	# publication
	"prism:coverDate",			# date
	"citedby-count",			# cited-by count
	"prism:aggregationType",	# type
	"subtype",					# subtype
	"source-id",				# source-id

	# additional fields in COMPLETE
	"dc:description",			# abstract
	"authkeywords"				# author keywords
]

field_edited_dic={
	# fields in STANDARD & COMPLETE
	"dc:identifier":"article_id",				# id
	"dc:title":"article_title",					# title
	"dc:creator":"article_author",				# author
	"prism:publicationName":"journal_name",		# publication
	"prism:coverDate":"publication_date",		# date
	"citedby-count":"citation_count",			# cited-by count
	"prism:aggregationType":"journal_type",		# type
	"subtype":"journal_subtype",				# subtype
	"source-id":"journal_id",					# source-id

	# additional fields in COMPLETE
	"dc:description":"abstract",				# abstract
	"authkeywords":"author_keywords"			# author keywords
}
	
print("\nfield list")
[print(field) for field in field_list]

d_ind={key:index for index,key in enumerate(field_list)}

print("\field dictionary")
[print(key,":",str(d_ind[key])) for key in list(d_ind.keys())]

############################
# new functions
############################
def instantiate_db(host_name,db_name,fname_userpw):

	fin_userpw=open(fname_userpw)
	userpw=fin_userpw.readlines()

	mydb = mysql.connector.connect(
	  host=host_name,
	  user=userpw.pop(0).strip(),
	  passwd=userpw.pop(0).strip(),
	  database=db_name
	)
	
	return mydb


def drop_and_create_table_corpus(mydb,field_list,corpus_name):

	# drop table corpus_name
	try:
		q="drop table "+corpus_name+";"
		print("\nquery:\t",q)
		mycursor=mydb.cursor()
		mycursor.execute(q)
		#myresult = mycursor.fetchall()
		#print(myresult)
		print("\ndropped table "+corpus_name+"")
	except mysql.connector.Error as e:
		print(e)
	
	# create table corpus_name
	text_field_list=["dc:title","prism:aggregationType","dc:description","authkeywords"]
	last_index=len(field_list)-1
	q="create table "+corpus_name+" ( "
	for index,field in enumerate(field_list):
		if field in text_field_list:
			q+="`"+field_edited_dic[field]+"` Text,"
		else:
			q+="`"+field_edited_dic[field]+"` VarChar(100),"
	q+=" primary key("+field_edited_dic["dc:identifier"]+")"
	q+=") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
	print("\nquery:\t",q)
	mycursor=mydb.cursor()
	mycursor.execute(q)
	#myresult = mycursor.fetchall()
	#print(myresult)
	print("\ncreated table "+corpus_name)

def copy_csv_to_ProgramData(scopus_corpus_fdir,data_prefix,mysql_datain_fdir):
	
	fname=data_prefix+"_corpus.csv"
	
	src=scopus_corpus_fdir+fname
	dst=mysql_datain_fdir+fname
	
	copyfile(src,dst)
	
	print("\ncorpus copied","\nfrom: ",src,"\nto: ",dst)


def load_data_table_corpus(mydb,db_name,corpus_name,mysql_datain_fdir,data_prefix):

	fname=data_prefix+"_corpus.csv"
	
	null_field_list=["dc:description","authkeywords"]

	q="load data infile \""+mysql_datain_fdir+fname+"\""
	q+=" ignore into table "+db_name+"."+corpus_name
	q+=" fields terminated by \"$\" enclosed by ''"
	q+=" lines terminated by \"\\r\\n\" starting by ''"
	q+=" ignore 1 rows"
	q+=" ("
	last_index=len(field_list)-1
	for index,field in enumerate(field_list):
		if field in null_field_list:
			q+="@v"
		q+=field_edited_dic[field]
		if index!=last_index:
			q+=", "
	q+=" )"
	q+=" set "
	last_index=len(null_field_list)-1
	for index,field in enumerate(null_field_list):
		q+=field_edited_dic[field]+"=nullif(@v"+field_edited_dic[field]+",\"\")"
		if index!=last_index:
			q+=", "
	q+=";"
	
	print("\nquery:\t",q)
	mycursor=mydb.cursor()
	mycursor.execute(q)
	mydb.commit()
	
	q="select * from "+corpus_name+";"
	print("\nquery:\t",q)
	mycursor=mydb.cursor()
	mycursor.execute(q)
	myresult = mycursor.fetchall()
	
	print("\nloaded csv data to "+corpus_name+": ",str(len(myresult))," lines")
	
	# print the first row
	q="select * from "+corpus_name+" limit 1;"
	mycursor=mydb.cursor()
	mycursor.execute(q)
	myresult = mycursor.fetchall()
	print(len(myresult))
	print(myresult)
	
		
def select_node_string(mydb,corpus_name):
	
	q="select article_id,author_keywords from "+corpus_name+" where author_keywords is not null;"
	
	print("\nquery:\t",q)
	mycursor=mydb.cursor()
	mycursor.execute(q)
	myresult = mycursor.fetchall()
	print("records with non-null keywords: ",str(len(myresult)))
	print("one example: ",myresult[1])
	
	return myresult
	
def process_node_strings(node_strings):

	nodes=[]

	temp_list=[list(tuple) for tuple in node_strings]
	
	replace_with_space=["&amp;"," and "]
	replace_with_nospace=["-",'\'',"`","\"","‘","’","“","”","«","»","(",")","*","#","[","]","≠"]
	
	
	remove_list=[
		"inc. all rights reserved.",
		"25.00 (hardcover);"
	]
	
	replace_dict={
		"israël":"israel",
	}
	
	for item in temp_list:
		id=item[0]
		
		# strip white space and convert to lowercase
		local_kw1=item[1].strip("\n").strip("\r").lower()
		
		# replace any items in replace_with_space, replace_with_nospace, and replace_dict
		for item in replace_with_space:
			local_kw1=local_kw1.replace(item," ")
		for item in replace_with_nospace:
			local_kw1=local_kw1.replace(item,"")
		for key in list(replace_dict.keys()):
			local_kw1=local_kw1.replace(key,replace_dict[key])
			
		# split once on '|' and again on ','
		local_kw1=local_kw1.split("|")
		local_kw2=[item.split(",") for item in local_kw1]
		
		# re-combine lists into a single list
		local_kw3=[]
		for item in local_kw2:
			local_kw3+=item		
			
		# strip white space
		local_kw3=[item.strip() for item in local_kw3]
		
		# filter out nodes too short, too long, and in remove_list
		local_kw3=[item for item in local_kw3 if len(item)>1 and len(item)<50 and item not in remove_list]
		
		# filter out duplicates
		local_kw3=list(set(local_kw3))
		
		# append each (article_id,nodel label) pair
		for kw in local_kw3:
			nodes.append((id,kw))
				
	# filter out duplicates one more time...
	nodes=list(set(nodes))
	
	# print some nodes
	[print(node) for node in nodes[1:200]]
	
	# calculate number of unique nodes
	unique_node_list=[]
	for pair in nodes:
		unique_node_list.append(pair[1])
	unique_node_list=list(set(unique_node_list))
		
	print("\nnodes: ",len(nodes))
	print("\nunique nodes: ",len(unique_node_list))
	
	return nodes 
	
def create_table_nodelist_and_insert_nodes(mydb,keyword,nodes):

	# drop table nodelist_keyword
	try:
		q="drop table nodelist_"+keyword+";"
		print("\nquery:\t",q)
		mycursor=mydb.cursor()
		mycursor.execute(q)
		#myresult = ,mycursor.fetchall()
		#print(myresult)
		print("\ndropped table nodelist_keyword")
	except mysql.connector.Error as e:
		print(e)
	
	# create table nodelist_keyword
	q="create table nodelist_"+keyword+" ( "
	q+=" `article_id` VarChar(100),"
	q+=" `node_label` VarChar(50),"
	q+=" primary key(article_id,node_label)"
	q+=") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"
	print("\nquery:\t",q)
	mycursor=mydb.cursor()
	mycursor.execute(q)
	#myresult = mycursor.fetchall()
	#print(myresult)
	print("\ncreated table nodelist_keyword")
	
	# insert nodes into table nodelist_keyword
	q="insert ignore into nodelist_"+keyword+" (article_id,node_label) values (%s,%s)"
	print("\nquery:\t",q)
	
	current_count=0
	batch_volume=10000
	node_count=len(nodes)
	
	while(current_count<node_count):
		remaining_count=node_count-current_count
		if remaining_count<batch_volume:
			batch_volume=remaining_count
		next_count=current_count+batch_volume
		node_batch=nodes[current_count:next_count]
		mycursor=mydb.cursor()
		mycursor.executemany(q,node_batch)
		mydb.commit()
		print("\nrows inserted: ",mycursor.rowcount)
		current_count=next_count
	
# alter corpus. add year column
def alter_corpus_add_year(mydb,corpus_name):

	id_field=field_edited_dic["dc:identifier"]
	date_field=field_edited_dic["prism:coverDate"]
	
	try:
		q="drop table temp;"
		print("\nquery:\t",q)
		mycursor=mydb.cursor()
		mycursor.execute(q)
	except mysql.connector.Error as e:
		print(e)
	
	q="create table temp as select * from "+corpus_name+";"
	print("\nquery:\t",q)
	mycursor=mydb.cursor()
	mycursor.execute(q)
	
	try:
		q="drop table "+corpus_name+";"
		print("\nquery:\t",q)
		mycursor=mydb.cursor()
		mycursor.execute(q)
	except mysql.connector.Error as e:
		print(e)
		
	q="create table "+corpus_name+" as"
	q+=" select a.*,left("+date_field+",4)*1 as publication_year"
	q+=" from temp as a;"
	print("\nquery:\t",q)
	mycursor=mydb.cursor()
	mycursor.execute(q)
	
	q="alter table "+corpus_name+" add primary key ("+id_field+");"
	print("\nquery:\t",q)
	mycursor=mydb.cursor()
	mycursor.execute(q)
	
	try:
		q="drop table temp;"
		print("\nquery:\t",q)
		mycursor=mydb.cursor()
		mycursor.execute(q)
	except mysql.connector.Error as e:
		print(e)


#############################
# old functions to keep
#############################

def import_corpus_from_files(fdir,d_ind):

	# import file list
	flist = os.listdir(fdir)
	flist.sort()
	print("Files: "+str(len(flist)))

	# instantiate corpus
	corpus={}
	totalcount=0
	errorcount=0
	null_dat=['' for keyword in list(d_ind.keys())]
	missing_key_dic={}

	# iterate through all json files in the directory
	for f in flist:

		print("######"+f)
		
		fin=io.open(fdir+f,encoding="utf-8")
		fj=json.load(fin)
		fin.close()
		
		entry_list= [entry for entry in fj["search-results"]["entry"] if "error" not in entry.keys()]
		ecount=len(entry_list)
		totalcount+=ecount

		#print(ecount,totalcount)
		
		
		# iterate through each entry in each json file
		if entry_list:
		
			for e in entry_list:

				#copy null_dat list to dat: instantiate dat_list equal in length to fields in d_kw
				dat=null_dat.copy()
				for key in list(d_ind.keys()):
					try:
						dat[d_ind[key]]=str(e[key])
					except KeyError:
						errorcount+=1
						if key in missing_key_dic.keys():
							missing_key_dic[key]+=1
						else:
							missing_key_dic[key]=1
				try:
					corpus[e["dc:identifier"]]=dat
				except KeyError:
					print("\nKeyError: missing dc:identifier")
					print(e)

	print("total entries: ",totalcount)
	print("corpus size: ",len(corpus))
	print("errors: ",errorcount)
	print("missing keys: ")
	[print("\t",key,":",missing_key_dic[key]) for key in list(missing_key_dic.keys())]
	
	return corpus
	
def export_corpus_to_csv(corpus_out_fdir,corpus_out_fname,d_ind,corpus):

	keys = list(d_ind.keys())
	header_str="$".join(keys)
	
	fout=io.open(corpus_out_fdir+corpus_out_fname,'w',encoding="utf-8")
	fout.write(header_str+"\n")
	[fout.write("$".join(e)+"\n") for e in list(corpus.values())]
	fout.close()
	
def import_corpus_from_csv(corpus_out_fdir,corpus_out_fname):

	fin=io.open(corpus_out_fdir+corpus_out_fname,encoding="utf-8")
	dat = fin.readlines()
	fin.close()
	
	print(dat.pop(0))
	corpus={}
	for e in dat:
		e_list=e.strip().split("$")
		corpus[e_list[0]]=e_list
		
	return corpus	


		
#############################
# main
#############################	

# instantiate mydb
mydb=instantiate_db(host_name,db_name,fname_userpw)


# import corpus from files and save to csv
if True:

	corpus = import_corpus_from_files(scopus_rawdata_fdir,d_ind)
	export_corpus_to_csv(scopus_corpus_fdir,corpus_out_fname,d_ind,corpus)


# copy data to ProgramData, create table corpus, and load data
if True:	

	# save copy of csv corpus to ProgramData/MySQL
	copy_csv_to_ProgramData(scopus_corpus_fdir,data_prefix,mysql_datain_fdir)

	mydb=instantiate_db(host_name,db_name,fname_userpw)
	drop_and_create_table_corpus(mydb,field_list,corpus_name)
	
	load_data_table_corpus(mydb,db_name,corpus_name,mysql_datain_fdir,data_prefix)
	
	alter_corpus_add_year(mydb,corpus_name)


# parse and clean nodes, create node & edge lists
if True:

	node_strings=select_node_string(mydb,corpus_name)	
	nodes=process_node_strings(node_strings)
	create_table_nodelist_and_insert_nodes(mydb,keyword,nodes)
	



# any additional processesing steps? or can I do the rest in R?

	# in R.
	#
	# 	1. visualize networks in R. edge and node size by weight
	#	2. join edge-id and node-id lists to corpus on id
	# 	3. add features for visualization: citation counts, subsets
			
