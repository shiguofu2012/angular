var page = require("webpage").create(),
    system = require('system'),
    t, address;
if (system.args.length === 1) {
    console.log('Usage: ljljl');
    phantom.exit();
}
t = Date.now();
address = system.args[1];
page.open(address, function(status){
    if (status !== 'success'){
        console.log(status);
        console.log('Fail to load % address');
    }
    else{
        t = Date.now() - t;
        console.log(page.content);
        console.log("loding time " + t + "msec");
    }
    phantom.exit()
});
