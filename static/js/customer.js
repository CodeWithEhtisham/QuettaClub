function SearchCustomer() {
  let field = document.getElementById('search_field').value;
  let value = document.getElementById('search_value').value;

  if (field != '' && value != '') {
    $.ajax({
      method: "GET",
      url: "/api/SearchCustomer/",
      data: { "field": field, "value": value },
      success: function (data) {
        // console.log("success on search" + data);
        update_table(data)
      },
      error: function () {
        console.log('error');
      }

    })
  }
};

function update_table(data) {
  let row;
  let all_rows = '';
  Object.keys(data).forEach(key => {
    console.log(data[key]);
    elem = data[key];
    row = '<tr>' +
      '<td>' + elem['customer_rank'] + '</td>' +
      '<td>' + elem['customer_name'] + '</td>' +
      '<td>' + elem['customer_address'] + '</td>' +
      '<td>' + elem['customer_id'] + '</td>' +
      '<td>' +
      '<div class="list-btn">' +
      '<a href=' + "{% url 'Customers:customer_details' %}?id={{customer.id}}" + ' class="">All Bills</a>' +
      '</div>' +
      '</td>' +
      '</tr>'
    all_rows += row;
  });
  $('#Customers_Data tbody').html(all_rows);
};

function SearchbyName() {
  let field = document.getElementById('search_field').value;
  let value = document.getElementById('search_value').value;

  if (field != '' && value != '') {
    $.ajax({
      method: "GET",
      url: "/api/SearchbyName/",
      data: { "field": field, "value": value },
      success: function (data) {
        // console.log("success on search" + data);
        update_customer_table(data)
      },
      error: function () {
        console.log('error');
      }

    })
  }
};

function update_customer_table(data) {
  console.log(data);
  let row;
  let all_rows = '';

  Object.keys(data).forEach(key => {
    elem = data[key];
    console.log(elem);
    console.log(elem['amount'] > 0);
    if (elem['amount'] > 0) {
      row = '<tr>' +
        // '<td>'+elem['id']+'</td>' +
        '<td>' + elem['bill_no'] + '</td>' +
        '<td>' + elem['month'] + '</td>' +
        '<td>' + elem['customer_id']['customer_rank'] + '</td>' +
        '<td>' + elem['PoS_no'] + '</td>' +
        '<td>' + elem['customer_id']['customer_name'] + '</td>' +
        // '<td>'+elem['customer_id']+'</td>' +
        '<td>' + elem['address'] + '</td>' +
        '<td>' + elem['account_of'] + '</td>' +
        '<td>' + elem['date'] + '</td>' +
        '<td>' + elem['amount'] + '</td>' +
        '<td>' + elem['discount'] + '</td>' +
        '<td>' + elem['net_amount'] + '</td>' +
        '<td>' + elem['remarks'] + '</td>' +
        '<td>' +
        '<div class="list">' +
        '<a href="" class="">Edit</a>' +
        '<button id="paid_modal" class="modal">Paid</button>' +
        '<a href="" class="">Complemantery</a>' +
        '<a href="" class="">Cancelled</a>' +
        '</div>' +
        '</td>' +
        '</tr>'
      all_rows += row;
    }
  });
  $('#Sales_data tbody').html(all_rows);

}



let paidModal = document.querySelector(".paidModal-open")
let compModal = document.querySelector(".compModal-open")
let cancelModal = document.querySelector(".cancelModal-open")

// paid model load on click
function paidMOdalOpen(id, value) {
  paidModal.style.display = "block";
  document.getElementById("paid-form-id").value = id;
  document.getElementById("pay_bill_modal_balance").value = value;
}

