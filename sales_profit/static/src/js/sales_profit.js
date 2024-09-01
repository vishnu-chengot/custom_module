odoo.define('sales_profit.select', function(require) {
	"use strict";
	var ListController = require('web.ListController');
	var rpc = require('web.rpc');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var session = require('web.session');
    var qweb = core.qweb;
    var _t = core._t;
	ListController.include({
        events: {
            "click .btn-sales-profit-report":"sales_profit_report",
        },
        _updateSelectionBox() {                   
            self = this;
            this._super.apply(this, arguments); 
            console.log("sale.order======================>",this);
            if (this.modelName == 'sale.order'){           
                if (this.$SalesProfitButton) {
                    this.$SalesProfitButton.remove();
                    this.$SalesProfitButton = null;
                } 
                this.$SalesProfitButton = $(qweb.render('sales_profit_report', {}));
                this.$SalesProfitButton.insertAfter($('.o_list_selection_box'));
            }
            
        },
        sales_profit_report: function(event) {
            
            const state = this.model.get(this.handle, {raw: true});
            
            let records = self.getSelectedRecords()
            console.log("sale.order======================>",typeof records);
            let active_ids = []
            $.each(records, function() {active_ids.push(this.res_id)})            
            if (records.length >= 1){
                rpc.query({
                    model: 'sale.order',
                    method: 'get_sale_order_info',
                    args: [active_ids],
                }).then(function(orders){
                    console.log("Orders",orders);
                    var buttons = [         
                        {
                            text: _t("Cancel"),
                            close: true,
                        },
                    ];
                    var dialog = new Dialog(this, {
                        title: _t("Compare Sales Orders"),
                        buttons: buttons,
                        $content: qweb.render('sales_profit_report_info', {orders:orders})
                    });
                    dialog.open();
                })
                
            }
        }
           
		
	});
	return ListController

});