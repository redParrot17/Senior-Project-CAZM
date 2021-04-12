

let ALL_SEMESTERS = ["January", "Spring", "May", "Early Summer","Late Summer", "Fall", "Winter Online"];
let invalidCombos = [];
// var studentData


function getNameByCode(code) {

	var returnedName = "N/A";

	let found = false;
	var courseIndex = 0;

	while (!found && courseIndex < listOfCourses.length) {
		let searchedCourse = allCourses[courseIndex];


		if (searchedCourse.courseCode === code) {
			found = true;

			returnedName = searchedCourse.name;
		}
		courseIndex++;
	}


	return returnedName;
}




function addClassHolder(semester, year, semesterOrder, courses, counter) {
  let classHolder =  document.getElementById("main-schedule");
	let holderContents = ``;
	let creditCount = 0;
	//console.log(semester);
	if(semester == "Winter Online" || semester == "January" || semester == "May" || semester == "Early Summer" || semester == "Late Summer"){
		//for loop through all the student's courses_to_add
		  courses.forEach((course, index) => {
		    holderContents += `<div class="col-6 drag_box">
		            <div class="drag_container rounded border" ondrop="drop(event)" ondragover="allowDrop(event)">
									<div id="${course.course_code}-${course.semester}-${course.year}" coursecode="${course.course_code}" year="${course.year}" semester="${course.semester}" class="drag_item drag_item_fill" draggable="true" ondragstart="set_valid_drag_locations(event);drag(event);" ondragend="revert_drag_locations(event);dragEnd(event);" data-toggle="tooltip" title="${getNameByCode(course.course_code)}">
			              <i class="col-1 pr-0 pl-0 ml-2 fas fa-arrows-alt" aria-hidden="true"></i>
			              <span class="col pr-0 pl-0 drag_item_text text-center">${course.course_code}
						  	<i aria-hidden="true"></i> 
						  </span>
			              <i class="col-1 pr-0 pl-0 fas fa-trash-alt mr-2 trashRed" onclick="removeDragItem(event)" aria-hidden="true"></i>
		            </div>
							</div>
		        </div>`
		      });
		holderContents = `
	  <fieldset class="container scheduleContainer rounded itemInvisible" data-semester="${semester}" data-year="${year}" data-order="${semesterOrder}">
	    <legend class = "mb-0"> ${semester} ${year}</legend>
				<div class = "row">
					<h6 class = "pl-3" id = "${semester}-${year}-credits"> Scheduled Credits: ${creditCount} </h6>
				</div>
	      <div class="row rounded mb-2 drag_box_container mt-0" id="${semester}-${year}">` + holderContents;



	    holderContents += `
	        <div class="col-6 drag_box">
	            <div class="drag_container rounded" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
	        </div>
	    </div>
	  </fieldset>`;
	}
	else{
		//for loop through all the student's courses_to_add
		  courses.forEach((course, index) => {
				creditCount += getCreditsForSum(course.course_code);

		    holderContents += `<div class="col-6 drag_box">
		            <div class="drag_container rounded border" ondrop="drop(event)" ondragover="allowDrop(event)">
									<div id="${course.course_code}-${course.semester}-${course.year}" coursecode="${course.course_code}" year="${course.year}" semester="${course.semester}" class="drag_item drag_item_fill" draggable="true" ondragstart="set_valid_drag_locations(event);drag(event);" ondragend="revert_drag_locations(event);dragEnd(event);" data-toggle="tooltip" title="${getNameByCode(course.course_code)}">
			              <i class="col-1 pr-0 pl-0 ml-2 fas fa-arrows-alt" aria-hidden="true"></i>
			              <span class="col pr-0 pl-0 drag_item_text text-center">${course.course_code}
						  	<i aria-hidden="true"></i> 
						  </span>
			              <i class="col-1 pr-0 pl-0 fas fa-trash-alt mr-2 trashRed" onclick="removeDragItem(event)" aria-hidden="true"></i>
			            </div>
								</div>
		        </div>`
		      });
			if(counter == 0){

				if(creditCount >17){
					holderContents = `
				  <fieldset data-title="Semester Block" data-step='3' data-intro = "This is a semester block. You can drag the courses from the side bar into these boxes where there is a dotted outline. You can also drag courses from semester to semester and delete them from your schedule all together by clicking the trash icon. NOTE: if a semester block is greyed out when you are dragging a course that means it is not available in that semester" class="container scheduleContainer rounded" data-semester="${semester}" data-year="${year}" data-order="${semesterOrder}">
				    <legend class = "mb-0"> ${semester} ${year}</legend>
							<div class = "row">
								<h6 class = "pl-3" id = "${semester}-${year}-credits"> <i data-toggle="tooltip" title="Credit Count High: There will be an added fee" class="fas fa-exclamation-triangle"></i> Scheduled Credits: ${creditCount} </h6>
							</div>
				      <div class="row rounded mb-2 drag_box_container mt-0" id="${semester}-${year}">` + holderContents;
				}
				else if(creditCount < 12 ){
					holderContents = `
					<fieldset data-title="Semester Block" data-step='3' data-intro = "This is a semester block. You can drag the courses from the side bar into these boxes where there is a dotted outline. You can also drag courses from semester to semester and delete them from your schedule all together by clicking the trash icon. NOTE: if a semester block is greyed out when you are dragging a course that means it is not available in that semester" class="container scheduleContainer rounded" class="container scheduleContainer rounded" data-semester="${semester}" data-year="${year}" data-order="${semesterOrder}">
						<legend class = "mb-0"> ${semester} ${year}</legend>
							<div class = "row">
								<h6 class = "pl-3" id = "${semester}-${year}-credits"> <i data-toggle="tooltip" title="Credit Count Low: Need more credits for full time" class="fas fa-exclamation-triangle"></i> Scheduled Credits: ${creditCount} </h6>
							</div>
							<div class="row rounded mb-2 drag_box_container mt-0" id="${semester}-${year}">` + holderContents;
				}
				else{
					holderContents = `
					<fieldset data-title="Semester Block" data-step='3' data-intro = "This is a semester block. You can drag the courses from the side bar into these boxes where there is a dotted outline. You can also drag courses from semester to semester and delete them from your schedule all together by clicking the trash icon. NOTE: if a semester block is greyed out when you are dragging a course that means it is not available in that semester" class="container scheduleContainer rounded" class="container scheduleContainer rounded" data-semester="${semester}" data-year="${year}" data-order="${semesterOrder}">
						<legend class = "mb-0"> ${semester} ${year}</legend>
							<div class = "row">
								<h6 class = "pl-3" id = "${semester}-${year}-credits">  Scheduled Credits: ${creditCount} </h6>
							</div>
							<div class="row rounded mb-2 drag_box_container mt-0" id="${semester}-${year}">` + holderContents;
				}
			}
			else{
				if(creditCount >17){
					holderContents = `
				  <fieldset class="container scheduleContainer rounded" data-semester="${semester}" data-year="${year}" data-order="${semesterOrder}">
				    <legend class = "mb-0"> ${semester} ${year}</legend>
							<div class = "row">
								<h6 class = "pl-3" id = "${semester}-${year}-credits"> <i data-toggle="tooltip" title="Credit Count High: There will be an added fee" class="fas fa-exclamation-triangle"></i> Scheduled Credits: ${creditCount} </h6>
							</div>
				      <div class="row rounded mb-2 drag_box_container mt-0" id="${semester}-${year}">` + holderContents;
				}
				else if(creditCount < 12 ){
					holderContents = `
					<fieldset class="container scheduleContainer rounded" data-semester="${semester}" data-year="${year}" data-order="${semesterOrder}">
						<legend class = "mb-0"> ${semester} ${year}</legend>
							<div class = "row">
								<h6 class = "pl-3" id = "${semester}-${year}-credits"> <i data-toggle="tooltip" title="Credit Count Low: Need more credits for full time" class="fas fa-exclamation-triangle"></i> Scheduled Credits: ${creditCount} </h6>
							</div>
							<div class="row rounded mb-2 drag_box_container mt-0" id="${semester}-${year}">` + holderContents;
				}
				else{
					holderContents = `
					<fieldset class="container scheduleContainer rounded" data-semester="${semester}" data-year="${year}" data-order="${semesterOrder}">
						<legend class = "mb-0"> ${semester} ${year}</legend>
							<div class = "row">
								<h6 class = "pl-3" id = "${semester}-${year}-credits"> Scheduled Credits: ${creditCount} </h6>
							</div>
							<div class="row rounded mb-2 drag_box_container mt-0" id="${semester}-${year}">` + holderContents;
				}
			}



	    holderContents += `
	        <div class="col-6 drag_box">
	            <div class="drag_container rounded" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
	        </div>
	    </div>
	  </fieldset>`;
	}

	if(semester == curSemester.semester && year == curSemester.year){
		holderContents += `
			<div class = "row align-items-center">
				<div class= "col-3 overflow-hidden p-0" style = "height:29px; text-align:center;">
					<h6>
						-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
					</h6>
				</div>

				<div class = "col-6 p-0" style = "text-align:center;">
					<h6>
						Future course offerings are not guaranteed to be accurate
					</h6>
				</div>

				<div class= "col-3 overflow-hidden p-0" style = "height:29px; text-align:center;">
					<h6>
						-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
					</h6>
				</div>
			</div>`;
	}

  classHolder.innerHTML +=holderContents;
}

