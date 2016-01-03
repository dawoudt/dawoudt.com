from content_management import Content

TOPIC_DICT = Content()

FUNC_TEMPLATE = '''

@app.route(TOPIC_DICT["CURRENTTOPIC"][CURRENTINDEX][1], methods=['GET', 'POST'])
def CURRENTTITLE():
    return render_template("CURRENTTOPIC/CURRENTHTML", curLink = TOPIC_DICT["CURRENTTOPIC"][CURRENTINDEX][1], curTitle=TOPIC_DICT["CURRENTTOPIC"][CURRENTINDEX][0], curPost = TOPIC_DICT["CURRENTTOPIC"][CURRENTINDEX][2], curCode = TOPIC_DICT["CURRENTTOPIC"][CURRENTINDEX][3], curExpl = TOPIC_DICT["CURRENTTOPIC"][CURRENTINDEX][4], nextLink = TOPIC_DICT["CURRENTTOPIC"][NEXTINDEX][1], nextTitle = TOPIC_DICT["CURRENTTOPIC"][NEXTINDEX][0]
'''
x = False
y = False
for each_topic in TOPIC_DICT:
    #print(each_topic)

    index_counter = 0
    for eachele in TOPIC_DICT[each_topic]:
        try:
            CURRENTHTML = (eachele[1]+'.html').replace("/","")
            CURRENTTOPIC = each_topic

            CURRENTTITLE = eachele[0].replace("-","_").replace(" ","_").replace(",","").replace("/","").replace(")","").replace("(","").replace(".","").replace("!","").replace(":","-").replace("'","")
            CURRENTINDEX = str(index_counter)
            PREVINDEX = str(index_counter - 1)
            NEXTINDEX = str(index_counter + 1)
            index_counter += 1

            if index_counter >= 1:
                if x == False:
                    FUNC_TEMPLATE = FUNC_TEMPLATE[:-1] 
                    prev_items = ', prevLink = TOPIC_DICT["CURRENTTOPIC"][PREVINDEX][1])'
                    # FUNC_TEMPLATE.replace("CURRENTTOPIC",CURRENTTOPIC).replace("CURRENTINDEX",CURRENTINDEX).replace("CURRENTTITLE",CURRENTTITLE).replace("CURRENTHTML",CURRENTHTML).replace("NEXTINDEX",NEXTINDEX) )
                    FUNC_TEMPLATE += prev_items
                    x = True   
                if len(TOPIC_DICT['Blog']) == index_counter:
                    print( FUNC_TEMPLATE.replace("CURRENTTOPIC",CURRENTTOPIC).replace("CURRENTINDEX",CURRENTINDEX).replace("CURRENTTITLE",CURRENTTITLE).replace("CURRENTHTML",CURRENTHTML).replace("NEXTINDEX","0").replace("PREVINDEX", PREVINDEX) )
                else:
                    print( FUNC_TEMPLATE.replace("CURRENTTOPIC",CURRENTTOPIC).replace("CURRENTINDEX",CURRENTINDEX).replace("CURRENTTITLE",CURRENTTITLE).replace("CURRENTHTML",CURRENTHTML).replace("NEXTINDEX",NEXTINDEX).replace("PREVINDEX", PREVINDEX) )

            else:
                FUNC_TEMPLATE += ')'
                print( FUNC_TEMPLATE.replace("CURRENTTOPIC",CURRENTTOPIC).replace("CURRENTINDEX",CURRENTINDEX).replace("CURRENTTITLE",CURRENTTITLE).replace("CURRENTHTML",CURRENTHTML).replace("NEXTINDEX",NEXTINDEX).replace("PREVINDEX", PREVINDEX) )

        except Exception as e:
            print(str(e))	  
	  