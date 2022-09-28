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

function update_table(data){
    let row;
    let all_rows = '';
    Object.keys(data).forEach(key => {
        console.log(data[key]);
        elem = data[key];
        row = '<tr>' +
        '<td>'+elem['customer_rank']+'</td>' +
        '<td>'+elem['customer_name']+'</td>' +
        '<td>'+elem['customer_address']+'</td>' +
        '<td>'+elem['customer_id']+'</td>' +
        '<td>' +
        '<div class="list-btn">'+
        '<a href='+"{% url 'Customers:customer_details' %}?id={{customer.id}}"+' class="">All Bills</a>'+
        '</div>'+
        '</td>' +
        '</tr>'
        all_rows += row;
    });
    $('#Customers_Data tbody').html(all_rows);
};

function customerCheck(data) {
    if (customer_name.includes(data.value)) {
        console.log("Customer Name No Already Exist");
        document.getElementById("customer_name").style.border = "1px solid red";
    }
    else {
        console.log("customer name No Not Exist");
        document.getElementById("customer_name").style.border = "1px solid green";
    }

}

        // // let saleId = document.getElementById("paid_modal_id").value
        // let paidModal = document.getElementById("paid_modal")
        // let compModalBtn = document.getElementById("comp_modal")
        // let canModalBtn = document.getElementById("cancel_modal")
        
        // let modal1 = document.querySelector(".paidModal-open")
        // let modal2 = document.querySelector(".compModal-open")
        // let modal3 = document.querySelector(".cancelModal-open")
        // let closeBtn = document.querySelector(".close-btn")
        // let cancelBtn = document.querySelector(".cancel")

        // window.payBill = function (id) {
        //     modal1.style.display = "block";
        //     $.ajax({
        //         method: "GET",
        //         url: "/api/pay_bill/",
        //         data: { "id": id },
        //         success: function (data) {
        //             // console.log(data);
        //             document.getElementById("pay_bill_modal_balance").value = data.net_amount;
        //             // update_table(data)
        //         }
        //     });

        //     $(document).ready(function () {
        //         $("form#pay_bill").submit(function (event) {
        //           let formData = {
        //             "id":id,
        //             "rv_no": $("#rv_no").val(),
        //             "paid_date": $("#today-date").val(),
        //             "amount": $("#paid_amount").val(),
        //             // balance: $("#pay_bill_modal_balance").val(),
        //             "remaining_amount": $("#pay_bill_modal_balance").val() - $("#paid_amount").val(),
        //           };
        //           console.log(JSON.stringify(formData));
              
        //           $.ajax({
        //             method: 'POST',
        //             url: "/api/pay_bill/",
        //             dataType: "json",
        //             data: formData,
        //           }).done(function (data) {
        //             console.log(data);
        //           });
              
        //           // event.preventDefault();
        //         });
        //       });
        // }

        // // complementary modal window
        // window.compBill = function (id) {
        //     modal2.style.display = "block";
        //     $.ajax({
        //         method: "GET",
        //         url: "/api/comp_bill/",
        //         data: { "id": id },
        //         success: function (data) {
        //             // console.log(data);
        //             document.getElementById("comp_bill_modal_balance").value = data.net_amount;
        //             // update_table(data)
        //         }
        //     });

        //     $(document).ready(function () {
        //         $("form#comp_bill").submit(function (event) {
        //           let formData = {
                    
        //             'comp_date': $("#today-date").val(),
        //             'comp_remarks': $("#comp_remarks").val(),
        //             'amount': $("#comp_amount").val(),
        //             'balance': $("#comp_bill_modal_balance").val(),
        //             // remaining_amount: $("#pay_bill_modal_balance").val() - $("#paid_amount").val(),
        //           };
        //           console.log(formData);
              
        //           $.ajax({
        //             method: "POST",
        //             url: "/api/comp_bill/",
        //             data: formData,
        //             dataType: "json",
        //           }).done(function (data) {
        //             console.log(data);
        //           });
              
        //           event.preventDefault();
        //         });
        //       });
        // }

        // // cancel modal window
        // window.cancelBill = function (id) {
        //     modal3.style.display = "block";
        //     $.ajax({
        //         method: "GET",
        //         url: "/api/cancel_bill/",
        //         data: { "id": id },
        //         success: function (data) {
        //             // console.log(data);
        //             document.getElementById("cancel_bill_modal_balance").value = data.net_amount;
        //             // update_table(data)
        //         }
        //     });

        //     $(document).ready(function () {
        //         $("form#cancel_bill").submit(function (event) {
        //           let formData = {
                    
        //             'cancel_date': $("#today-date").val(),
        //             'reason': $("#reason").val()
        //           };
        //           console.log(formData);
              
        //           $.ajax({
        //             method: "POST",
        //             url: "/api/cancel_bill/",
        //             data: formData,
        //             dataType: "json",
        //           }).done(function (data) {
        //             console.log(data);
        //           });
              
        //           event.preventDefault();
        //         });
        //       });
        // }
