# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
import datetime

from odoo import http
from odoo.http import request
from collections import defaultdict
import json
# from datetime import datetime

class ProjectFilter(http.Controller):
    """
    The ProjectFilter class provides the filter option to the js.
    When applying the filter return the corresponding data.
        Methods:
            project_filter(self):
                when the page is loaded adding filter options to the selection
                field.
                return a list variable.
            project_filter_apply(self,**kw):
                after applying the filter receiving the values and return the
                filtered data.

    """

    @http.route('/project/filter', auth='public', type='json')
    def project_filter(self):

        """

        Summery:
            transferring data to the selection field that works as a filter
        Returns:
            type:list of lists , it contains the data for the corresponding
            filter.


        """
        current_year = datetime.datetime.now().year
        start_year = current_year - 10
        end_year = current_year + 5
        years = list(range(start_year, end_year + 1))
        response_data = {'years': years}

        # Log the response before returning
        print(json.dumps(response_data))

        return json.dumps(response_data)

    @http.route('/month/filter', auth='public', type='json')
    def month_filter(self):
        current_year = datetime.datetime.now().year

        # Generate a list of 12 months for the current year
        months = [datetime.date(current_year, month, 1).strftime('%B') for month in range(1, 13)]

        response_data = {'months': months}

        # Log the response before returning
        print(json.dumps(response_data))

        return json.dumps(response_data)






    @http.route('/project/filter-apply/year-wise', auth='public', type='json')
    def project_filter_apply_year_wise(self, **kw):
        data = kw['data']
        print(f"Debug: Data received: {data}")

        # Extract start_date and end_date from the input data
        start_date = data['start_date']
        end_date = data['end_date']

        # Convert start_date and end_date strings to datetime objects
        # start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        # end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        # Initialize a dictionary to store month-wise totals
        # month_totals = defaultdict(float)
        month_totals = defaultdict(lambda: {'subtotal': 0.0, 'total': 0.0})

        # Query sale.order.line records based on start_date and end_date
        sale_order_lines = request.env['sale.order.line'].search(
            [('start_date_order', '>=', start_date), ('start_date_order', '<=', end_date)])

        # Iterate through the sale order lines and calculate month-wise totals
        for line in sale_order_lines:
            month = line.start_date_order.strftime('%B')  # Get the month name
            subtotal = line.price_subtotal
            total = line.price_total
            month_totals[month]['subtotal'] += subtotal
            month_totals[month]['total'] += total

        # Convert the defaultdict to a regular dictionary
        month_totals_dict = dict(month_totals)

        return {
            'month_wise_totals': month_totals_dict,
        }

    @http.route('/sale/order/year', auth='public', type='json')
    def sale_order_year(self):
        current_year = datetime.datetime.now().year

        # Initialize a dictionary to store month-wise data
        monthly_data = defaultdict(lambda: {'subtotal': 0.0, 'total': 0.0})

        # Query sale.order.line records for the current year
        sale_order_lines = request.env['sale.order.line'].search([
            ('start_date_order', '>=', f'{current_year}-01-01'),
            ('start_date_order', '<=', f'{current_year}-12-31')
        ])

        # Iterate through the sale order lines and calculate month-wise totals
        for line in sale_order_lines:
            month = line.start_date_order.strftime('%B').lower()  # Get the month name in lowercase
            subtotal = line.price_subtotal
            total = line.price_total

            # Ensure that the values in the dictionary are numerical before adding
            monthly_data[f'{month}']['subtotal'] += subtotal
            monthly_data[f'{month}']['total'] += total

        # Convert the defaultdict to a regular dictionary
        monthly_data_dict = dict(monthly_data)

        return {
            'month_wise_totals': monthly_data_dict,
        }

    @http.route('/filter-apply/month-wise', auth='public', type='json')
    def filter_apply_month_wise(self, **kw):
        data = kw['data']
        print(f"Debug: Data received: {data}")

        # Extract start_date and end_date from the input data
        start_date = data['start_date']
        end_date = data['end_date']
        print(start_date)
        print(end_date)
        year, month, day = map(int, start_date.split("/"))
        new_start_date = datetime.datetime(year, 1, 1)
        new_end_date = datetime.datetime(year, month, day)
        formatted_start_date = new_start_date.strftime("%Y/%m/%d")
        formatted_end_date = new_end_date.strftime("%Y/%m/%d")
        print(formatted_start_date)
        print(formatted_end_date)

        pending_milestone = request.env['sale.order.line'].search(
            [('start_date_order', '>', formatted_start_date), ('start_date_order', '<=', formatted_end_date)])
        pending_data = 0.0
        pending_data_dict = {}
        for pending in pending_milestone:
            if pending.pending_boolean_field:
                sale_order = pending.order_id  # Get the associated sale order
                sale_order_name = sale_order.name
                pending_data_dict[sale_order_name] = pending.price_subtotal
                pending_data += pending.price_subtotal
        print(pending_data_dict)

        #invoice filtering previous month
        previous_invoice_dict = {}
        previous_invoice = request.env['account.move'].search(
            [('invoice_date', '>', formatted_start_date), ('invoice_date', '<=', formatted_end_date)])
        for invoice in previous_invoice:
            previous_invoice_dict[invoice.invoice_origin] = invoice.invoice_date.month

        print(previous_invoice_dict,'previous')
        year, month, day = map(int, end_date.split("/"))
        end_date_datetime = datetime.date(year, month, day)

        for key in previous_invoice_dict:
            if end_date_datetime.month > previous_invoice_dict[key]:
                if key in pending_data_dict:
                    pending_data = pending_data - pending_data_dict[key]

        #invoice filtering
        invoice_current_month = request.env['account.move'].search(
            [('invoice_date', '>', start_date), ('invoice_date', '<=', end_date)])
        current_invoice_data_dict = {}
        for inovice in invoice_current_month:
            current_invoice_data_dict[inovice.invoice_origin] = inovice.invoice_date.month
        print(current_invoice_data_dict)
        # Initialize variables to store the sum of price_subtotal and price_total

        subtotal_sum = 0.0
        total_sum = 0.0
        # Query sale.order.line records based on start_date and end_date
        sale_order_lines = request.env['sale.order.line'].search(
            [('start_date_order', '>', start_date), ('start_date_order', '<=', end_date)])
        # current_invoice_data_dict = {}
        # Iterate through the sale order lines and calculate the sums
        for line in sale_order_lines:
            subtotal_sum += line.price_subtotal
            total_sum += line.price_total
            # if line.invoice_status == 'invoiced':
            #     current_invoice_data_dict[line.id] = line.price_subtotal
        common_keys = set(pending_data_dict.keys()) & set(current_invoice_data_dict.keys())
        # print('common key:',common_keys)
        year, month, day = map(int, end_date.split("/"))
        end_date_datetime = datetime.datetime(year, month, day)
        value = 0.0
        for key in common_keys:

            value += pending_data_dict[key]
            # if end_date_datetime.month > current_invoice_data_dict[key]:
            #     pending_data = pending_data - pending_data_dict[key]
        print(value)

        # print(end_date_datetime.month, 'month')


        return {
            'subtotal_sum': subtotal_sum,
            'total_sum': total_sum,
            'pending_data': pending_data,
            'achieved_data': value,
        }