var reqs;
var requisites;
var studentData;



window.addEventListener("DOMContentLoaded", function () {

    $.getJSON($SCRIPT_ROOT + '/studentData', {

    }, function (data) {
        studentData = data;

        //Get requirements list for student's major
        $.getJSON($SCRIPT_ROOT + '/getRequirements', {
            major_name: studentData.major_name,
            major_year: studentData.major_year
        }, function (reqData) {

            reqs = reqData;

            loadStatusSheet(reqs);

        })

        
        // set up student schedule containers
        setUpStudentScheduleContainers(studentData);


        //Get requisite list for each course
        $.getJSON($SCRIPT_ROOT + '/getRequisites', {

        }, function (requisiteData) {
            requisites = requisiteData;
            addClassestoPools();
            console.log("Page load checking")
            checkPools(false);
    
        })

    })


    let search = document.getElementById("search-button");

    search.addEventListener("click", filterCourses);

});
