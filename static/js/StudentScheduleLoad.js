var reqs;
var requisites;
var studentData;



window.addEventListener("DOMContentLoaded", function () {

    $.getJSON($SCRIPT_ROOT + '/studentData', {

    }, function (data) {
        studentData = data;

        $.getJSON($SCRIPT_ROOT + '/getRequirements', {
            major_name: studentData.major_name,
            major_year: studentData.major_year
        }, function (reqData) {

            reqs = reqData;
            console.log(reqs)
            loadStatusSheet(reqs);

        })

        // console.log(studentData);
        // set up student schedule containers
        setUpStudentScheduleContainers(studentData);


        $.getJSON($SCRIPT_ROOT + '/getRequisites', {

        }, function (requisiteData) {
            requisites = requisiteData;
            addClassestoPools();
            // console.log(requisites);
    
        })

    })

   

    // console.log(studentData)




    let search = document.getElementById("search-button");

    search.addEventListener("click", filterCourses);

});