// paid Modal submit
function paidModalSubmit() {
  $.ajax({
    method: 'POST',
    url: "/api/customer/pay_bill/",
    data: {
      "id": $("#paid-form-id").val(),
      "rv_no": $("#rv_no").val(),
      "paid_date": $("#today-date").val(),
      "amount": $("#paid_amount").val(),
      "remaining_amount": $("#pay_bill_modal_balance").val() - $("#paid_amount").val(),
    },
    dataType: "json",
  })
  paidModal.style.display = "none";
  window.location.reload();
}


function closeModal(model) {
  console.log(model)
  document.querySelector(model).style.display = "none";
}

// open complementory modal window
function compModalOpen(id, value) {
  compModal.style.display = "block";
  document.getElementById("comp-form-id").value = id;
  document.getElementById("comp_bill_modal_balance").value = value;
}

// complementory modal submit button
function compModalSubmit() {
  $.ajax({
    method: "POST",
    url: "/api/customer/comp_bill/",
    data: {
      "id": $("#comp-form-id").val(),
      'comp_date': $("#comp-today-date").val(),
      'comp_remarks': $("#comp_remarks").val(),
      'comp_amount': $("#comp_amount").val(),
      // 'balance': $("#comp_bill_modal_balance").val(),
      "remaining_amount": $("#comp_bill_modal_balance").val() - $("#comp_amount").val(),
    },
    dataType: "json",
  })
  compModal.style.display = "none";
  window.location.reload();
}

// open cancel modal window
function cancelModalOpen(id) {
  cancelModal.style.display = "block";
  document.getElementById("cancel-form-id").value = id;
}

// cancel modal submit button
function cancelModalSubmit() {
  $.ajax({
    method: "POST",
    url: "/api/customer/cancel_bill/",
    data: {
      'id': $("#cancel-form-id").val(),
      'cancel_date': $("#cancel-today-date").val(),
      'reason': $("#reason").val()
    },
    dataType: "json",
  })
  cancelModal.style.display = "none";
  window.location.reload();
}

let today = new Date();
document.getElementById("today-date").value =
  today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) +
  '-' + ('0' + today.getDate()).slice(-2);

let compToday = new Date();
document.getElementById("comp-today-date").value =
  compToday.getFullYear() + '-' + ('0' + (compToday.getMonth() + 1)).slice(-2) +
  '-' + ('0' + compToday.getDate()).slice(-2);

let cancelToday = new Date();
document.getElementById("cancel-today-date").value =
  cancelToday.getFullYear() + '-' + ('0' + (cancelToday.getMonth() + 1)).slice(-2) +
  '-' + ('0' + cancelToday.getDate()).slice(-2);

// function for export to excel or csv file 
function download_table_as_csv(Sales_data, separator = ',') {
  // Select rows from table_id
  var rows = document.querySelectorAll('table#' + Sales_data + ' tr');
  // Construct csv
  var csv = [];
  for (var i = 0; i < rows.length; i++) {
    var row = [], cols = rows[i].querySelectorAll('td, th');
    for (var j = 0; j < cols.length; j++) {
      // Clean innertext to remove multiple spaces and jumpline (break csv)
      var data = cols[j].innerText.replace(/(\r\n|\n|\r)/gm, '').replace(/(\s\s)/gm, ' ')
      // Escape double-quote with double-double-quote (see https://stackoverflow.com/questions/17808511/properly-escape-a-double-quote-in-csv)
      data = data.replace(/"/g, '""');
      // Push escaped string
      row.push('"' + data + '"');
    }
    csv.push(row.join(separator));
  }
  var csv_string = csv.join('\n');
  // Download it
  var filename = Sales_data + '_' + new Date().toLocaleDateString() + '.csv';
  var link = document.createElement('a');
  link.style.display = 'none';
  link.setAttribute('target', '_blank');
  link.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv_string));
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
// auto fill the paid remaining amount on paid modal
document.getElementById("paid_amount").onchange = function () {
  var balance = document.getElementById('pay_bill_modal_balance').value;
  var amount = document.getElementById('paid_amount').value;
  var total = balance - amount;
  document.getElementById('remaing_amount').value = total;
};

