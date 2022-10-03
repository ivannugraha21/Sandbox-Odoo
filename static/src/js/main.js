# Define Ajax variable

var ajax = require('web.ajax');


//# Json rpc call

ajax.jsonRpc("/some_url", 'call', {'input_data' : $('#input').val()})


//# if data is received from python(odoo backend)

[optional]

.then(function (data) {
    var output_data = data['output_data']  //#Output from controller in form of data dictionary
    //$("#output").html(output_data);
    console.log(output_data)
});