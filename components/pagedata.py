

########################## This file is for get only the required page data #####################
import psycopg2
conn = psycopg2.connect(database="quotationbot", user = "cloobot", password = "cloobot", host = "localhost", port = "5432")
# conn = psycopg2.connect(database="quotationbot", user = "postgres", password = "Logapriya@213", host = "localhost", port = "5432")

import ast
cur = conn.cursor()


def get_page_data(from_no,to_no,page_no,table_name,search_text,required):
    if(search_text == ""):
        cur.execute("select * from "+table_name+" ORDER BY timestamp DESC;")
        table_data = cur.fetchall()
        # print(table_data)
        if(required == "view"):
            try:
                return list(table_data[from_no - 1:to_no])
            except:
                try:
                    return list(table_data[from_no - 1: len(table_data)])
                except:
                    return []
        else:
            return table_data
    else:
        search = " | ".join(search_text.split(' '))
        print('\n\n data going to searchsearch :',search,"\n\n")
        cur.execute("with q as (select to_tsquery(%s) as query),ranked as (select f_id,f_topic,f_anstext,f_anslink,ts_rank_cd(tsv, query) as rank from "+table_name+" ,q where q.query @@ tsv order by rank desc) select f_id, ts_headline(f_topic,q.query),ts_headline(f_anslink, q.query) from ranked,q order by ranked desc;",(search,))
        search_result = cur.fetchall()
        print("\n\n serch result : ",search_result,"\n\n")
        table_data = []
        for each_res in search_result:
            cur.execute("select * from faq where f_id = %s",(each_res[0],))
            table_data.append(cur.fetchone())
        if(required == "view"):
            try:
                return list(table_data[from_no - 1:to_no])
            except:
                try:
                    return list(table_data[from_no - 1: len(table_data)])
                except:
                    return []
        else:
            return table_data


def get_page_no(table_name,search_text):
    if(search_text == ""):
        cur.execute("select * from "+table_name+" ;")
        table_data = cur.fetchall()
        # print(table_data)
        try:
            return len(table_data)
        except:
            print("unknown error in page adata")
    else:
        search = " | ".join(search_text.split(' '))
        print('\n\n data going to searchsearch :',search,"\n\n")
        cur.execute("with q as (select to_tsquery(%s) as query),ranked as (select f_id,f_topic,f_anstext,f_anslink,ts_rank_cd(tsv, query) as rank from "+table_name+" ,q where q.query @@ tsv order by rank desc) select f_id, ts_headline(f_topic,q.query),ts_headline(f_anslink, q.query) from ranked,q order by ranked desc;",(search,))
        search_result = cur.fetchall()

        try:
            return len(search_result)
        except:
            print("unknown error in page adata")


