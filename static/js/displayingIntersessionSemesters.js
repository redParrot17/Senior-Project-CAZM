
function displayIntersessionSemesters() {
  if (document.getElementById("intersession-checkbox").checked) {
    mainSchedule = document.getElementById("main-schedule");
    mainSchedule.querySelectorAll(".scheduleContainer").forEach((item) => {
      if(item.getAttribute("data-semester") == "WINTER ONLINE" || item.getAttribute("data-semester") == "JANUARY" || item.getAttribute("data-semester") == "MAY" || item.getAttribute("data-semester") == "EARLY SUMMER" || item.getAttribute("data-semester") == "LATE SUMMER"){
        item.classList.remove('itemInvisible');
      }
    })
  }
  else{
    mainSchedule = document.getElementById("main-schedule");
    mainSchedule.querySelectorAll(".scheduleContainer").forEach((item) => {
      if(item.getAttribute("data-semester") == "WINTER ONLINE" || item.getAttribute("data-semester") == "JANUARY" || item.getAttribute("data-semester") == "MAY" || item.getAttribute("data-semester") == "EARLY SUMMER" || item.getAttribute("data-semester") == "LATE SUMMER"){
        item.classList.add('itemInvisible');
      }
    })
  }

}
