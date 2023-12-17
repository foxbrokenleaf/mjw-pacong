class myMJW:
    __myDefine_WebLink = ""
    __myGetencode = ""
    __myGetuploaddate = ""
    __myExpires = ""
    __headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    __DownloadPlaylist_FileList_Path = ""
    __read_url_for_file = []
    #==========Data========
    def __init__( self ):
        self.__DownloadPlaylist_FileList_Path = "DownloadPlaylist\\"
    def __del__( self ):
    
    def BuildExpires( self ):
        with open("Download_list.txt",'r') as f:
            self.__read_url_for_file = f.readlines()
            for i in self.__read_url_for_file:
                i = i.replace('\n','')
                self.__myExpires.append(i[i.find("&expires=",0,-1) + 9 : -1])
                self.__myDefine_WebLink.append(i[0 : i.find(".com",0,-1) + 5])
                self.__myGetuploaddate
    def BuildDownloadURL( self ):

    def FileDownload( self ):
        
    def CheckFileDownloadCompelete( self ):

    def ReDownloadFile( self ):
        
    def BuildFfmpegListFile( self ):
        
    def MakeCompeleteVideo( self ):
