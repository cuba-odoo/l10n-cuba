# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class PartnerBalance(models.AbstractModel):
    _name = 'report.l10n_cu_reports.report_partnerbalance'
    _description = 'Partner Balance'

    def _lines(self, data):
        tables_where_params = self.env['account.move.line'].with_context(data['form'].get('used_context', {}))._query_get()
        params = [tuple(data['ids']), tuple(data['computed']['result_selection'])] + tables_where_params[2]

        # print(params)

        # print(tables_where_params[0])
        # print(tables_where_params[1])
        # print(tables_where_params[2])
        query = """
                    SELECT p.ref,account_move_line.account_id,ac.name AS account_name,ac.code AS code,p.name, sum(debit) AS debit, sum(credit) AS credit,
                    CASE WHEN sum(debit) > sum(credit)
                        THEN sum(debit) - sum(credit)
                        ELSE 0
                    END AS sdebit,
                    CASE WHEN sum(debit) < sum(credit)
                        THEN sum(credit) - sum(debit)
                        ELSE 0
                    END AS scredit

            FROM
            account_move_line LEFT JOIN res_partner p ON (account_move_line.partner_id=p.id)
            JOIN account_account ac ON (account_move_line.account_id = ac.id)
            JOIN account_move as account_move_line__move_id ON (account_move_line__move_id.id = account_move_line.move_id)
            WHERE (ac.id in %s) and (ac.internal_type IN %s)       
            AND """ + tables_where_params[1] + """
            GROUP BY p.id, p.ref, p.name,account_move_line.account_id,ac.name,ac.code
            ORDER BY account_move_line.account_id,p.name """

        # print(tables_where_params[2])

        # arg_list = (tuple(data['ids']), tuple(data['computed'].get('move_state')))
        # arg_list += (tuple(data['computed'].get('result_selection')), tuple(data['form'].get('journal_ids', {})))


        self.env.cr.execute(query, tuple(params))
        res = self.env.cr.dictfetchall()

        if data['form']['display_partner'] == 'non-zero_balance':
            full_account = [r for r in res if r['sdebit'] > 0 or r['scredit'] > 0]
        else:
            full_account = [r for r in res]

        for rec in full_account:
            if not rec.get('name', False):
                rec.update({'name': _('Unknown Partner')})

        ## We will now compute Total
        subtotal_row = self._add_subtotal(full_account)
        return subtotal_row

    def _add_subtotal(self, cleanarray):
        i = 0
        completearray = []
        tot_debit = 0.0
        tot_credit = 0.0
        tot_scredit = 0.0
        tot_sdebit = 0.0
        # tot_enlitige = 0.0
        for r in cleanarray:
            # For the first element we always add the line
            # type = 1 is the line is the first of the account
            # type = 2 is an other line of the account
            if i==0:
                # We add the first as the header
                #
                ##
                new_header = {}
                new_header['ref'] = ''
                new_header['name'] = r['account_name']
                new_header['code'] = r['code']
                new_header['debit'] = r['debit']
                new_header['credit'] = r['credit']
                new_header['scredit'] = tot_scredit
                new_header['sdebit'] = tot_sdebit
                # new_header['enlitige'] = tot_enlitige
                new_header['balance'] = r['debit'] - r['credit']
                new_header['type'] = 3
                ##
                completearray.append(new_header)
                #
                r['type'] = 1
                r['balance'] = float(r['sdebit']) - float(r['scredit'])

                completearray.append(r)
                #
                tot_debit = r['debit']
                tot_credit = r['credit']
                tot_scredit = r['scredit']
                tot_sdebit = r['sdebit']
                # tot_enlitige = (r['enlitige'] or 0.0)
                #
            else:
                if cleanarray[i]['account_id'] != cleanarray[i-1]['account_id']:

                    new_header['debit'] = tot_debit
                    new_header['credit'] = tot_credit
                    new_header['scredit'] = tot_scredit
                    new_header['sdebit'] = tot_sdebit
                    # new_header['enlitige'] = tot_enlitige
                    new_header['balance'] = float(tot_sdebit) - float(tot_scredit)
                    # new_header['type'] = 3
                    # we reset the counter
                    tot_debit = r['debit']
                    tot_credit = r['credit']
                    tot_scredit = r['scredit']
                    tot_sdebit = r['sdebit']
                    # tot_enlitige = (r['enlitige'] or 0.0)
                    #
                    ##
                    new_header = {}
                    new_header['ref'] = ''
                    new_header['name'] = r['account_name']
                    new_header['code'] = r['code']
                    new_header['debit'] = tot_debit
                    new_header['credit'] = tot_credit
                    new_header['scredit'] = tot_scredit
                    new_header['sdebit'] = tot_sdebit
                    # new_header['enlitige'] = tot_enlitige
                    new_header['balance'] = float(tot_sdebit) - float(tot_scredit)
                    new_header['type'] = 3
                    ##get_fiscalyear
                    ##

                    completearray.append(new_header)
                    ##
                    #
                    r['type'] = 1
                    #
                    r['balance'] = float(r['sdebit']) - float(r['scredit'])

                    completearray.append(r)

                if cleanarray[i]['account_id'] == cleanarray[i-1]['account_id']:
                    # we reset the counter

                    new_header['debit'] = tot_debit
                    new_header['credit'] = tot_credit
                    new_header['scredit'] = tot_scredit
                    new_header['sdebit'] = tot_sdebit
                    # new_header['enlitige'] = tot_enlitige
                    new_header['balance'] = float(tot_sdebit) - float(tot_scredit)
                    new_header['type'] = 3

                    tot_debit = tot_debit + r['debit']
                    tot_credit = tot_credit + r['credit']
                    tot_scredit = tot_scredit + r['scredit']
                    tot_sdebit = tot_sdebit + r['sdebit']
                    # tot_enlitige = tot_enlitige + (r['enlitige'] or 0.0)

                    new_header['debit'] = tot_debit
                    new_header['credit'] = tot_credit
                    new_header['scredit'] = tot_scredit
                    new_header['sdebit'] = tot_sdebit
                    # new_header['enlitige'] = tot_enlitige
                    new_header['balance'] = float(tot_sdebit) - float(tot_scredit)

                    #
                    r['type'] = 2
                    #
                    r['balance'] = float(r['sdebit']) - float(r['scredit'])
                    #

                    completearray.append(r)

            i = i + 1
        return completearray

    @api.model
    def _get_report_values(self, docids, data=None):

        data['computed'] = {}
        data['computed']['move_state'] = ['draft', 'posted']
        if data['form'].get('target_move', 'all') == 'posted':
            data['computed']['move_state'] = ['posted']
        # display_partner = data['form'].get('display_partner')
        # data['computed']['display_partner'] = display_partner


        # target_move = data['form'].get('target_move', 'all')
        if data['form']['result_selection'] == 'customer':
            data['computed']['result_selection'] = ['receivable']
        elif data['form']['result_selection'] == 'supplier':
            data['computed']['result_selection'] = ['payable']
        else:
            data['computed']['result_selection'] = ['payable', 'receivable']


        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('l10n_cu_reports.report_partnerbalance')

        docargs = {
            'doc_model': report.model,
            'data': data,
            'lines': self._lines,
        }
        return docargs