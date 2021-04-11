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



let getTargetIndex = (year, semester) => {
   
    for (let s = 0; s < semesters.length; s++) {
        let sem = semesters[s].dataset;

        if (sem.year == year && sem.semester.toUpperCase() == semester.toUpperCase()) {
            var index = s;

        }
    }

    return index;
}


/**
 * Sets warnings on the element passed in
 * @param {String} courseID
 * ID forCourse Box that will have warnings set on it if necessary
 * @param {Boolean} showSnack 
 * `true` if the warning should include a snackbar popup
 */
function setWarnings(courseID, showSnack) {

    let courseElement = document.getElementById(courseID)
    let code = courseElement.getAttribute("coursecode");

    let semester = courseElement.getAttribute("semester");
    let year = courseElement.getAttribute("year");
    

    //If requisites bad, set the warning, otherwise set to no warnings
    if (!checkRequisites(code, semester, year)) {


        //only show snackbar if required
        if (showSnack && courseElement.parentElement.classList == "drag_container rounded border") {
            new SnackBar({
                message: "Warning: Prerequisites or Corequisites for " + code + " not met.",
                position: "bc",
                timeout: 10000,
                status: "warning",
                width: "100%"
            });

        }
        courseElement.parentElement.classList = "drag_container rounded border warning"

    }
    else if(checkSpecial(code)){
        courseElement.parentElement.classList = "drag_container rounded border special-warning"
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
 * @returns {Boolean} Requisites met
 */
function checkSpecial(code) {

    //Get code prereq dictionary
    let codeReqs = requisites[code]

    if (codeReqs !== undefined) {
        var special = codeReqs[0]
    }

    //special requisite exists
    if(special !== undefined){
        return true
    }

    //special requisite does not exist
    return false
    
}



function checkRequisites(code, semester, year) {

    //Get code prereq dictionary
    let codeReqs = requisites[code]

    //! CHECK PREREQS
    if (codeReqs !== undefined) {

        //Get target semester #
        //Find the semester number of semesters before this class

        let targetindex = getTargetIndex(year, semester);
        var prereqs = codeReqs[1]
        var coreqs = codeReqs[2]



        //TODO handle prohibited courses correctly
        // var prohibited = codeReqs[4]
        var found = false;



        //! Corequisites exist
        if (coreqs !== undefined) {

            //Check Coreqs
            coreqs = Object.values(coreqs)

            var groupNum = 0;

            //Check each group until one of them is met
            while (!found && groupNum < coreqs.length) {



                let group = coreqs[groupNum] //group of requisites (only 1 required to be completed)

                var reqmet = true;
                var req = 0

                //Try group
                while (reqmet && req < group.length) {

                    reqmet = false;
                    let compareCode = group[req]; //individual requirement in the major

                    //Check if all semesters up to target semester contain the required courses
                    for (let p = 0; p <= targetindex; p++) {

                        let activePool = pools[p]; //currently checked pool

                        for (let q = 0; q < activePool.length; q++) {
                            let checkedCourse = document.getElementById(activePool[q])
                            if (checkedCourse.getAttribute("coursecode").includes(compareCode)) {
                                reqmet = true;
                            }
                        }

                    }

                    found = reqmet;

                    req++;
                }//done with group
                groupNum++;
            }//next group

        }


        //! Prerequisites exist
        if (!found && prereqs !== undefined) {
            //Check Prereqs
            if (targetindex > 0) {

                prereqs = Object.values(prereqs)

                var groupNum = 0;

                //Check each group until one of them is met
                while (!found && groupNum < prereqs.length) {



                    let group = prereqs[groupNum] //group of requisites (only 1 required to be completed)
                    var reqmet = true;
                    var req = 0

                    //Try group
                    while (reqmet && req < group.length) {

                        reqmet = false;
                        let compareCode = group[req]; //individual requirement in the major

                        //Check if all semesters before target semester contain the required courses
                        for (let p = 0; p < targetindex; p++) {

                            let activePool = pools[p]; //currently checked pool
                            for (let q = 0; q < activePool.length; q++) {
                                let checkedCourse = document.getElementById(activePool[q])

                                if (checkedCourse.getAttribute("coursecode").includes(compareCode)) {
                                    reqmet = true;

                                }
                            }

                        }

                        found = reqmet;
                        req++;
                    }//done with group
                    groupNum++;
                }//next group

            }

            //class in first semester has prereqs, fails by default
            else {
                return false;
            }

        }
        return (found)

        //TODO Check Prohibited


    }

    //No Requisites, automatically true
    return true;
}




let totalCreds = () => {
    var credits = 0;
    let credindex = getTargetIndex(curSemester.year, curSemester.semester);
    for (let sem = 0; sem <= credindex; sem++) {
        let pool = pools[sem];
        for (let course in pool) {
            let code = pool[course].split("-")[0];

            credits += getCreditsForSum(code);
        }
    }
    return credits;
}

