let semesters = document.getElementsByClassName("scheduleContainer")
var pools;


function setWarnings(code, semester, year, element){
    if(!checkRequisites(code, semester, year)){

        
        element.parentElement.style.backgroundColor = "#ff9800";
        new SnackBar({
                    message: "Warning: Prerequisites for " + code + " not met.",
                    position: "bc",
                    status: "warning"
                });

    }
    else{
        element.parentElement.style.backgroundColor = ""
    }

}

function addClassestoPools() {
    pools = []
    for (let s = 0; s < semesters.length; s++) {
        let sem = []
        let classes = semesters[s].getElementsByClassName("drag_item drag_item_fill")
        for (let c = 0; c < classes.length; c++) {
            sem.push(classes[c].id)
            setWarnings(classes[c].getAttribute("coursecode"), semesters[s].dataset.semester, semesters[s].dataset.year, classes[c])
        }
        pools.push(sem)
    }
}

function checkRequisites(code, semester, year) {
    var index;
    //Get code prereq dict
    let codeReqs = requisites[code]


    //! CHECK PREREQS
    if (codeReqs !== undefined) {
        //Get target semester #


        for (let s = 0; s < semesters.length; s++) {

            if (semesters[s].dataset.year === year && semesters[s].dataset.semester === semester) {

                index = s

            }
        }

        var prereqs = codeReqs[1]
        if (prereqs !== undefined) {
            prereqs = Object.values(prereqs)


            var found = false;
            var groupNum = 0;
            while (!found && groupNum < prereqs.length) {



                let group = prereqs[groupNum]

                var reqmet = true;
                var req = 0

                //Try group
                while (reqmet && req < group.length) {

                    reqmet = false;

                    let compareCode = group[req];
                    for (let p = 0; p < index; p++) {
                        for(i in pools[p]){
                            let e = document.getElementById(pools[p][i])
                            if (e.getAttribute("coursecode").includes(compareCode)) {
                                reqmet = true
                            }
                        }


                    }

                    found = reqmet;
                    req++
                }
                groupNum++;
            }


            return (found)
        }


        //TODO Check Coreqs
        //TODO Check Prohibited


    }
    //No Requisites, automatically true
    return true;
}
