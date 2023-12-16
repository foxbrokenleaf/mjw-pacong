from fnmatch import fnmatch
#==================数据区（全局）=============================
myGetencode = "cd92a8ae03d0"
myGetuploaddate = "202204/14"
#===========================================================

#=========================下载链接组成模块====================================
myFile = open("F:\\MyProject\\snake\\playlist.m3u8","r",encoding="UTF-8")
counter = 0
for i in myFile.readlines():
    if fnmatch(i,"playlist*"):
        counter += 1
myUrl = "https://cdn8.tvtvgood.com/" + myGetuploaddate + "/" + myGetencode + "/playlist"
file_name = ".ts"
myDefine_file = []
for i in range(counter):
    myBuildUrl = myUrl + i.__str__() + file_name
    myDefine_file.append(myBuildUrl)
myFile.close()
#print(myDefine_file[1]) #测试
#==========================================================================

#=========================找到存在于html中的密匙模块=========================
myFile = open("F:\\MyProject\\snake\\1272-1-1.html","r",encoding="UTF-8")
temp_str = myFile.readlines()
myFile.close()
for i in temp_str:
    if fnmatch(i,"*player_aaaa*"):
        temp_str = i
        break
counter = 0
encode = ""
print(temp_str)
n = temp_str.find("\"url\"",0,len(temp_str)) + 7
m = temp_str.find("\"",n,len(temp_str))

#==========================================================================