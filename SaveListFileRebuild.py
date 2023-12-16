import os
from fnmatch import fnmatch
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