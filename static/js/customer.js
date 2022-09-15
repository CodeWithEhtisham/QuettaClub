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
        elem = data[key];
        row = '<tr>' +
        '<td>'+elem['id']+'</td>' +
        '<td>'+elem['customer_name']+'</td>' +
        '<td>'+elem['customer_rank']+'</td>' +
        '<td>'+elem['customer_id']+'</td>' +
        '<td>' +
        '<div class="list-btn">'+
        '<a href='+"{% url 'Customers:customer_details' %}"+' class="">All Bills</a>'+
        '<a href="" class="">Paid Bill</a>'+
        '<a href="" class="">Printer</a>'+
        '<a href="" class="">Export</a>'+
        '</div>'+
        '</td>' +
        '</tr>'
        all_rows += row;
    });
    $('#Customer_Data tbody').html(all_rows);
}