def search(data,search_text,all_cols_list,datatypes_list,search_cols_list):
    try:
        cur.execute("drop table for_search")
    except:
        pass
    print("\n\n for search dropped \n\n")
    with_datatype = []
    for i in range(len(all_cols_list)):
        with_datatype.append(all_cols_list[i]+" "+datatypes_list[i])
    create_str = ','.join(with_datatype)
    all_col = ','.join(all_cols_list)
    search_col = ','.join(search_cols_list)
    conn.commit()
    # cur.execute("create table for_search(i_id text,center text,email text,product text,location text,name text,phone text,tsv tsvector);")
    cur.execute("create table for_search("+create_str+",tsv tsvector);")

    print("\n\n for search created \n\n")
    # cur.execute("create trigger tcvrealtime before insert or update on for_search for each row execute procedure tsvector_update_trigger(tsv,'pg_catalog.english',email,name,location,phone,center,product);")
    cur.execute("create trigger tcvrealtime before insert or update on for_search for each row execute procedure tsvector_update_trigger(tsv,'pg_catalog.english',"+search_col+");")
    print("\n\n trigger created \n\n")
    cur.execute("create index fts_index on for_search using gin(tsv);")
    print("\n\n index created \n\n")
    conn.commit()
    for each_row in data:
        # cur.execute("INSERT INTO for_search ('i_id','center','email','product','location','name','phone') VALUES (%s,%s,%s,%s,%s,%s,%s)",(each_row['i_id'],each_row['center'],each_row['email'],each_row['product'],each_row['location'],each_row['name'],each_row['phone']))
        cur.execute("INSERT INTO for_search ("+all_col+") VALUES (%s,%s,%s,%s,%s,%s)",(each_row['q_id'],each_row['client'],each_row['descr'],each_row['part'],each_row['sal_ex'],each_row['manager']))
    conn.commit()
    # cur.execute("with q as (select to_tsquery(%s) as query),ranked as (select i_id,center,email,product,location,name,phone,ts_rank_cd(tsv, query) as rank from for_search,q where q.query @@ tsv order by rank desc) select i_id from ranked,q order by ranked desc;",(search_text,))
    cur.execute("with q as (select to_tsquery(%s) as query),ranked as (select "+all_col+",ts_rank_cd(tsv, query) as rank from for_search,q where q.query @@ tsv order by rank desc) select "+all_cols_list[0]+" from ranked,q order by ranked desc;",(search_text,))
    search_result = list(cur.fetchall())
    id_list = []
    for each in search_result:
        id_list.append(each[0])
    print("\n\n search_result \n\n",id_list,"\n\n")
    
    return id_list


def search_report(data,search_text,all_cols_list,datatypes_list,search_cols_list):
    try:
        cur.execute("drop table for_search")
    except:
        pass
    print("\n\n for search dropped \n\n")
    with_datatype = []
    for i in range(len(all_cols_list)):
        with_datatype.append(all_cols_list[i]+" "+datatypes_list[i])
    create_str = ','.join(with_datatype)
    all_col = ','.join(all_cols_list)
    search_col = ','.join(search_cols_list)
    conn.commit()
    # cur.execute("create table for_search(i_id text,center text,email text,product text,location text,name text,phone text,tsv tsvector);")
    cur.execute("create table for_search("+create_str+",tsv tsvector);")

    print("\n\n for search created \n\n")
    # cur.execute("create trigger tcvrealtime before insert or update on for_search for each row execute procedure tsvector_update_trigger(tsv,'pg_catalog.english',email,name,location,phone,center,product);")
    cur.execute("create trigger tcvrealtime before insert or update on for_search for each row execute procedure tsvector_update_trigger(tsv,'pg_catalog.english',"+search_col+");")
    print("\n\n trigger created \n\n")
    cur.execute("create index fts_index on for_search using gin(tsv);")
    print("\n\n index created \n\n")
    conn.commit()
    for each_row in data:
        # cur.execute("INSERT INTO for_search ('i_id','center','email','product','location','name','phone') VALUES (%s,%s,%s,%s,%s,%s,%s)",(each_row['i_id'],each_row['center'],each_row['email'],each_row['product'],each_row['location'],each_row['name'],each_row['phone']))
        cur.execute("INSERT INTO for_search ("+all_col+") VALUES (%s,%s)",(each_row['id'],each_row['name']))
    conn.commit()
    # cur.execute("with q as (select to_tsquery(%s) as query),ranked as (select i_id,center,email,product,location,name,phone,ts_rank_cd(tsv, query) as rank from for_search,q where q.query @@ tsv order by rank desc) select i_id from ranked,q order by ranked desc;",(search_text,))
    cur.execute("with q as (select to_tsquery(%s) as query),ranked as (select "+all_col+",ts_rank_cd(tsv, query) as rank from for_search,q where q.query @@ tsv order by rank desc) select "+all_cols_list[0]+" from ranked,q order by ranked desc;",(search_text,))
    search_result = list(cur.fetchall())
    id_list = []
    for each in search_result:
        id_list.append(each[0])
    print("\n\n search_result \n\n",id_list,"\n\n")
    
    return id_list