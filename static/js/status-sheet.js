function loadStatusSheet(reqs) {
	let keys = Object.keys(reqs)
	console.log(keys)
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

		let courselist = document.createElement("ol")
		var courseAry = value.classes

		for (let i in courseAry) {

			let li = document.createElement("li")
			li.classList = "requirement-list-course"
			li.innerHTML = courseAry[i]
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


			let altCourselist = document.createElement("ol")
			let altCourseAry = alt

			for (let i in altCourseAry) {

				let li = document.createElement("li")
				li.classList = "requirement-list-course"
				li.innerHTML = altCourseAry[i]
				altCourselist.appendChild(li)

			}
			fieldset.appendChild(altCourselist)

			//REMOVE KEY FROM LIST
			for(let k in keys){ 
    
				if ( keys[k] == alt_req_key) { 	
					console.log("Removed " + keys[k] + " from list")
					keys.splice(k, 1); 
				}
			
			}
		

		} //End Alternates
	}
}