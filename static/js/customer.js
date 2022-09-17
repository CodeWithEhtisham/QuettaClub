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
}