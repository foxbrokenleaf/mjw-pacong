#第一集https://cdn3.tvtvgood.com/202204/21/ca80a3c9992c/playlist.m3u8?token=VT4orQyJjwdXU97xtMx67Q&expires=1702647946
#第二集https://cdn3.tvtvgood.com/202204/21/e913a9d4c28d/playlist.m3u8?token=dXG6BlzthTnVtGxnz5p8gw&expires=1702648428
#Build to be like     
#myDefine_WebLink = "https://cdn8.tvtvgood.com/"
#myGetencode = "cd92a8ae03d0"
#myGetuploaddate = "202204/14"
#myExpires = "1702648428"
#下载playlist.m3u8文件并保存为mySign中的名字
#从文件中读取
import requests
import os
from fnmatch import fnmatch
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
with open("Download_list.txt",'r') as f:
    read_url_for_file_temp = f.readlines()
    for i in read_url_for_file_temp:
        i = i.replace('\n','')
        myExpires = i[i.find("&expires=",0,-1) + 9 : -1]
        myDefine_WebLink = i[0 : i.find(".com",0,-1) + 5]
        myGetuploaddate = i[i.find(".com",0,-1) + 5 : i.find(".com",0,-1) + 15]
        myGetencode = i[i.find(".com",0,-1) + 15 : i.find("playlist",0,-1) - 1]
        with open("DownloadPlaylist\\" + myExpires,'w') as SaveListFile:
            print(i)
            res = requests.get(i,headers=headers)
            print(res.status_code)
            for j in res.iter_content(chunk_size=1024):
                SaveListFile.writelines(str(j))
            SaveListFile.close()
#========================================================
DownloadPlaylist_FileList = os.listdir("DownloadPlaylist\\")
for i in DownloadPlaylist_FileList:
    File_Source = ""
    with open("DownloadPlaylist\\" + i,"r") as f:
        File_Source = f.readlines()
        f.close()
    with open("DownloadPlaylist\\" + i,"w") as SaveListFile:
        for j in File_Source:
            j = j.split("\\n")
            for a in j:
                if fnmatch(a,"playlist*"):
                    a += '\n'
                    SaveListFile.writelines(a)
        SaveListFile.close()
#===================================================================