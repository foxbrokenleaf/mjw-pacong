import os
import requests
from fnmatch import fnmatch
class myMJW:
    __myDefine_WebLink = []
    __myGetencode = []
    __myGetuploaddate = []
    __myExpires = []
    __myCounter_URL = 0
    __headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    __read_url_for_file = []
    #==========Data========
    def __init__( self ):
        pass
    def __del__( self ):
        pass
    def BuildExpires( self ):
        DownloadPlaylist_FileList_Path = "DownloadPlaylist\\"
        with open("Download_list.txt",'r') as f:
            self.__read_url_for_file = f.readlines()
            for i in self.__read_url_for_file:
                self.__myCounter_URL += 1 #链接个数记录
                i = i.replace('\n','')
                self.__myExpires.append(i[i.find("&expires=",0,-1) + 9 : -1])   #记录链接Expires
                self.__myDefine_WebLink.append(i[0 : i.find(".com",0,-1) + 5])  #记录链接的网页
                self.__myGetuploaddate.append(i[i.find(".com",0,-1) + 5 : i.find(".com",0,-1) + 14])    #记录链接的资源上传日期
                self.__myGetencode.append(i[i.find(".com",0,-1) + 15 : i.find("playlist",0,-1) - 1])     #记录链接的密匙
                with open("DownloadPlaylist\\" + self.__myExpires[-1],'w') as SaveListFile:    #接收playlist
                    print(i)
                    res = requests.get(i,headers=self.__headers)
                    print(res.status_code)
                    for j in res.iter_content(chunk_size=1024):
                        SaveListFile.writelines(str(j))
                    SaveListFile.close()
        DownloadPlaylist_FileList = os.listdir(DownloadPlaylist_FileList_Path)      #重组playlist
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
    #重组链接------------------>组成完整的链接
    def BuildDownloadURL( self ):
        Now_counter_url = 0
        DownloadPlaylist_FileList_Path = "DownloadPlaylist\\"
        DownloadPlaylist_FileList = os.listdir(DownloadPlaylist_FileList_Path)
        for loop_counter in DownloadPlaylist_FileList:
            myFile = open(DownloadPlaylist_FileList_Path + loop_counter,"r",encoding="UTF-8")
            counter = 0
            for i in myFile.readlines():
                if fnmatch(i,"playlist*"):
                    counter += 1
            myFile.close()
            #print(self.__myDefine_WebLink[Now_counter_url])
            #print(self.__myGetuploaddate[Now_counter_url])
            #print(self.__myGetencode[Now_counter_url])
            myUrl = self.__myDefine_WebLink[Now_counter_url] + self.__myGetuploaddate[Now_counter_url] + "/" + self.__myGetencode[Now_counter_url]
            file_name = ".ts"
            myDefine_file = []
            for i in range(counter):
                myBuildUrl = myUrl + "/playlist" + i.__str__() + file_name
                myDefine_file.append(myBuildUrl)
            with open(DownloadPlaylist_FileList_Path + loop_counter,"w",encoding="UTF-8") as myFile:
                for i in myDefine_file:
                    myFile.writelines(i + '\n')
                myFile.close()
            Now_counter_url += 1
    #
    def FileDownload( self ):
        DownloadPlaylist_FileList_Path = "DownloadPlaylist\\"
        myRequestsStatusList = []
        total = []   #当前链接要下载的ts视频的总数
        counter_for_filed = 0
        DownloadPlaylist_FileList = os.listdir(DownloadPlaylist_FileList_Path)
        for i in DownloadPlaylist_FileList:
            os.mkdir("download\\" + counter_for_filed.__str__())    #创建对应序列下载目录
            SaveRequestsStatusListFile = open("download\\" + counter_for_filed.__str__() + '\\' +"RequestsStatusListFile","w")  #保存下载的每一个文件的状态码以后续检查是否下载完全
            with open(DownloadPlaylist_FileList_Path + i,'r') as f:
                myDefine_file = f.readlines()
                f.close()
                temp_counter = 0
                for temp in myDefine_file:
                    myDefine_file[temp_counter] = temp.replace('\n','')
                    temp_counter += 1
                total.append(temp_counter)
                del temp_counter
            counter = 0
            for j in myDefine_file:
                response = requests.get(j,headers=self.__headers,stream=True)
                myRequestsStatusList.append([response.status_code,"playlist" + counter.__str__()])
                SaveRequestsStatusListFile.writelines(str(myRequestsStatusList[-1]) + "\n")
                #print(response.status_code)
                #print(response.headers['content-length'])
                #content_size = int(response.headers['content-length'])
                myDownload_path = "download\\" + counter_for_filed.__str__() + '\\' + counter.__str__() + ".ts"
                with open(myDownload_path,"wb") as f:
                    for i in response.iter_content(chunk_size=1024):
                        f.write(i)
                    f.close()
                print("\rURL [{}] ".format(j) + "已下载 [{}/{}] ".format(counter,total[counter_for_filed]) + "状态码 [{}]".format(response.status_code),end="")
                counter += 1
            counter_for_filed += 1
            SaveRequestsStatusListFile.close()
    #
    def CheckFileDownloadCompelete( self ):
        pass
    def ReDownloadFile( self ):
        pass
    def BuildFfmpegListFile( self ):
        DownloadPlaylist_FileList_Path = "DownloadPlaylist\\"
        for i in range(self.__myCounter_URL):
            counter = 0
            with open(DownloadPlaylist_FileList_Path + self.__myExpires[i],'r') as f:
                for temp in f.readlines():
                    if temp[-1] == '\n':
                        counter += 1
                f.close()
            mylist = open("download\\" + i.__str__() + '\\' + "filelist","w+",encoding="UTF-8")
            for j in range(counter):
                mylist.writelines("file '" + j.__str__() + ".ts'\n")
            mylist.close()
    def MakeCompeleteVideo( self ):
        ffmpeg_dir_bin = "ffmpeg\\bin\\" #ffmpeg所在目录(相对路径)
        for i in range(self.__myCounter_URL):
            out_file_name = "output\\" + i.__str__() + ".mp4"    #输出文件名b
            list_file_name = os.getcwd() + "\download\\" + i.__str__() + '\\' + "filelist" #列表文件所在目录（绝对路径)
            os.system(ffmpeg_dir_bin + "ffmpeg -f concat -safe 0 -i " + list_file_name + " -c " + " copy " + out_file_name)    #执行指令
    #
    def BuildFolder( self ):
        os.mkdir("download")
        os.mkdir("DownloadPlaylist")
        pass
    #remove download\\*
    #remove DownloadPlaylist\\*
    def RemoveFolder( self ):
        file_list_download = os.listdir("download\\")
        file_list_downloadplaylist = os.listdir("DownloadPlaylist\\")
        for i in file_list_downloadplaylist:
            os.remove("DownloadPlaylist\\" + i)
        for i in file_list_download:
            file_list_download_i = os.listdir("download\\" + i)
            for j in file_list_download_i:
                os.remove("download\\" + i + '\\' + j)
            os.rmdir("download\\" + i)
        os.rmdir("download")
        os.rmdir("DownloadPlaylist")
    #auto
    def start( self ):
        self.BuildFolder()
        self.BuildExpires()
        self.BuildDownloadURL()
        self.FileDownload()
        self.BuildFfmpegListFile()
        self.MakeCompeleteVideo()
        self.RemoveFolder()
        pass
a = myMJW()
a.start()