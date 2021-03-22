/**
 * @param Semesters 
 * Array of DOM elements containing each semester box
 */
let semesters = document.getElementsByClassName("scheduleContainer")

/**
 * @param pools 
 * Array of course codes contained within each Semester box
 */
var pools;

/**
 * Sets warnings on the element passed in
 * @param {String} courseID
 * ID forCourse Box that will have warnings set on it if necessary
 * @param {Boolean} showSnack 
 * `true` if the warning should include a snackbar popup
 */
function setWarnings(courseID, showSnack) {

    let courseElement = document.getElementById(courseID)
    // console.log(courseElement)
    let code = courseElement.getAttribute("coursecode");

    let semester = courseElement.getAttribute("semester");
    let year = courseElement.getAttribute("year");

    //If requisites bad, set the warning, otherwise set to no warnings
    if (!checkRequisites(code, semester, year)) {

        

        //only show snackbar if required
        if (showSnack && courseElement.parentElement.classList == "drag_container rounded border") {
            new SnackBar({
                message: "Warning: Prerequisites for " + code + " not met.",
                position: "bc",
                status: "warning"
            });
           
        }
        courseElement.parentElement.classList = "drag_container rounded border warning"

    }
    //no warnings
    else {

        courseElement.parentElement.classList = "drag_container rounded border"
    }

}



/**
 * Updates `pools` to contain the current classes
 */
function addClassestoPools() {
    pools = []
    for (let s = 0; s < semesters.length; s++) {
        let sem = []
        let classes = semesters[s].getElementsByClassName("drag_item drag_item_fill");

        //push each class to semester
        for (let c = 0; c < classes.length; c++) {
            sem.push(classes[c].id);
        }
        pools.push(sem)
    }
}



/**
 * Sets warnings for every class in pools array;
 * `addClassestoPools()` Must Be called first in order to provide accurate results
 * @param {Boolean} update 
 * Pass `false` if checking pools on page load, otherwise pass in `false`
 */
function checkPools(update) {
    for (let semester = 0; semester < pools.length; semester++) {
        let currentSemester = pools[semester];
        //check warnings for each course
        for (let course = 0; course < currentSemester.length; course++) {
            // console.log("Course " + course)
            let checkedCourse = currentSemester[course];

            //element has no warnings and has already been checked, so the the most recent change had a side effect of 
            //changing the warnings of this class -> show a snackbar
            if (update) {
                setWarnings(checkedCourse, true);
            }

            //no snackbar
            else {
                setWarnings(checkedCourse, false);

            }

        }
    }
}


/**
 * 
 * @param {String} code 
 * the course code of the class being examined
 * @param {String} semester 
 * the semester of the class being examined
 * @param {Integer} year 
 * the year of the class being examined
 * @returns {Boolean}
 */
function checkRequisites(code, semester, year) {
    var index;

    //Get code prereq dictionary
    let codeReqs = requisites[code]


    //! CHECK PREREQS
    if (codeReqs !== undefined) {
        //Get target semester #

        //Find the semester number of semesters before this class
        for (let s = 0; s < semesters.length; s++) {
            let sem = semesters[s].dataset;
            if (sem.year === year && sem.semester === semester) {
                index = s;
            }
        }

        var prereqs = codeReqs[1]

        //! Prerequisites exist
        if (prereqs !== undefined) {
            //Check Prereqs
            if (index > 0) {

                prereqs = Object.values(prereqs)
                var found = false;
                var groupNum = 0;
                while (!found && groupNum < prereqs.length) {



                    let group = prereqs[groupNum] //group of requisites (only 1 required to be completed)
                    var reqmet = true;
                    var req = 0

                    //Try group
                    while (reqmet && req < group.length) {

                        reqmet = false;
                        let compareCode = group[req]; //individual requirement in the major

                        //Check if all semesters before target semester contain the required courses
                        for (let p = 0; p < index; p++) {

                            let activePool = pools[p]; //currently checked pool
                            for (let q = 0; q < activePool.length; q++) {
                                let checkedCourse = document.getElementById(activePool[q])
                                console.log("checked course: " + checkedCourse);


                                if (checkedCourse.getAttribute("coursecode").includes(compareCode)) {
                                    reqmet = true;
                                }
                            }

                        }

                        found = reqmet;
                        req++;
                    }
                    groupNum++;
                }
                return (found);
            }

            //class in first semester has prereqs, fails by default
            else {
                return false;
            }

        }


        //TODO Check Coreqs
        //TODO Check Prohibited


    }
    //No Requisites, automatically true
    return true;
}
