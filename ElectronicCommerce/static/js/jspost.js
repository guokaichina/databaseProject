function jsPost(url, params, fileParams={}){
    let temp_form = document.createElement("form");
    temp_form.action = url;
    temp_form.enctype ="multipart/form-data";
    temp_form.method = "post";
    temp_form.style.display = "none";
    for (let x in params) {
        let opt = document.createElement("textarea");
        opt.name = x;
        opt.value = params[x];
        temp_form .appendChild(opt);
    }
    for (let x in fileParams){
        let opt = document.createElement("input")
        opt.type = "file";
        opt.name = "x";
        opt.value = fileParams[x];
        temp_form.appendChild(opt);
    }
    document.body.appendChild(temp_form);
    temp_form.submit();
}