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
        '<td>' + elem['date'] + '</td>';
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

// let saleId = document.getElementById("paid_modal_id").value
let paidModal = document.getElementById("paid_modal")
let compModalBtn = document.getElementById("comp_modal")
let canModalBtn = document.getElementById("cancel_modal")

let modal1 = document.querySelector(".paidModal-open")
let modal2 = document.querySelector(".compModal-open")
let modal3 = document.querySelector(".cancelModal-open")
let closeBtn = document.querySelector(".close-btn")
let cancelBtn = document.querySelector(".cancel")

window.payBill = function (id) {
  modal1.style.display = "block";
  $.ajax({
    method: "GET",
    url: "/api/sales/pay_bill/",
    data: { "id": id },
    success: function (data) {
      // console.log(data);
      document.getElementById("pay_bill_modal_balance").value = data.net_amount;
      // update_table(data)
    }
  });

  $(document).ready(function () {
    $("form#pay_bill").submit(function (event) {
      let formData = {
        "id": id,
        "rv_no": $("#rv_no").val(),
        "paid_date": $("#today-date").val(),
        "amount": $("#paid_amount").val(),
        // balance: $("#pay_bill_modal_balance").val(),
        "remaining_amount": $("#pay_bill_modal_balance").val() - $("#paid_amount").val(),
      };
      console.log(JSON.stringify(formData));

      $.ajax({
        method: 'POST',
        url: "/api/sales/pay_bill/",
        dataType: "json",
        data: formData,
      }).done(function (data) {
        console.log(data);
      });

      // event.preventDefault();
    });
  });
}

// complementary modal window
window.compBill = function (id) {
  modal2.style.display = "block";
  $.ajax({
    method: "GET",
    url: "/api/sales/comp_bill/",
    data: { "id": id },
    success: function (data) {
      // console.log(data);
      document.getElementById("comp_bill_modal_balance").value = data.net_amount;
      // update_table(data)
    }
  });

  $(document).ready(function () {
    $("form#comp_bill").submit(function (event) {
      let formData = {

        'comp_date': $("#today-date").val(),
        'comp_remarks': $("#comp_remarks").val(),
        'amount': $("#comp_amount").val(),
        'balance': $("#comp_bill_modal_balance").val(),
        // remaining_amount: $("#pay_bill_modal_balance").val() - $("#paid_amount").val(),
      };
      console.log(formData);

      $.ajax({
        method: "POST",
        url: "/api/sales/comp_bill/",
        data: formData,
        dataType: "json",
      }).done(function (data) {
        console.log(data);
      });

      event.preventDefault();
    });
  });
}

// cancel modal window
window.cancelBill = function (id) {
  modal3.style.display = "block";
  $.ajax({
    method: "GET",
    url: "/api/sales/cancel_bill/",
    data: { "id": id },
    success: function (data) {
      console.log(data);
      // document.getElementById("cancel_bill_modal_balance").value = data.net_amount;
      // update_table(data)
    }
  });

  $(document).ready(function () {
    $("form#cancel_bill").submit(function (event) {
      let formData = {

        'cancel_date': $("#today-date").val(),
        'reason': $("#reason").val()
      };
      console.log(formData);

      $.ajax({
        method: "POST",
        url: "/api/sales/cancel_bill/",
        data: formData,
        dataType: "json",
      }).done(function (data) {
        console.log(data);
      });

      event.preventDefault();
    });
  });
}

closeBtn.onclick = function () {
  if (modal1.style.display = "block") {
    modal1.style.display = "none"
  }
  if (modal2.style.display = "block") {
    modal2.style.display = "none"
  }
  if (modal3.style.display = "block") {
    modal3.style.display = "none"
  }
}
cancelBtn.onclick = function () {
  if (modal1.style.display = "block") {
    console.log("modal1")
    modal1.style.display = "none"
  } if (modal2.style.display = "block") {
    console.log("modal2")
    modal2.style.display = "none"
  }
  if (modal3.style.display = "block") {
    console.log("modal3")
    modal3.style.display = "none"
  }
}

function cancelModel(model){
  model.style.display = "none"
}
// window.onclick = function (e) {
//     if (e.target == modal) {
//         modal1.style.display = "block"
//     }
// }
var today = new Date();
document.getElementById("today-date").value =
  today.getFullYear() + '-' + ('0' + (today.getMonth() + 1)).slice(-2) +
  '-' + ('0' + today.getDate()).slice(-2);