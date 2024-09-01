odoo.define('pj_dashboard.Dashboard', function(require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    var _t = core._t;
    var session = require('web.session');
    var web_client = require('web.web_client');
    var abstractView = require('web.AbstractView');
    var flag = 0;
    var tot_so = []
    var tot_project = []
    var tot_task = []
    var tot_employee = []
    var tot_hrs = []
    var tot_margin = []
    var PjDashboard = AbstractAction.extend({
        template: 'PjDashboard',
        cssLibs: [
            '/project_dashboard_odoo/static/src/css/lib/nv.d3.css'
        ],
        jsLibs: [
            '/project_dashboard_odoo/static/src/js/lib/d3.min.js'
        ],

        events: {

            'change #income_expense_values': 'onchange_profitability',
//            'change #start_date': '_onchangeFilter',
//            'change #end_date': '_onchangeFilter',
             'click #filter_button': '_onchangeFilter',
            'change #employee_selection': '_onchangeFilter',
//            'change #project_selection': 'render_filter',
               'click #project_selection': '_onProjectSelectionClick',
               'click #month_selection': '_onMonthSelectionClick',
        },

        init: function(parent, context) {
            this._super(parent, context);
            this.dashboards_templates = ['DashboardProject', 'DashboardChart'];
            this.today_sale = [];
        },


        willStart: function() {
            var self = this;
            return $.when(ajax.loadLibs(this), this._super()).then(function() {
                return self.fetch_data();
            });
        },

        start: function() {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function() {
                self.render_dashboards();
//                self.render_graphs();
                self.render_filter()
            });
        },

        render_dashboards: function() {
            var self = this;
            _.each(this.dashboards_templates, function(template) {
                self.$('.o_pj_dashboard').append(QWeb.render(template, {
                    widget: self
                }));
            });
        },

        render_filter: function() {
            alert('hai')
            ajax.rpc('/sale/order/year').then(function(response) {

//            var data = JSON.parse(response);
            console.log(response)
            var currentYear = new Date().getFullYear();
//            $("#project_selection").val(currentYear);
             let serialNumber = 1;
             for (const key in response.month_wise_totals)
{

             var Html="<tr>
                <td >"+serialNumber+" </td>
                <td>"+key+"</td>
                <td>"+response.month_wise_totals[key]['subtotal']+"</td>
                <td>"+response.month_wise_totals[key]['total']+"</td>
            </tr>";
            $('#tbody').append(Html);
            serialNumber++;
    }
       });
                },




        on_reverse_breadcrumb: function() {
            var self = this;
            web_client.do_push_state({});
            this.fetch_data().then(function() {
                self.$('.o_pj_dashboard').empty();
                self.render_dashboards();
//                self.render_graphs();
            });
        },
        _onchangeFilter: function() {
            flag = 1
            var selectedYear = $('#project_selection').val();
            var selectedMonth = $('#month_selection').val();
//            var start_date = selectedYear + "/01/01";
//            var end_date = selectedYear + "/12/31";
            console.log(selectedMonth)

            if (selectedMonth === 'month') {
         var startDate = new Date(selectedYear, 0, 1);
            var endDate = new Date(selectedYear, 11, 31);
            var start_date = startDate.toISOString().split('T')[0].replace(/-/g, '/');
            var end_date = endDate.toISOString().split('T')[0].replace(/-/g, '/');
//            console.log(start_date)
//            console.log(end_date)
                       $('#tbody').empty();
            ajax.rpc('/project/filter-apply/year-wise', {
                'data': {
                    'start_date': start_date,
                    'end_date': end_date,

                }
            }).then(function(data) {
             console.log(data.month_wise_totals)
             let serialNumber = 1;
             for (const key in data.month_wise_totals)
{

             var Html="<tr>
                <td >"+serialNumber+" </td>
                <td>"+key+"</td>
                <td>"+data.month_wise_totals[key]['subtotal']+"</td>
                <td>"+data.month_wise_totals[key]['total']+"</td>
            </tr>";
            $('#tbody').append(Html);
            serialNumber++;
    }
    var selectBox1 = document.getElementById("project_selection");
    selectBox1.selectedIndex = 0;


            })
            }
            else{

        var startDate = new Date(selectedYear, selectedMonth - 1, 1); // Set the day to 01
        var endDate = new Date(selectedYear, selectedMonth, 1);
        var start_date = startDate.toISOString().split('T')[0].replace(/-/g, '/');
        var end_date = endDate.toISOString().split('T')[0].replace(/-/g, '/');
//        console.log(start_date)
//        console.log(end_date)
                   ajax.rpc('/filter-apply/month-wise', {
                'data': {
                    'start_date': start_date,
                    'end_date': end_date,

                }
            }).then(function(data) {
             console.log(data)
             var selectBox1 = document.getElementById("project_selection");
             var selectBox2 = document.getElementById("month_selection");
             selectBox1.selectedIndex = 0
             selectBox2.selectedIndex = 0
             document.getElementById('fixed_forcast').innerHTML = data['total_sum']
             document.getElementById('timesheet_forcast').innerHTML = data['subtotal_sum']
             document.getElementById('pending_forcast').innerHTML = data['pending_data']
             document.getElementById('achieved_data').innerHTML = data['achieved_data']

//             let serialNumber = 1;
//             for (const key in data.month_wise_totals)
//{
//
//             var Html="<tr>
//                <td >"+serialNumber+" </td>
//                <td>"+key+"</td>
//                <td>"+data.month_wise_totals[key]['subtotal']+"</td>
//                <td>"+data.month_wise_totals[key]['total']+"</td>
//            </tr>";
//            $('#tbody').append(Html);
//            serialNumber++;
//    }

            });


            }


        },

        _onProjectSelectionClick: function() {
         var $projectSelection = $('#project_selection');
    if ($projectSelection.data('loaded') !== true) {
        // Set a flag to indicate that options have been loaded
        $projectSelection.data('loaded', true);
        ajax.rpc('/project/filter').then(function(response) {
            var data = JSON.parse(response);
            console.log(data.years)
                var years = data.years;

//                var employees = data[1]
                $(years).each(function(index,year) {
                    $('#project_selection').append("<option value=" + year + " class='fs-5'>" + year + "</option>");
                });
                 });
                 }
        },

 _onMonthSelectionClick: function() {
         var $monthSelection = $('#month_selection');
    if ($monthSelection.data('loaded') !== true) {
        // Set a flag to indicate that options have been loaded
        $monthSelection.data('loaded', true);
        ajax.rpc('/month/filter').then(function(response) {
            var data = JSON.parse(response);
            console.log(data.months)
                var years = data.months;

//                var employees = data[1]
                $(years).each(function(index,year) {
                var monthNumber = index + 1;
                    $('#month_selection').append("<option value=" + monthNumber + " class='fs-5'>" + year + "</option>");
                });
                 });
                 }
        },






        fetch_data: function() {
            var self = this;
            var def1 = this._rpc({
                model: 'project.project',
                method: 'get_tiles_data'
            }).then(function(result) {
                self.total_projects = result['total_projects']

            });





            return $.when(def1);
        },

    });

    core.action_registry.add('project_dashboard', PjDashboard);

    return PjDashboard;

});