function setUpStudentScheduleContainers(studentData) {
  year = studentData.enrolled_year;
  // console.log(StudentCourses);
  while (year <= studentData.grad_year){
    counter = 0;

    for (i = 0; i < 7; i++) {

      if ((year === studentData.enrolled_year)&&(i === 0)&&(counter === 0)){
        i = ALL_SEMESTERS.indexOf(studentData.enrolled_semester);
        counter = counter + 1;
      }
      //create list of the student's courses in that semester
      let currentSemesterCourses = []
	  
      StudentCourses.forEach((course, index) => {
        if(course.year == year){
          if(course.semester.toUpperCase() == ALL_SEMESTERS[i].toUpperCase()){
            //add course to currentSemesterCourses
            currentSemesterCourses.push(course);
          }
        }
      });
	  console.log(currentSemesterCourses)
      // console.log(currentSemesterCourses);

			if(ALL_SEMESTERS[i]==studentData.enrolled_semester && year == studentData.enrolled_year){
				addClassHolder(ALL_SEMESTERS[i], year, 0, currentSemesterCourses,0);
			}
			else{
				addClassHolder(ALL_SEMESTERS[i], year, 0, currentSemesterCourses,1);
			}
      if ((year === studentData.grad_year) && (i>=ALL_SEMESTERS.indexOf(studentData.grad_semester))){
        year ++;
        break;
      }
      if (i===6){
        year++;
      }
    }
  }
}


