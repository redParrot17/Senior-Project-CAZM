var classes;
window.addEventListener("DOMContentLoaded", function () {

    let search = document.getElementById("search-button");
    
    search.addEventListener("click", function(){
        $.getJSON($SCRIPT_ROOT + '/searchClasses', {
            class_name: $('input[id="search-bar"]').val()
         }, function(data) {
             classes = data
             console.log(classes)
             console.log("--Search Done--");
         });
    });


});

