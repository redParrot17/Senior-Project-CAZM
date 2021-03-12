var reqs;
var requisites;
var studentData;



window.addEventListener("DOMContentLoaded", function () {

    $.getJSON($SCRIPT_ROOT + '/getRequisites', {

    }, function (data) {
        requisites = data;
        console.log(requisites);

    })


    $.getJSON($SCRIPT_ROOT + '/getRequirements', {
        major_name: studentData.major_name,
        major_year: studentData.major_year
    }, function (data) {
        reqs = data;
        loadStatusSheet(reqs);

    })

    let search = document.getElementById("search-button");
    console.log(search)
    search.addEventListener("click", searchClasses);
    addClassestoPools();

});
