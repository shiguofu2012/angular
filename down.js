

var page = require('webpage').create(),
    fs = require("fs");
//page.settings.userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36";
system = require('system');
page.viewportSize = {width: 480, height: 1000}
//page.settings.loadImages = false;
link = system.args[1];
phantom.onError = function(msg, trace){
    var magStack = ['phantom error: ' + msg];
    if(trace && trace.length)
    {
        msgStack.push('trace:');
        trace.forEach(function(t){
            msgStack.push('->' + (t.file || t.sourceURL) + ':' + t.line + (t.function ? ' (in function ' + t.function +')' : ''));
        });
    }
};

page.open(link, function(status){
    if(status != 'success'){
        console.log("failed");
        phantom.exit();
    }
    else{
        //f = fs.open("weixin.html", "w");
        //f.write(page.content);
        //f.close();
        //page.evaluate(function(){
        //    var pos = 0;
        //    function scroll()
        //    {
        //        pos += 10000;
        //        window.document.body.scrollTop = pos;
        //        window.setTimeout(scroll, 100);
        //    };
        //    scroll();
        //    return window.document.body.scrollTop;
        //}).then(function(h){console.log(h);page.set('scrollHeight', {top: h, left: 0})});
        var i = 0,
            top,
            get_height = function(){
            return document.body.scrollHeight;
        };
        setInterval(function(){
            top = page.evaluate(get_height); 
            i++;
            page.scrollPosition = {top: top + 1, left: 0};
            if(i >= 5){
                console.log(page.content);
                phantom.exit();
            }
        }, 300);
    }
});

//window.setTimeout(function(){
//    page.render("a.png");
//    //console.log(page.content);
//    phantom.exit();
//}, 10000);
