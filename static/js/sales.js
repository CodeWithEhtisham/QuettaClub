function SearchbyName(){
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

function update_table(data){
    console.log(data);
    let row;
    let all_rows = '';

    Object.keys(data).forEach(key => {
        elem = data[key];
        console.log(elem);
        row = '<tr>' +
        // '<td>'+elem['id']+'</td>' +
        '<td>'+elem['bill_no']+'</td>' +
        '<td>'+elem['month']+'</td>' +
        '<td>'+elem['customer_id']['customer_rank']+'</td>' +
        '<td>'+elem['PoS_no']+'</td>' +
        '<td>'+elem['customer_id']['customer_name']+'</td>' +
        // '<td>'+elem['customer_id']+'</td>' +
        '<td>'+elem['address']+'</td>' +
        '<td>'+elem['account_of']+'</td>' +
        '<td>'+elem['date']+'</td>' +
        '<td>'+elem['amount']+'</td>' +
        '<td>'+elem['discount']+'</td>' +
        '<td>'+elem['net_amount']+'</td>' +
        '<td>'+elem['remarks']+'</td>' +
        '<td>' +
            '<div class="list">'+
                '<a href="" class="">Edit</a>'+
                '<button id="paid_modal" class="modal">Paid</button>'+
                '<a href="" class="">Complemantery</a>'+
                '<a href="" class="">Cancelled</a>'+
            '</div>'+
        '</td>' +
        '</tr>'
        all_rows += row;
    });
    $('#Sales_data tbody').html(all_rows);
        
}