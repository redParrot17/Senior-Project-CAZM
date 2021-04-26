
/* Gets number of credits for a coursecode */
function getCredits(code) {

	var returnedCredits = -1;

	let found = false;
	var courseIndex = 0;

	while (!found && courseIndex < listOfCourses.length) {
		let searchedCourse = listOfCourses[courseIndex];

		if (searchedCourse.courseCode === code[0]) {
			found = true;
			returnedCredits = searchedCourse.credits;
		}
		courseIndex++;
	}


	return returnedCredits;
}


/* Gets number of credits for a coursecode */
function getCreditsForSum(code) {

	var returnedCredits = -1;

	let found = false;
	var courseIndex = 0;

	while (!found && courseIndex < listOfCourses.length) {
		let searchedCourse = listOfCourses[courseIndex];

		if (searchedCourse.courseCode === code) {
			found = true;
			returnedCredits = searchedCourse.credits;
		}
		courseIndex++;
	}


	return returnedCredits;
}





function updateStatusSheet() {

	let statusSheetCourses = document.getElementsByClassName("requirement-list-course")

	let selectedClasses = document.getElementsByClassName("drag_item drag_item_fill")


	for (let courseNum = 0; courseNum < statusSheetCourses.length; courseNum++) {


		//Set checkboxes as default
		let statusSheetCourse = statusSheetCourses[courseNum];
		let statusSheetCourseCode = statusSheetCourse.childNodes[0].nodeValue;
		statusSheetCourse.childNodes[1].childNodes[0].classList = "fas fa-times"
		statusSheetCourse.childNodes[1].childNodes[0].style = "color: red;"


		for (let classNum = 0; classNum < selectedClasses.length; classNum++) {

			let selectedClass = selectedClasses[classNum];
			let selectedCode = selectedClass.getAttribute("coursecode");



			if (statusSheetCourseCode === selectedCode) {
				let year = selectedClass.getAttribute("year")
				let semester = selectedClass.getAttribute("semester")



				if (getTargetIndex(year,semester) < getTargetIndex(curSemester.year, curSemester.semester)) {

					statusSheetCourse.childNodes[1].childNodes[0].classList = "fas fa-check"
					statusSheetCourse.childNodes[1].childNodes[0].style = "color: green;"
				}
				else {

					statusSheetCourse.childNodes[1].childNodes[0].classList = "fas fa-hourglass-start"
					statusSheetCourse.childNodes[1].childNodes[0].style = "color: blue;"
				}


			}


		}

	}
}


/**
 * Loads the status sheet into the DOM
 * @param {Object} reqs
 * JSON dictionary of requirement info to build the status sheet from
 */
 function loadStatusSheet(reqs) {

	/**
	 * Array of requirement IDs
	 */
	let keys = Object.keys(reqs)

	/**
	 * container of course requirements
	 */
	let container = document.getElementById("req-list")


	for (let key of keys) {

		/**
		 * Individual Requirement
		 */
		let value = reqs[key]

		//Create Fieldset with legend
		let requirementContainer = document.createElement("fieldset")
		requirementContainer.classList = "statusSheetSectionContainer container rounded"
		let legend = document.createElement("legend")
		legend.classList = "StatusSheetTitles"
		legend.innerText = value.title.replaceAll("_", " ")
		requirementContainer.appendChild(legend)
		container.appendChild(requirementContainer)



		/*Special Requirement*/
		if (value.special !== "") {
			let message = value.special;
			let p = document.createElement("p");
			p.innerHTML = message;
			requirementContainer.appendChild(p)

		}


		/*Normal Requirement*/
		else {

			var clusters = value.clusters

			let clusterKeys = Object.keys(clusters);

			//Examine each cluster
			var count = 0
			for (let clusterKey of clusterKeys) {

				let selectedCluster = clusters[clusterKey]


				//credit requirement?
				let creds = selectedCluster.credits;
				let courses = selectedCluster.courses;
				let alts = selectedCluster.alternate_clusters;





				//Each course in current cluster
				let courselist = document.createElement("ul")
				courselist.className = "fa-ul"
				for (let course = 0; course < courses.length; course++) {
					let currentCourse = courses[course];
					let li = document.createElement("li");
					li.classList = "requirement-list-course";
					li.innerText = currentCourse;

					//Add Credits
					let creditSpan = document.createElement("span");
					let creds = getCredits(currentCourse)
					creditSpan.classList = "shift-right"
					if (creds !== -1) {
						creditSpan.innerText = " - " + creds + " Credits";
					}
					else {
						creditSpan.innerText = " - Course Unavailable!";
					}

					let span = document.createElement("span")
					span.innerHTML = '<i class="fas fa-times" style="color: red;"></i>'
					span.className = "fa-li"
					li.appendChild(span)
					li.appendChild(creditSpan)
					courselist.appendChild(li)
				}



				if (count > 0) {
					let and = document.createElement("h3");
					and.classList = "fa-ul status-h3";
					and.innerText = "[AND]"
					requirementContainer.appendChild(and)
				}


				if (creds !== null) {
					let credMsg = "Select " + creds + " credits";
					let msg = document.createElement("p");
					msg.classList = "fa-ul select-txt"

					msg.innerHTML = credMsg;
					requirementContainer.appendChild(msg)
				}

				requirementContainer.appendChild(courselist)


				//! Add and remove Alt clusters
				for (let i = 0; i < alts.length; i++) {

					let altcourselist = document.createElement("ul")
					altcourselist.className = "fa-ul"

					let alt_key = alts[i][0];
					let alt_cluster = clusters[alt_key];
					let alternate_creds = alt_cluster.credits;
					let alternate_courses = alt_cluster.courses;


					for (let altcourse = 0; altcourse < alternate_courses.length; altcourse++) {

						let currentAltCourse = alternate_courses[altcourse];
						let li = document.createElement("li")
						li.classList = "requirement-list-course"
						li.style = "width: 48%;"
						li.innerText = currentAltCourse

						//Add Credits
						let altcreditSpan = document.createElement("span");
						altcreditSpan.classList = "shift-right"

						let altcreds = getCredits(currentAltCourse)
						if (altcreds !== -1) {
							altcreditSpan.innerText = " - " + altcreds + " Credits";
						}
						else {
							altcreditSpan.innerText = " - Course Unavailable!";
						}

						let altspan = document.createElement("span")
						altspan.innerHTML = '<i class="fas fa-times" style="color: red;"></i>'

						altspan.className = "fa-li"

						li.appendChild(altspan)
						li.appendChild(altcreditSpan)
						altcourselist.appendChild(li)

					}
					let or = document.createElement("h3");
					or.classList = "or status-h3"
					or.innerText = "[~~~ OR ~~~]";
					requirementContainer.appendChild(or);

					if (alternate_creds !== null) {
						let altcredMsg = "Select " + alternatecreds + " credits";
						let altmsg = document.createElement("p");
						altmsg.innerHTML = altcredMsg;
						msg.classList = "fa-ul select-txt"


						requirementContainer.appendChild(altmsg)
					}

					requirementContainer.appendChild(altcourselist)


					for (let k in clusterKeys) {

						if (clusterKeys[k] == alt_key)
							clusterKeys.splice(k,1);
					}


				}



				count++;
			}

		}

	}
	updateStatusSheet();
}
