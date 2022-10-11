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
        update_table(data)
      },
      error: function () {
        console.log('error');
      }

    })
  }
};

function update_table(data) {
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
        '<a href="/Sales/update_sales/?id=' + elem['id'] + '" style="background-color: rgb(255, 204, 0); color: black;">Edit</a>' +
        '<button class="modal" id="paid_modal" onclick="paidMOdalOpen(' + elem['id'] + ',' + elem['net_amount'] + ')" style="background-color: green; color: rgb(246, 244, 244);">Paid</button>' +
        '<button id="comp_modal" class="modal" onclick="compModalOpen(' + elem['id'] + ',' + elem['net_amount'] + ')">Complemantery</button>' +
        '<button id="cancel_modal" class="modal" onclick="cancelModalOpen(' + elem['id'] + ',' + elem['net_amount'] + ')" style="background-color: #dc3545;">Cancelled</button>' +

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
  todays('today-date');
}

// paid Modal submit
function paidModalSubmit() {
  var csrftoken = $.cookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  $.ajax({
    method: 'POST',
    url: "/api/sales/pay_bill/",
    data: {
      "id": $("#paid-form-id").val(),
      "rv_no": $("#rv_no").val(),
      "paid_date": $("#today-date").val(),
      "amount": $("#paid_amount").val(),
      "balance": $("#pay_bill_modal_balance").val(),
      
      "remaining_amount": $("#pay_bill_modal_balance").val() - $("#paid_amount").val(),
      csrfmiddlewaretoken: window.CSRF_TOKEN,
    },
    dataType: "json",
  })
  paidModal.style.display = "none";
  window.location.reload();
}


// open complementory modal window
function compModalOpen(id, value) {
  compModal.style.display = "block";
  document.getElementById("comp-form-id").value = id;
  document.getElementById("comp_bill_modal_balance").value = value;
  todays('comp-today-date');
}

// complementory modal submit button
function compModalSubmit() {
  var csrftoken = $.cookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  $.ajax({
    method: "POST",
    url: "/api/sales/comp_bill/",
    data: {
      "id": $("#comp-form-id").val(),
      'comp_date': $("#comp-today-date").val(),
      'comp_remarks': $("#comp_remarks").val(),
      'comp_amount': $("#comp_amount").val(),
      // 'balance': $("#comp_bill_modal_balance").val(),
      "remaining_amount": $("#comp_bill_modal_balance").val() - $("#comp_amount").val(),
      csrfmiddlewaretoken: window.CSRF_TOKEN,
    },
    dataType: "json",
  })
  compModal.style.display = "none";
  window.location.reload();
}


// open cancel modal window
function cancelModalOpen(id, value, amount) {
  cancelModal.style.display = "block";
  document.getElementById("cancel-form-id").value = id;
  document.getElementById("cancel_bill_modal_balance").value = value;
  document.getElementById("bill_amount").value = amount;
  todays('cancel-today-date');
}

// cancel modal submit button
function cancelModalSubmit() {
  var csrftoken = $.cookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  $.ajax({
    method: "POST",
    url: "/api/sales/cancel_bill/",
    data: {
      'id': $("#cancel-form-id").val(),
      'cancel_date': $("#cancel-today-date").val(),
      'reason': $("#reason").val(),
      "remaining_amount": $("#cancel_bill_modal_balance").val(),
      'amount': $("#bill_amount").val(),
      csrfmiddlewaretoken: window.CSRF_TOKEN,
    },
    dataType: "json",
  })
  cancelModal.style.display = "none";
  window.location.reload();
}


function closeModal(model) {
  document.querySelector(model).style.display = "none";
}

// let today = new Date();
// document.getElementById("today-date").value =
//   today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) +
//   '-' + ('0' + today.getDate()).slice(-2);

// let compToday = new Date();
// document.getElementById("comp-today-date").value =
// compToday.getFullYear() + '-' + ('0' + (compToday.getMonth() + 1)).slice(-2) +
//     '-' + ('0' + compToday.getDate()).slice(-2);

// let cancelToday = new Date();
// document.getElementById("cancel-today-date").value =
// cancelToday.getFullYear() + '-' + ('0' + (cancelToday.getMonth() + 1)).slice(-2) +
//         '-' + ('0' + cancelToday.getDate()).slice(-2);


function todays(element_id) {
  let today = new Date();
  document.getElementById(element_id).value =
    today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) +
    '-' + ('0' + today.getDate()).slice(-2);

}

function reloadPage() {
  window.location.reload();
};



function sendTable() {
  var myRows = [];
  var $headers = $("th");
  var $rows = $("tbody tr").each(function (index) {
    $cells = $(this).find("td");
    myRows[index] = {};
    $cells.each(function (cellIndex) {
      myRows[index][$($headers[cellIndex]).html()] = $(this).html();
    });
  });

  // Let's put this in the object like you want and convert to JSON (Note: jQuery will also do this for you on the Ajax request)
  var myObj = {};
  myObj.myrows = myRows;

  var csrftoken = $.cookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });
  // Ajax request goes here
  $.ajax({
    type: "POST",
    url: "/api/sales/sales_upload/",
    data: JSON.stringify(myObj),
    csrfmiddlewaretoken: window.CSRF_TOKEN,
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function (data) {
      // clear table all data
      $("#Sales_data tbody").empty();
    }
  });

}