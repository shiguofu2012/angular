var page = require('webpage').create();
page.settings.userAgent = "Phantom.js bot";

link = "https://mp.weixin.qq.com/";

page.open(link, function(status){
    if(status != 'success')
    {
        console.log(status);
        phantom.exit();
    }
    else
    {
        ret = page.evaluate(function(){
            $("#account").value = "shiguofu@hust.edu.cn";
            $("#pwd").value = "5082753shi";
            $("#loginBt").click();
            return document.documentElement.innerHtml;
        });
        console.log(page.childFramesCount());
        console.log(ret);
        phantom.exit()
    }
});
