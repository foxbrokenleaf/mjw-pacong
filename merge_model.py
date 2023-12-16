import os
#============================生成列表文件==========================
mylist = open("download\\filelist","w+",encoding="UTF-8")
for i in range(446):
    mylist.writelines("file '" + i.__str__() + ".ts'\n")    
mylist.close()
#=================================================================

#==============================合并视频模块===================================================
ffmpeg_dir_bin = "ffmpeg\\bin\\" #ffmpeg所在目录(相对路径)
out_file_name = "output\\output.mp4"    #输出文件名
list_file_name = os.getcwd() + "\download\\filelist" #列表文件所在目录（绝对路径)
os.system(ffmpeg_dir_bin + "ffmpeg -f concat -safe 0 -i " + list_file_name + " -c " + " copy " + out_file_name)    #执行指令
#==================================================================================================================