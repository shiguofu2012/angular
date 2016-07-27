var page = require("webpage").create(),
    system = require('system'),
    fs = require('fs'),
    t, address;
if (system.args.length === 1) {
    console.log('Usage: ljljl');
    phantom.exit();
}
t = Date.now();
address = system.args[1];
page.viewportSize = {width: 1024, height: 100000};
page.open(address, function(status){
    if (status !== 'success'){
        console.log(status);
        console.log('Fail to load % address');
    }
    else{
        t = Date.now() - t;
        page.render("a.png");
        var f = fs.open("baidu.html", "w");
        f.write(page.content);
        f.close();
        console.log("loding time " + t + "msec");
    }
    phantom.exit()
});
