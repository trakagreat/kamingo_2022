console.log("hello")
const spinner = document.getElementById("spinner-box")
const list = document.getElementById("list")

$.ajax({
    type:'GET',
    url:'/service',
    success: function(response){

        setTimeout(() => {
        spinner.classList.add('no-display')
        console.log("{{filter}}");
        
        list.classList.remove('no-display')

         console.log(list.innerHTML);
        }, 400);
        
    },
    error: function(error){
        console.log("error");
    },
})