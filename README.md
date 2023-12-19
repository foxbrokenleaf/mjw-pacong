2023/12/20/00:22
[BUG] 最多只能下6个
        描述：在DownloadPlaylist中只生成了6个文件
            在download中只生成了6个文件夹
        推测：内存空间不足？
        尝试解决方案：1、读取一条URL就生成一个DownloadPlaylist，生成一个download中的文件夹，下载一条URL,完成后再读取URL
                        再生成一个DownloadPlaylist,再生成一个download中的文件夹，再下载一条URL。
                    2、