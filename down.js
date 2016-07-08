

var page = require('webpage').create(),
    fs = require("fs");
page.settings.userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36";
system = require('system');

link = system.args[1];

page.open(link, function(status){
    if(status != 'success'){
        console.log("failed");
    }
    else{
        f = fs.open("weixin.html", "w+");
        f.write(page.content);
        f.close();
        page.render("a.png");
    }
    phantom.exit();
})
