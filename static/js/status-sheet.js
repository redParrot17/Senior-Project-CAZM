function loadStatusSheet(reqs) {
	let keys = Object.keys(reqs)

	for (let key of keys) {
		let value = reqs[key]

		let fieldset = document.createElement("fieldset")
		fieldset.classList = "statusSheetSectionContainer container rounded"

		let legend = document.createElement("legend")
		legend.classList = "StatusSheetTitles"
		legend.innerText = value.title.replaceAll("_"," ")

		fieldset.appendChild(legend)

		let container = document.getElementById("req-list")
		container.appendChild(fieldset)

		let courselist = document.createElement("ul")
		courselist.className="fa-ul"
		var courseAry = value.classes

		for (let i in courseAry) {

			let li = document.createElement("li")
			li.classList = "requirement-list-course"
			li.innerHTML = courseAry[i]

			let span = document.createElement("span")
			span.innerHTML = '<i class="far fa-square" style="color: red;"></i>'
			span.className="fa-li"
			li.appendChild(span)
	

			courselist.appendChild(li)

		}


		fieldset.appendChild(courselist)
		let alt_req_key = value.alternate_requirements


		//List alternates if available
		if (alt_req_key != null) {

			let or = document.createElement("h3")
			or.innerHTML = "OR"
			or.style = "font-weight: bold; font-size: 1.1em"
			fieldset.appendChild(or)
			let alt = reqs[alt_req_key].classes


			let altCourselist = document.createElement("ul")
			altCourselist.className="fa-ul"
			let altCourseAry = alt

			for (let i in altCourseAry) {

				let li = document.createElement("li")
				li.classList = "requirement-list-course"
				li.innerHTML = altCourseAry[i]

				let span = document.createElement("span")
				span.innerHTML = '<i class="far fa-square" style="color: red;"></i>'
				span.className="fa-li"
				li.appendChild(span)
		

				altCourselist.appendChild(li)

				
				

			}
			fieldset.appendChild(altCourselist)

			//REMOVE KEY FROM LIST
			for(let k in keys){ 
    
				if ( keys[k] == alt_req_key) { 	
					
					keys.splice(k, 1); 
				}
			
			}
		

		} //End Alternates
	}
}

function updateStatusSheet(selectedCourses){
	let statusSheetCourses = document.getElementsByClassName("requirement-list-course")
	
	for(course in statusSheetCourses){
		let ssCourse = statusSheetCourses[course]

		if(selectedCourses.includes(ssCourse.innerText)){
			console.log(ssCourse.childNodes)
			ssCourse.childNodes[1].childNodes[0].classList = "fas fa-check-square"
			ssCourse.childNodes[1].childNodes[0].style = "color: green;"

		}
	}
}