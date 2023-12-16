from fnmatch import fnmatch
import requests
import os

#==================数据区（全局）=============================
myDefine_WebLink = ""
myGetencode = ""
myGetuploaddate = ""
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
DownloadPlaylist_FileList_Path = "DownloadPlaylist\\"
#===========================================================

#第一集https://cdn3.tvtvgood.com/202204/21/ca80a3c9992c/playlist.m3u8?token=VT4orQyJjwdXU97xtMx67Q&expires=1702647946
#第二集https://cdn3.tvtvgood.com/202204/21/e913a9d4c28d/playlist.m3u8?token=dXG6BlzthTnVtGxnz5p8gw&expires=1702648428
#Build to be like     
#myDefine_WebLink = "https://cdn8.tvtvgood.com/"
#myGetencode = "cd92a8ae03d0"
#myGetuploaddate = "202204/14"
#myExpires = "1702648428"
#下载playlist.m3u8文件并保存为mySign中的名字
#从文件中读取
#============================================================
with open("Download_list.txt",'r') as f:
    read_url_for_file_temp = f.readlines()
    for i in read_url_for_file_temp:
        i = i.replace('\n','')
        myExpires = i[i.find("&expires=",0,-1) + 9 : -1]
        myDefine_WebLink = i[0 : i.find(".com",0,-1) + 5]
        myGetuploaddate = i[i.find(".com",0,-1) + 5 : i.find(".com",0,-1) + 14]
        myGetencode = i[i.find(".com",0,-1) + 15 : i.find("playlist",0,-1) - 1]
        with open("DownloadPlaylist\\" + myExpires,'w') as SaveListFile:
            print(i)
            res = requests.get(i,headers=headers)
            print(res.status_code)
            for j in res.iter_content(chunk_size=1024):
                SaveListFile.writelines(str(j))
            SaveListFile.close()
#========================================================
DownloadPlaylist_FileList = os.listdir(DownloadPlaylist_FileList_Path)
for i in DownloadPlaylist_FileList:
    File_Source = ""
    with open(DownloadPlaylist_FileList_Path + i,"r") as f:
        File_Source = f.readlines()
        f.close()
    with open(DownloadPlaylist_FileList_Path + i,"w") as SaveListFile:
        for j in File_Source:
            j = j.split("\\n")
            for a in j:
                if fnmatch(a,"playlist*"):
                    a += '\n'
                    SaveListFile.writelines(a)
        SaveListFile.close()
#===================================================================

#=========================下载链接组成模块====================================
DownloadPlaylist_FileList = os.listdir(DownloadPlaylist_FileList_Path)
for loop_counter in DownloadPlaylist_FileList:
    myFile = open(DownloadPlaylist_FileList_Path + myExpires,"r",encoding="UTF-8")
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
        #content_size = int(response.headers['content-length'])
        n = 1
        myDownload_path = "download\\" + counter.__str__() + ".ts"
        with open(myDownload_path,"wb") as f:
            for i in response.iter_content(chunk_size=1024):
                f.write(i)
            f.close()
        print("\rURL [{}] ".format(j) + "已下载 [{}/{}] ".format(counter,total) + "状态码 [{}]".format(response.status_code),end="")
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

    #============================生成列表文件==========================
    mylist = open("download\\filelist","w+",encoding="UTF-8")
    for i in range(counter):
        mylist.writelines("file '" + i.__str__() + ".ts'\n")    
    mylist.close()
    #=================================================================

    #==============================合并视频模块===================================================
    ffmpeg_dir_bin = "ffmpeg\\bin\\" #ffmpeg所在目录(相对路径)
    out_file_name = "output\\" + loop_counter + ".mp4"    #输出文件名b
    list_file_name = os.getcwd() + "\download\\filelist" #列表文件所在目录（绝对路径)
    os.system(ffmpeg_dir_bin + "ffmpeg -f concat -safe 0 -i " + list_file_name + " -c " + " copy " + out_file_name)    #执行指令
    #==================================================================================================================
    path_file = "download\\"
    download_file_list = os.listdir(path=path_file)
    for i in download_file_list:
        os.remove(path=path_file + i)
        print("已删除[{}]".format(path_file + i))
    path_file = "DownloadPlaylist\\"
    download_file_list = os.listdir(path=path_file)
    for i in download_file_list:
        os.remove(path=path_file + i)