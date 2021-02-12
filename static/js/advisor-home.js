
let $table = $('#table')
let $yearFilter = $('#filterYearSelection')
let statusMap = {1: 'Approved', 2: 'Awaiting Student Approval', 3: 'Awaiting Student Creation', 4: 'Awaiting Advisor Approval'};
let advisees = [];

function setAdvisees(json) {
    advisees = json;
}

function buildAdviseeCard(advisee) {
    return [
        '<div class="shadow p-3 mb-4 bg-body rounded">',
        '<div class="row align-items-center">',
        `<div class="col"><h5>${advisee.name}</h5></div>`,
        `<div class="col"><h5>${advisee.id}</h5></div>`,
        '<div class="col">',
        `<strong>Credits Completed:</strong> ${advisee.credits}<br>`,
        `<strong>Status:</status> ${statusMap[advisee.status]}`,
        '</div></div></div>'
    ].join('')
}

function refreshTable() {
    $table.html('')
    advisees.forEach(advisee => {
        $table.html($table.html() + buildAdviseeCard(advisee));
    });
}

$(document).ready(function() {
    refreshTable();
});
