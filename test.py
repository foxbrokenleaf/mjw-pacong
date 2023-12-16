#Build to be like     
#myDefine_WebLink = "https://cdn8.tvtvgood.com/"
#myGetencode = "cd92a8ae03d0"
#myGetuploaddate = "202204/14"
#myExpires = "1702648428"
with open("Download_list.txt",'r') as f:
    read_url_for_file_temp = f.readlines()
    for i in read_url_for_file_temp:
        i = i.replace('\n','')
        myExpires = i[i.find("&expires=",0,-1) + 9 : -1]
        myDefine_WebLink = i[0 : i.find(".com",0,-1) + 5]
        myGetuploaddate = i[i.find(".com",0,-1) + 5 : i.find(".com",0,-1) + 15]
        myGetencode = i[i.find(".com",0,-1) + 15 : i.find("playlist",0,-1) - 1]
        print(myGetencode)
    f.close()