window.onload = function () {
    var fileUpload = document.getElementById("fileupload");
    fileUpload.onchange = function () {
        if (typeof (FileReader) != "undefined") {
            var dvPreview = document.getElementById("dvPreview");
            dvPreview.innerHTML = "";
            var regex = /^([a-zA-Z0-9\s_\\.\-:])+(.jpg|.jpeg|.gif|.png|.bmp)$/;
            for (var i = 0; i < fileUpload.files.length; i++) {
                var file = fileUpload.files[i];
                if (regex.test(file.name.toLowerCase())) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        var img = document.createElement("IMG");
                        img.height = "200";
                        img.width = "200";
                        img.src = e.target.result;
                   //make image border radius to circle
                        img.style.borderRadius = "2%";
                   //make image class to rounded
                        img.className = "img-thumbnail";
                    //give image a margin
                        img.style.margin = "0.5rem";
                        dvPreview.appendChild(img);
                    }
                    reader.readAsDataURL(file);
                } else {
                    alert(file.name + " is not a valid image file.");
                    dvPreview.innerHTML = "";
                    return false;
                }
            }
        } else {
            alert("This browser does not support HTML5 FileReader.");
        }
    }
};