function set_valid_drag_locations(event) {

  let dragItem = event.target; // item being dragged
  let dragItemId = dragItem.id; // id of item being dragged
  // find what are valid drop locations
  validSemesters = [];
  years = [];
  combined = [];
  for (i = 0; i < listOfCourses.length; i++) {
    // get the current course
    let currentCourse = listOfCourses[i];
    // see if it is the one we want

    if (dragItemId.includes(currentCourse.courseCode)) {

      // get items
      //let year = currentCourse.year;
      let semester = currentCourse.semester;

      // add to array
      years.push(year);
      validSemesters.push(semester);
      for (let year = studentData.enrolled_year; year <= studentData.grad_year; year++) {
        if((year === studentData.grad_year) && (ALL_SEMESTERS.indexOf(semester)> ALL_SEMESTERS.indexOf(studentData.grad_semester))){
          //do nothing
        }
        else if((year === studentData.enrolled_year) && (ALL_SEMESTERS.indexOf(semester)< ALL_SEMESTERS.indexOf(studentData.enrolled_semester))){
          //do nothing
        }
        else{
          combined.push(`${semester}-${year}`);
          years.push(year);
        }

      }

    }
  }
  //console.log(validSemesters, years, combined);

  // block non-valid
  invalidSemesters = [];
  for (let i = 0; i < ALL_SEMESTERS.length; i++) {
    if(!validSemesters.includes(ALL_SEMESTERS[i])) {
      invalidSemesters.push(ALL_SEMESTERS[i]);

      for (let year = studentData.enrolled_year; year <= studentData.grad_year; year++) {
        invalidCombos.push(`${ALL_SEMESTERS[i]}-${year}`)
      }
    }
  }

  //console.log("INVALID", invalidSemesters, invalidCombos);

  // go over invalid objects
  invalidCombos.forEach((item, index) => {
      let dropContainer = document.getElementById(item);

      if (dropContainer) { // if item found
        // make unable to drop

        dropContainer.parentElement.classList.add('greyOut');
        dropContainer.querySelectorAll(".drag_container").forEach((item) => {
          item.removeAttribute("ondrop");
        });
        dropContainer.querySelectorAll(".drag_container").forEach((item) => {
          item.removeAttribute("ondragover");
        });
      }
  });

  combined.forEach((item1, index) => {
    let dropContainer = document.getElementById(item1);
		//console.log(combined);
		//console.log(item1);
		//console.log(dropContainer);
    let checkId = dragItemId + "-" + item1;
    // console.log(checkId);

    let hasCourse = dropContainer.querySelectorAll(".drag_item_fill");

    if(hasCourse.length > 0){
      // console.log("got in");

      hasCourse.forEach((item2, index) => {
        if(item2.id == checkId){

          dropContainer.parentElement.classList.add('greyOut');
          dropContainer.querySelectorAll(".drag_container").forEach((item3) => {
            item3.removeAttribute("ondrop");
          });
          dropContainer.querySelectorAll(".drag_container").forEach((item3) => {
            item3.removeAttribute("ondragover");
          });


          invalidCombos.push(item1);
        }
      });
    }
  });

}


function revert_drag_locations(event) {
  // go over invalid objects
  invalidCombos.forEach((item, index) => {
      let dropContainer = document.getElementById(item);

      if (dropContainer) { // if item found
        // make able to drop

        dropContainer.parentElement.classList.remove('greyOut');
        dropContainer.querySelectorAll(".drag_container").forEach((item) => {
          item.setAttribute("ondrop", "drop(event)");
        });
        dropContainer.querySelectorAll(".drag_container").forEach((item) => {
          item.setAttribute("ondragover", "allowDrop(event)");
        });
      }
  });

  // clear invalid positions
  while (invalidCombos.length) { invalidCombos.pop(); }
}




//------------------------------------------------------------------------------
/*$.getJSON($SCRIPT_ROOT + '/studentData', {

}, function (data) {
    studentData = data;
    console.log(studentData);
    // set up student schedule containers
    setUpStudentScheduleContainers(studentData);

})*/
