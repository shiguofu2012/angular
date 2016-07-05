
var page = require('webpage').create();
page.open('http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MjM5OTA1MDUyMA==&uin=MTI3MjcwNjMyMA%3D%3D&key=f5c31ae61525f82e9282f4ea322ef7d35a56613404252cfb758213517a424a19827a3c6d6b196f2fcf685d36d6ca7d63&devicetype=android-21&version=26031031&lang=zh_CN&nettype=WIFI&pass_ticket=kv0JjqHr3D%2FnMa8r4cUB17MyeFeNKi2w9%2BBkksO0LR0i6e4Kcu7xdWjBb9lRCZC9', function(status){
        if(status != 'fail'){
            console.log("ok");
            page.render('test.png');
        }
        phantom.exit();
        })
