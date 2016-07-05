

var page = require('webpage').create()

system = require('system')

link = system.args[1];

page.open(link, function(status){
    if(status != 'success'){
        console.log("failed");
    }
    else{
        console.log(page.content);
    }
    phantom.exit();
})
