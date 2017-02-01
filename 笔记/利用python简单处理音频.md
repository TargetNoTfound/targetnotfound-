#利用python简单处理音频
整理自<http://appleu0.sinaapp.com/?p=588>
##环境准备
###1.pydub
>所以就发现了一个python库：pydub，用来处理音频，比如说MP3啊、wav之类的东西是很方便的。
我们还知道有另一个有名的软件，Adobe Audition。Au功能自然是很多，不过我们用python啊之类的，是可以达到更加批量化的效果，而且没有那么高的学习成本，如果之前有python的一些基础，直接就能方便的操纵音频了。当然了，功能是肯定要比Au少的就是了。

	pip install pydub


[官网](http://pydub.com/)

###2.ffmpeg
>安装完pydub之后，就可以处理一些wav格式的音频文件，但是这个并不是我们最常用的，我们可能比较常用的还是mp3啊、MP4等等格式的。
这个时候，还需要安装ffmpeg，这个是一个命令行工具，可以用于一些音频格式的转换，比如mp3转wav啊之类的，然后就可以处理其他类型的多媒体文件了。

[官网](https://ffmpeg.org/)

[windows下的安装指南](http://zh.wikihow.com/%E5%9C%A8Windows%E4%B8%8A%E5%AE%89%E8%A3%85FFmpeg%E7%A8%8B%E5%BA%8F)

##使用说明
请参考[pydub官网](http://pydub.com/)



