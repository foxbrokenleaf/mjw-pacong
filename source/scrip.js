var art = new Artplayer({
    container: '.artplayer-app',
    url: 'https://cdn8.tvtvgood.com/202204/14/cd92a8ae03d0/playlist.m3u8?token=YKl_2bA8IdnYALa281Lj0A&expires=1702390443',
    poster:'https://wework.qpic.cn/wwpic/477300__CdsT_MFTNKfeCz_1684174507/0',
    setting: true,
    screenshot: true,
    autoplay: true,
    autoOrientation: true,
    hotkey: true,
    pip: true,
    quality: [{"default":true,"html":"\u7ebf\u8def1","url":"https:\/\/cdn8.tvtvgood.com\/202204\/14\/cd92a8ae03d0\/playlist.m3u8?token=YKl_2bA8IdnYALa281Lj0A&expires=1702390443"},{"default":false,"html":"\u7ebf\u8def2","url":"https:\/\/cdn4.yzzy-online.com\/20220527\/12469_3d95c069\/index.m3u8"},{"default":false,"html":"\u7ebf\u8def3","url":"https:\/\/s1.fsvod1.com\/20220314\/YJdRaeAH\/index.m3u8"}],
    flip: true,
    playbackRate: true,
    aspectRatio: true,
    fullscreen: true,
    fastForward: true,
    miniProgressBar: true,
    autoMini: true,
    theme: '#23ade5',
    icons: {
        loading: '<img src="./static/img/ploading.gif">',
        state: '<img width="150" heigth="150" src="./static/img/state.svg">',
        indicator: '<img width="16" heigth="16" src="./static/img/indicator.svg">',
    },
    
    customType: {
        m3u8: function playM3u8(video, url, art) {
            if (Hls.isSupported()) {
                if (art.hls) art.hls.destroy();
                const hls = new Hls();
                hls.loadSource(url);
                hls.attachMedia(video);
                art.hls = hls;
                art.on('destroy', () => hls.destroy());
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = url;
            } else {
                art.notice.show = 'Unsupported playback format: m3u8';
            }
        }
    },
});
// 获取视频的URL和当前时间
var videoId = 'CMzE4ODZfMGp1aGU=';
var currentTime = '';
var duration = '';
var nextepisode = '';
if(nextepisode!="")
{
    //console.log('不为空');
    //next(nextepisode);
}
var i=0;
setInterval(function() 
{
    if(art.duration==0)
    {
        i++;
    }
    if(i>10)
    {

        art.notice.show = '播放失败请切换线路！';
    }
    console.info(i);
}, 1000);
// 在页面加载时从本地存储中恢复视频播放位置
if (localStorage.getItem(videoId)) 
{
    art.on('ready', () => {
        art.notice.show = '请勿相信视频内广告!!!';
        //console.info(localStorage.getItem(videoId));
        art.currentTime = localStorage.getItem(videoId);
        duration = art.duration;
    });
}

// 每5秒钟更新一次本地存储中的播放位置信息
setInterval(function() 
{
    //console.log(parseInt(art.currentTime));
    if(parseInt(art.currentTime) !== parseInt(duration))
    {
        //console.info(art.currentTime);
        localStorage.setItem(videoId, art.currentTime);
    }
}, 5000);

// 在视频结束后清除本地存储中的播放位置信息
art.on('video:ended', function() 
{
    if (!removeExistingItem(videoId))
        console.log("Error");
});
function removeExistingItem(key) 
{
    if (localStorage.getItem(key) === null)
        return false;
    localStorage.removeItem(key);
    return true;
}
function next(nexturl){
    $('.art-control-playAndPause').after('<div class="art-control art-control-next" data-index="10"><i class="art-icon art-icon-next hint--rounded hint--top" aria-label="下一集" style="display: flex;"><svg xmlns="http://www.w3.org/2000/svg" height="22" width="22"><path d="M16 5a1 1 0 00-1 1v4.615a1.431 1.431 0 00-.615-.829L7.21 5.23A1.439 1.439 0 005 6.445v9.11a1.44 1.44 0 002.21 1.215l7.175-4.555a1.436 1.436 0 00.616-.828V16a1 1 0 002 0V6C17 5.448 16.552 5 16 5z"></path></svg></i></div>');
    $(".art-control-next").on("click", function() 
    {
        top.location.href=nexturl;
    });
}
art.on('error', (error, reconnectTime) => {
    console.info(error, reconnectTime);
});