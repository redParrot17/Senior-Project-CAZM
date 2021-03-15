var reqs;
var requisites;
var studentData;



window.addEventListener("DOMContentLoaded", function () {

    $.getJSON($SCRIPT_ROOT + '/studentData', {

    }, function (data) {
        studentData = data;

        /*$.getJSON($SCRIPT_ROOT + '/getRequirements', {
            major_name: studentData.major_name,
            major_year: studentData.major_year
        }, function (data) {
            console.log(studentData.major_name)
            console.log(studentData.major_year)
            reqs = data;
            loadStatusSheet(reqs);

        })*/

        console.log(studentData);
        // set up student schedule containers
        setUpStudentScheduleContainers(studentData);

    })

    $.getJSON($SCRIPT_ROOT + '/getRequisites', {

    }, function (data) {
        requisites = data;
        console.log(requisites);

    })

    console.log(studentData)




    let search = document.getElementById("search-button");
    console.log(search)
    search.addEventListener("click", searchClasses);
    addClassestoPools();

});
