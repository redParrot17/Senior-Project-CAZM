/**
 * Toggles the displaying of intersession semesters in the semester list
 */
function displayIntersessionSemesters() {
  if (document.getElementById("intersession-checkbox").checked) {
    mainSchedule = document.getElementById("main-schedule");
    mainSchedule.querySelectorAll(".scheduleContainer").forEach((item) => {
      if(item.getAttribute("data-semester") == "Winter Online" || item.getAttribute("data-semester") == "January" || item.getAttribute("data-semester") == "May" || item.getAttribute("data-semester") == "Early Summer" || item.getAttribute("data-semester") == "Late Summer"){
        item.classList.remove('itemInvisible');
      }
    })
  }
  else{
    mainSchedule = document.getElementById("main-schedule");
    mainSchedule.querySelectorAll(".scheduleContainer").forEach((item) => {
      if(item.getAttribute("data-semester") == "Winter Online" || item.getAttribute("data-semester") == "January" || item.getAttribute("data-semester") == "May" || item.getAttribute("data-semester") == "Early Summer" || item.getAttribute("data-semester") == "Late Summer"){
        item.classList.add('itemInvisible');
      }
    })
  }

}
