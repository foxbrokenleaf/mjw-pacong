from fnmatch import fnmatch
import requests
#==================数据区（全局）=============================
myDefine_WebLink = "https://cdn8.tvtvgood.com/"
myGetencode = "cd92a8ae03d0"
myGetuploaddate = "202204/14"
mySign = "1702648428"
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
}
#===========================================================

#=========================下载链接组成模块====================================
#从playlist.m3u8文件开始组成
myFile = open(mySign,"r",encoding="UTF-8")
counter = 0
for i in myFile.readlines():
    if fnmatch(i,"playlist*"):
        counter += 1
myUrl = myDefine_WebLink + myGetuploaddate + "/" + myGetencode
file_name = ".ts"
myDefine_file = []
for i in range(counter):
    myBuildUrl = myUrl + "/playlist" + i.__str__() + file_name
    myDefine_file.append(myBuildUrl)
myFile.close()
#==========================================================================

#========================文件下载模块=======================================
myRequestsStatusList = []
total = counter
counter = 0
SaveRequestsStatusListFile = open("download\\RequestsStatusListFile","w+")
for j in myDefine_file[:-1]:
    response = requests.get(j,headers=headers,stream=True)
    myRequestsStatusList.append([response.status_code,"playlist" + counter.__str__()])
    SaveRequestsStatusListFile.writelines(str(myRequestsStatusList[-1]) + "\n")
    #print(response.status_code)
    #print(response.headers['content-length'])
    content_size = int(response.headers['content-length'])
    n = 1
    myDownload_path = "download\\" + counter.__str__() + ".ts"
    with open(myDownload_path,"wb") as f:
        for i in response.iter_content(chunk_size=1024):
            f.write(i)
        f.close()
    print("\r已下载[{}/{}]".format(counter,total),end='')
    counter += 1
SaveRequestsStatusListFile.close()
#=========================================================================

#============================检测文件是否全部下载完成=======================
myErrorForDownload = []
counter = 0
CheckRequestsStatusList = open("download\\RequestsStatusListFile","r")
for i in CheckRequestsStatusList.readlines():
    if not fnmatch(i, "*200*"):
        myErrorForDownload.append("playlist" + counter.__str__() + ".ts")
    counter += 1
CheckRequestsStatusList.close()
CheckRequestsStatusList = open("download\\ErrorFileList","w")
for i in myErrorForDownload:
    CheckRequestsStatusList.writelines(str(i) + "\n")
CheckRequestsStatusList.close()
#=========================================================================

#=============================重下失败文件模块=================================
for i in myErrorForDownload:
    myBuildUrl = myUrl + i
    response = requests.get(myBuildUrl,headers=headers,stream=True)
    if not response.status_code == 200:
        print("[{}]失败，请稍后再试".format(response.status_code))
        continue
    myDownload_path = "download\\" + i
    with open(myDownload_path,"wb") as f:
        for j in response.iter_content(chunk_size=1024):
            f.write(j)
        f.close()
    print("{}已下载".format(i))
#=======================若此次重下失败，则不再重下============================
