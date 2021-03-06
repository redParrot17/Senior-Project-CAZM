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
 * Gets the 0-indexed position of the semester matching the parameters from the semester list
 * @param {Number} year 
 * The year of the semester
 * @param {String} semester 
 * The season of the semester i.e. "Spring" or "Winter Online"
 * @returns the semester's 0-indexed position
 */
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
    let title = getNameByCode(code);
    let warn = courseElement.children[1].children[0];

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
        courseElement.setAttribute("title", title + "\n--Missing Requisites--\n\n" + getWarningMsg(code) + getSpecialWarningMsg(code))
        warn.classList = "fas fa-exclamation-circle";
        courseElement.parentElement.classList = "drag_container rounded border warning"

    }
    else if(checkSpecial(code)){
        courseElement.parentElement.classList = "drag_container rounded border special-warning"
        courseElement.setAttribute("title", title + "\n\n" +getSpecialWarningMsg(code))
        warn.classList = "fas fa-exclamation-circle";
    }

    //no warnings
    else {

        courseElement.parentElement.classList = "drag_container rounded border";
        courseElement.setAttribute("title", title);
        warn.classList = "";
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


/**
 * Returns false if missing prereqs or coreqs, else if true
 * @param {*} code 
 * checked course code
 * @param {*} semester 
 * checked semester 
 * @param {*} year 
 * checked year
 * @returns false if warning required, else true
 */
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

        if (prereqs === undefined && coreqs === undefined){
            found = true;
        }
        return (found)


    }

    //No Requisites, automatically true
    return true;
}



/**
 * Gets sum total of credits in the schedule
 * @returns credit count
 */
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

/**
 * Gets a string containing the warnings for any available prereqs or coreqs
 * @param {String} code the code being checked for warnings needed
 * @returns warning message string, empty if no warnings needed
 */
function getWarningMsg(code) {
    let codeRequisites = requisites[code];
    if (codeRequisites !== undefined) {
        var codePrereqs = (codeRequisites[1] ? Object.values(codeRequisites[1]) : undefined);
        var codeCoreqs = (codeRequisites[2] ? Object.values(codeRequisites[2]) : undefined);
    }


    var prereqMsg = "";
    var coreqMsg = "";


    if (codePrereqs !== undefined) {
        prereqMsg += "Prerequisites:\n-------------\n";

        for (let msgGroup = 0; msgGroup < codePrereqs.length; msgGroup++) {
            if (msgGroup > 0) {
                prereqMsg += "\nOR\n\n"
            }
            let group = codePrereqs[msgGroup];
            for (let m = 0; m < group.length; m++) {
                if (m > 0) {
                    prereqMsg += "AND\n"
                }
                prereqMsg += (group[m] + "\n");
            }
        }

        if (prereqMsg !== "") {
            prereqMsg += "\n";
        }

    }

    if (codeCoreqs !== undefined) {
        prereqMsg += "Corequisites:\n-------------\n";

        for (let msgGroup = 0; msgGroup < codeCoreqs.length; msgGroup++) {
            if (msgGroup > 0) {
                coreqMsg += "\nOR\n\n"
            }
            let group = codeCoreqs[msgGroup];
            for (let m = 0; m < group.length; m++) {
                if (m > 0) {
                    coreqMsg += "AND\n";
                }
                coreqMsg += (group[m] + "\n");
            }
        }

        if (coreqMsg !== "") {
            coreqMsg += "\n";
        }

    }
    return (prereqMsg + coreqMsg);
}

/**
 * Gets a string containing the warnings for any available special messages
 * @param {String} code the code being checked for warnings needed
 * @returns warning message string, empty if no warnings needed
 */
function getSpecialWarningMsg(code) {
    let codeRequisites = requisites[code];
    if (codeRequisites !== undefined) {
        var codeSpecial = (codeRequisites[0] ? Object.values(codeRequisites[0]) : undefined);
    }

    var specialMsg = "";


    //Special
    if (codeSpecial !== undefined) {
        specialMsg += "Other Requirements:\n-------\n";

        for (let msgGroup = 0; msgGroup < codeSpecial.length; msgGroup++) {
            if (msgGroup > 0) {
                specialMsg += "AND\n"
            }
            let group = codeSpecial[msgGroup];
            for (let m = 0; m < group.length; m++) {
                if (m > 0) {
                    specialMsg += "\nOR\n\n"
                }
                specialMsg += (group[m] + "\n");
            }
        }

    }

   
    return specialMsg;
}