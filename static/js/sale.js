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
        '<td>' + elem['date'] + '</td>'+
      '<td>' + elem['amount'] + '</td>'+
        '<td>' + elem['discount'] + '</td>' +
        '<td>' + elem['net_amount'] + '</td>' +
        '<td>' + elem['remarks'] + '</td>' +
        '<td>' +
        '<div class="list">' +
        '<a href={% url "Sales:update_sales" %}?id=' +elem['sale.id'] +' style="background-color: rgb(255, 204, 0); color: black;">Edit</a>' +
        '<button class="modal" id="paid_modal" onclick="paidMOdalOpen("{{sale.id}}","{{sale.net_amount}}")" style="background-color: green; color: rgb(246, 244, 244);">Paid</button>' +
        '<button id="comp_modal" class="modal" onclick="compModalOpen("{{sale.id}}","{{sale.net_amount}}")">Complemantery</button>' +
        '<button id="cancel_modal" class="modal" onclick="cancelModalOpen("{{sale.id}}")" style="background-color: #dc3545;">Cancelled</button>' +
        
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
function paidMOdalOpen(id,value){
  paidModal.style.display = "block";
  document.getElementById("paid-form-id").value = id;
  document.getElementById("pay_bill_modal_balance").value = value;
}

// paid Modal submit
function paidModalSubmit() {
  $.ajax({
    method: 'POST',
    url: "/api/sales/pay_bill/",
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
    url: "/api/sales/comp_bill/",
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
  document.getElementById("cancel_bill_modal_balance").value = value;
  // document.getElementById("bill_amount").value = value;
}

// cancel modal submit button
function cancelModalSubmit() {
  $.ajax({
    method: "POST",
    url: "/api/sales/cancel_bill/",
    data: {
      'id': $("#cancel-form-id").val(),
      'cancel_date': $("#cancel-today-date").val(),
      'reason': $("#reason").val(),
      "remaining_amount": $("#cancel_bill_modal_balance").val() * 0 ,
      'amount': $("#bill_amount").val() * 0,
    },
    dataType: "json",
  })
  cancelModal.style.display = "none";
  window.location.reload();
}


function closeModal(model){
  console.log(model)
  document.querySelector(model).style.display = "none";
}

let today = new Date();
document.getElementById("today-date").value =
  today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) +
  '-' + ('0' + today.getDate()).slice(-2);

let compToday = new Date();
document.getElementById("comp-today-date").value = compToday.getFullYear() + '-' + ('0' + (compToday.getMonth() + 1)).slice(-2) + '-' + ('0' + compToday.getDate()).slice(-2);

let cancelToday = new Date();
document.getElementById("cancel-today-date").value = cancelToday.getFullYear() + '-' + ('0' + (cancelToday.getMonth() + 1)).slice(-2) + '-' + ('0' + cancelToday.getDate()).slice(-2);






function reloadPage() {
    window.location.reload();
};

setTimeout(fade_out, 4000);
        function fade_out() {
            $(".messages").fadeOut().empty();
        }
        $(".post-form")[0].reset();


