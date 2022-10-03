odoo.define('restapi.sale_order', function (require) {
	"use strict";

	var ListController = require('web.ListController');
	var ListView = require('web.ListView');
	var viewRegistry = require('web.view_registry');
	var TreeButton = ListController.extend({
	   buttons_template: 'saleProductUpdate.buttons',
	   events: _.extend({}, ListController.prototype.events, {
	       'click': '_OpenWizard',
	   }),
	   _OpenWizard: function () {
	   		

		 //    var rpc = require('web.rpc');

		 //    rpc.query({ 
			//      model: 'product.template', 
			//      method: 'action_update_product', 
			//      args: [[],[]]
			// }).then(function(data){
			//      // Result
			//      console.log("BERES");
			//      console.log(data)
			// });


		    console.log('UPDATE SEKARANG')
	   		



	   }
	});
	var SaleOrderListView = ListView.extend({
	   config: _.extend({}, ListView.prototype.config, {
	       Controller: TreeButton,
	   }),
	});
	viewRegistry.add('updateProduct_List', SaleOrderListView);
});