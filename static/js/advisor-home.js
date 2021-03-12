
let $table = $('#table')

const APPROVED = 1;
const AWAITING_STUDENT_APPROVAL = 2;
const AWAITING_STUDENT_CREATION = 3;
const AWAITING_ADVISOR_APPROVAL = 4;
const STATUS_MAP = {
    [APPROVED]: 'Approved',
    [AWAITING_STUDENT_APPROVAL]: 'Awaiting Student Approval',
    [AWAITING_STUDENT_CREATION]: 'Awaiting Student Creation',
    [AWAITING_ADVISOR_APPROVAL]: 'Awaiting Advisor Approval',
};

let allAdvisees = [];   // A list of all advisee objects.
let uniqueYears = [];   // A unique set of year values.

// values used to filter and sort the listed results
let selectedStatusFilter = $('#status-selector > label.active > input').val() || 'all';
let selectedYearFilter = $('#filterYearSelection').find('option:selected').text();
let selectedSortFilter = $('#sortBySelection').find('option:selected').text();
let searchBarText = $('#search-text').val();


function setAdvisees(json) {
    allAdvisees = json;
    uniqueYears = [];

    allAdvisees.forEach(advisee => {
        // update the set of unique years
        if (!uniqueYears.includes(advisee.year)) {
            uniqueYears.push(advisee.year);
        }
    });
}

function setEmailButtonText(text) {
    $('#message-btn').html(`<i class="fa fa-envelope" aria-hidden="true"></i> Message ${text}`);
}

// ADVISEE FILTERING METHODS //

function filterByStatus(advisees) {
    if (selectedStatusFilter === 'all')
        return advisees;
    else if (selectedStatusFilter === 'approved')
        return advisees.filter(a => a.status === APPROVED);
    else if (selectedStatusFilter === 'awaiting-approval')
        return advisees.filter(a => a.status === AWAITING_STUDENT_APPROVAL || a.status === AWAITING_ADVISOR_APPROVAL);
    else if (selectedStatusFilter === 'awaiting-creation')
        return advisees.filter(a => a.status === AWAITING_STUDENT_CREATION);
    else return [];
}

function filterByYear(advisees) {
    if (selectedYearFilter !== 'All Years...')
        return advisees.filter(a => a.year == selectedYearFilter);
    return advisees;
}

function filterBySearch(advisees) {
    let search = searchBarText.toLowerCase();
    return advisees.filter(a => {
        if (a.id.toString().includes(search)) return true;
        let name = a.name.toLowerCase();
        return search.split(" ").every(s => name.includes(s))
    });
}

function getFilteredAdvisees() {
    let advisees = allAdvisees;
    advisees = filterByStatus(advisees);
    advisees = filterByYear(advisees);
    advisees = filterBySearch(advisees);
    return advisees;
}

function sortAdvisees(advisees) {
    let newAdvisees = advisees;

    if (selectedSortFilter === 'Name')
        newAdvisees.sort(function(a, b) {
            let aName = a.name.toLowerCase();
            let bName = b.name.toLowerCase();
            if (aName > bName) return 1;
            if (aName < bName) return -1;
            return 0;
        });
    else if (selectedSortFilter === 'Major')
        newAdvisees.sort(function(a, b) {
            let aMajor = a.major.toLowerCase();
            let bMajor = b.major.toLowerCase();
            if (aMajor > bMajor) return 1;
            if (aMajor < bMajor) return -1;
            return 0;
        });
    else if (selectedSortFilter === 'Status')
        newAdvisees.sort(function(a, b){ a.status - b.status });
    return newAdvisees;
}

// CALLBACK FUNCTIONS //

// Sends an html POST request to the current location
function httpPost(object) {
    let xhr = new XMLHttpRequest();
    let url = window.location.href;
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.readyState === xhr.DONE) {
            if (xhr.status === 200) {
                console.log(xhr.response);
                console.log(xhr.responseText);
            }
        }
    }
    xhr.send(JSON.stringify(object));
}

function onClickAdvisee(user_id) {
    $('#student_id').val(user_id)
    document.forms[1].submit();
    // window.location.href = `/studentProfile`;
}

function onClickLogout() {
    console.log('Perform logout')
    window.location.href = '/'
}

function onClickMessage() {
    let advisees = getFilteredAdvisees();
    $('#emailModal').modal('show')
    console.log('Email students')
}

// TEMPLATES //

function buildAdviseeCard(advisee) {
    return [
        `<div class="advisee border shadow p-3 mb-4 bg-body rounded" value="${advisee.id}" onclick="onClickAdvisee(${advisee.id})">`,
        '<div class="row align-items-center">',
        `<div class="col"><h5>${advisee.name}</h5></div>`,
        `<div class="col"><h5>${advisee.id}</h5></div>`,
        '<div class="col">',
        `<strong>Credits Completed:</strong> ${advisee.credits}<br>`,
        `<strong>Status:</status> ${STATUS_MAP[advisee.status] || 'Unknown'}`,
        '</div></div></div>'
    ].join('')
}

function buildYearOption(text, selected) {
    if (selected) return `<option selected>${text}</option>`;
    return `<option>${text}</option>`;
}

// SETUP FUNCTIONS //

function refreshTable() {
    $table.html('');
    let advisees = sortAdvisees(getFilteredAdvisees());
    advisees.forEach(advisee => {
        $table.html($table.html() + buildAdviseeCard(advisee));
    });
}

function refreshYears() {
    let $yearSelector = $('#filterYearSelection');
    $yearSelector.html(buildYearOption('All Years...', true));  // reset the inner html
    uniqueYears.forEach(year => $yearSelector.html($yearSelector.html() + buildYearOption(year, false)));
}

function addListeners() {
    $('#status-selector input').click(function() {
        selectedStatusFilter = $(this).val();
        setEmailButtonText($(this).parent().text())
        refreshTable();
    });
    $('#filterYearSelection').change(function() {
        selectedYearFilter = $(this).find('option:selected').text();
        refreshTable();
    });
    $('#sortBySelection').change(function() {
        selectedSortFilter = $(this).find('option:selected').text();
        refreshTable();
    });
    $('#search-btn').click(function() {
        searchBarText = $('#search-text').val();
        refreshTable();
    });
    $('#search-text').on('keypress', function(e) {
        if (e.which === 13) {
            // Disabling textbox to avoid multiple submits.
            $(this).attr('disabled', 'disabled');

            searchBarText = $(this).val();
            refreshTable();

            // Re-enabling textbox
            $(this).removeAttr('disabled');
        }
    });
}

$(document).ready(function() {
    refreshYears();
    addListeners();
    refreshTable();

    $('#emailRichText').richText();
});
