let ALL_SEMESTERS = ["January", "Spring", "May", "Summer", "Fall", "Winter Online"];
let invalidCombos = [];
studentData = {
  startYear:2020,
  startSemester:"Fall",
  gradYear:2024,
  gradSemester:"Spring"
};



function addClassHolder(semester, year, semesterOrder) {
  document.getElementById("main-schedule").innerHTML += `
  <fieldset class="container scheduleContainer rounded" data-semester="${semester}" data-year="${year}" data-order="${semesterOrder}">
    <legend > ${semester} ${year}</legend>
    <div class="row rounded mb-2 drag_box_container mt-0" id="${semester}-${year}">
        <div class="col-6 drag_box">
            <div class="drag_container rounded" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
        </div>
    </div>
  </fieldset>`;
}

function setUpStudentScheduleContainors(studentData) {
  year = studentData.startYear;

  while (year <= studentData.gradYear){
    counter = 0;
    for (i = 0; i < 6; i++) {

      if ((year === studentData.startYear)&&(i === 0)&&(counter === 0)){
        i = ALL_SEMESTERS.indexOf(studentData.startSemester);
        counter = counter + 1;
      }
      addClassHolder(ALL_SEMESTERS[i], year, 0);
      if ((year === studentData.gradYear) && (i>=ALL_SEMESTERS.indexOf(studentData.gradSemester))){
        year ++;
        break;
      }
      if (i===5){
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
    if (dragItemId == currentCourse.courseCode) {
      // get items
      let year = currentCourse.year;
      let semester = currentCourse.semester;
      // add to array
      years.push(year);
      validSemesters.push(semester);
      combined.push(`${semester}-${year}`);
    }
  }
  //console.log(validSemesters, years, combined);

  // block non-valid
  invalidSemesters = [];
  for (let i = 0; i < ALL_SEMESTERS.length; i++) {
    if(!validSemesters.includes(ALL_SEMESTERS[i])) {
      invalidSemesters.push(ALL_SEMESTERS[i]);

      for (let year = studentData.startYear; year <= studentData.gradYear; year++) {
        invalidCombos.push(`${ALL_SEMESTERS[i]}-${year}`)
      }
    }
  }

  //console.log("INVALID", invalidSemesters, invalidCombos);

  // go over invalid objects
  invalidCombos.forEach((item, index) => {
      let dropContainor = document.getElementById(item);

      if (dropContainor) { // if item found
        // make unable to drop

        dropContainor.parentElement.classList.add('greyOut');
        dropContainor.querySelectorAll(".drag_container").forEach((item) => {
          item.removeAttribute("ondrop");
        });
        dropContainor.querySelectorAll(".drag_container").forEach((item) => {
          item.removeAttribute("ondragover");
        });
      }
  });


}


function revert_drag_locations(event) {
  // go over invalid objects
  invalidCombos.forEach((item, index) => {
      let dropContainor = document.getElementById(item);

      if (dropContainor) { // if item found
        // make able to drop

        dropContainor.parentElement.classList.remove('greyOut');
        dropContainor.querySelectorAll(".drag_container").forEach((item) => {
          item.setAttribute("ondrop", "drop(event)");
        });
        dropContainor.querySelectorAll(".drag_container").forEach((item) => {
          item.setAttribute("ondragover", "allowDrop(event)");
        });
      }
  });

  // clear invalid positions
  while (invalidCombos.length) { invalidCombos.pop(); }
}









//------------------------------------------------------------------------------

// set up student schedule containors
setUpStudentScheduleContainors(studentData);
