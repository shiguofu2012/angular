function getParameter(name)
{
    var p = window.location.search;
    var index = p.indexOf(name);
    if(index != -1)
    {
        var paraEnd = p.indexOf("&", index);
        if(paraEnd == -1)
        {
            paraEnd = p.length;
        }
        var str = p.substr(index, paraEnd - 1);
        var paras = str.split("=");
        if(paras.length != 2)
        {
            return null;
        }
        return paras[1];
    }
    return null;
}

function isNull(data)
{
    if(data == null || data == "" || data == undefined)
        return true;
    else
        return false;
}
