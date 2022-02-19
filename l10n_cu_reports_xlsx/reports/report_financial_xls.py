# -*- coding: utf-8 -*-

from odoo import models


def layout_header(self, workbook, worksheet, data):
    normal = workbook.add_format({'bold': False, 'border': 1})
    normal.set_font_size(10)

    cimg = workbook.add_format({'bold': False})
    cimg.set_top(1)
    cimg.set_left(1)
    worksheet.merge_range('A1:C1', '', cimg)

    worksheet.set_row(0, 50)
    worksheet.set_column(0, 50)

    worksheet.insert_image(0, 0,
                           '/home/burger/src-15.0/burger/l10n_cu_reports_xlsx/static/src/img/escudo_nacional.png',
                           {'x_scale': 1.7, 'y_scale': 1.7})
    cestados = workbook.add_format({'bold': True,
                                    'align': 'vcenter',
                                    'border': 1,
                                    })
    cestados.set_font_size(10)
    cestados.set_text_wrap()
    worksheet.merge_range('D1:E2', "ESTADOS FINANCIEROS", cestados)

    cestado_de_valor = workbook.add_format({'bold': True,
                                            'align': 'vcenter',
                                            'border': 1,
                                            })
    cestado_de_valor.set_font_size(10)
    cestado_de_valor.set_text_wrap()
    worksheet.merge_range('F1:G2', data['form']['account_report_id'][1], cestado_de_valor)

    cpaginado_efe = workbook.add_format({'bold': True,
                                         'align': 'vcenter',
                                         'border': 1,
                                         })
    cpaginado_efe.set_font_size(10)
    cpaginado_efe.set_text_wrap()
    worksheet.merge_range('H1:H2', '(%s)' % data['context']['efe'], cpaginado_efe)

    cmep = workbook.add_format({'bold': False})
    cmep.set_font_size(10)
    cmep.set_left(1)

    worksheet.merge_range('A2:C2', 'Ministerio de Finanzas y Precios', cmep)

    cacumulado_uom = workbook.add_format({'bold': True,
                                          'border': 1,
                                          })
    cacumulado_uom.set_font_size(10)
    worksheet.merge_range('A3:D3', 'INFORME ACUMULADO HASTA:', cacumulado_uom)
    worksheet.merge_range('E3:H3', 'UNIDAD DE MEDIDA:', cacumulado_uom)

    worksheet.merge_range('A4:D4', data['form']['date_to'], normal)
    worksheet.merge_range('E4:H4', 'Pesos cubanos con dos decimales', normal)

    context = data.get('context')
    active_company = self.env["res.company"].browse(context.get('allowed_company_ids'))

    centidad = workbook.add_format({
        'border': 1,
    })
    centidad.set_font_size(10)
    worksheet.merge_range('A5:H5', 'Entidad: %s' % active_company[0].name, centidad)

    ccodigo_entidad = workbook.add_format({
        'border': 1,
        'align': 'center',
    })
    ccodigo_entidad.set_font_size(10)
    worksheet.merge_range('A6:C6', 'Código Entidad', ccodigo_entidad)
    worksheet.merge_range('D6:F6', 'N.A.E', ccodigo_entidad)
    worksheet.merge_range('G6:H6', 'D.P.A', ccodigo_entidad)

    corganismo = workbook.add_format({
        'border': 1,
    })
    corganismo.set_font_size(10)
    worksheet.write('A7', 'ORG', corganismo)
    worksheet.write('B7', 'SUB', corganismo)
    worksheet.write('C7', 'CÓDIGO', corganismo)
    worksheet.merge_range('D7:E7', 'DIVISIÓN', corganismo)
    worksheet.write('F7', 'CLASE', corganismo)
    worksheet.write('G7', 'PROVINCIA', corganismo)
    worksheet.write('H7', 'MUNICIPIO', corganismo)

    worksheet.write('A8', '', corganismo)
    worksheet.write('B8', '', corganismo)
    worksheet.write('C8', active_company[0].company_registry, corganismo)
    worksheet.merge_range('D8:E8', '', corganismo)
    worksheet.write('F8', '', corganismo)
    worksheet.write('G8', active_company[0].state_id and active_company[0].state_id.code or '', corganismo)
    worksheet.write('H8', active_company[0].city, corganismo)


def layout_footer(self, workbook, worksheet, data, row):
    normal = workbook.add_format({'bold': False})
    normal.set_font_size(10)
    ccertificamos = workbook.add_format({
        'border': 1,
        'align': 'justify',
        # 'font': {'size': 10},
    })
    ccertificamos.set_font_size(10)
    # ccertificamos.set_align('justify')
    ccertificamos.set_text_wrap()

    worksheet.merge_range('A%d:B%d' % (row + 1, row + 6),
                          "Certificamos que los datos contenidos en este estado financiero se corresponden"
                          "con las anotaciones contables de acuerdo con las regulaciones vigentes.", ccertificamos)

    cecho_por = workbook.add_format({
        'border': 1,
        'align': 'left',
    })
    cecho_por.set_font_size(10)

    worksheet.merge_range('C%d:D%d' % (row + 1, row + 1), "HECHO POR:", cecho_por)
    worksheet.merge_range('C%d:D%d' % (row + 2, row + 2), "______________________", normal)
    worksheet.merge_range('C%d:D%d' % (row + 3, row + 3), "FIRMA:", normal)
    worksheet.merge_range('C%d:D%d' % (row + 4, row + 5), "______________________", cecho_por)

    caprobado_por = workbook.add_format({
        'border': 1,
        'align': 'left',
    })
    caprobado_por.set_font_size(10)

    worksheet.merge_range('E%d:F%d' % (row + 1, row + 1), "APROBADO POR:", cecho_por)
    worksheet.merge_range('E%d:F%d' % (row + 2, row + 2), "______________________", normal)
    worksheet.merge_range('E%d:F%d' % (row + 3, row + 3), "FIRMA:", normal)
    worksheet.merge_range('E%d:F%d' % (row + 4, row + 5), "______________________", cecho_por)

    cfecha = workbook.add_format({
        'border': 1,
        'align': 'left',
    })
    cfecha.set_font_size(10)
    worksheet.merge_range('G%d:H%d' % (row + 1, row + 1), "FECHA:", cfecha)


class ReportFinancialXlsxBS(models.AbstractModel):
    _name = 'report.l10n_cu_reports_xlsx.report_financial_xls_bs'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_financial']
    _description = 'Report Financial XLSX 5920-04'

    def generate_xlsx_report(self, workbook, data, financial_report):
        account_lines = self.get_account_lines(data.get('form'))
        sheet = workbook.add_worksheet('Estado de Situación (5920-04)')
        sheet.set_margins(0.3, 0.3)
        sheet.center_horizontally()

        layout_header(self, workbook, sheet, data)

        cconcepto = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'vcenter',
        })
        cconcepto.set_align('center')
        cconcepto.set_font_size(10)
        sheet.set_row(8, 30)

        sheet.merge_range('A9:C9', "CONCEPTOS", cconcepto)
        sheet.write('D9:D9', "Filas", cconcepto)
        sheet.write('E9', "N", cconcepto)
        cconcepto.set_text_wrap()
        sheet.write('F9', "Plan Anual", cconcepto)
        sheet.write('G9', "Apertura", cconcepto)
        sheet.write('H9', "Real hasta la fecha", cconcepto)

        cconcepto_body = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'left',
        })
        cconcepto_body.set_font_size(10)
        cconcepto_body.set_text_wrap()

        cnumber = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'right',
        })
        cnumber.set_font_size(10)
        row = 9
        for line in account_lines:
            if line['visible'] and line['level'] != 0:
                sheet.merge_range(row, 0, row, 2, line.get('name'), cconcepto_body)

                sheet.write(row, 3, line.get('sequence'), cnumber)
                sheet.write(row, 4, '', cnumber)
                sheet.write(row, 5, line.get('plan_anual', 0), cnumber)
                sheet.write(row, 6, line.get('apertura', ''), cnumber)
                sheet.write(row, 7, line.get('balance'), cnumber)
                row += 1

        layout_footer(self, workbook, sheet, data, row)

class ReportFinancialXlsxPl(models.AbstractModel):
    _name = 'report.l10n_cu_reports_xlsx.report_financial_xls_pl'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_financial']
    _description = 'Report Financial XLSX 5921-04'

    def generate_xlsx_report(self, workbook, data, financial_report):
        account_lines = self.get_account_lines(data.get('form'))
        sheet = workbook.add_worksheet('Estado de Rendimiento Financiero (5921-04)')
        sheet.set_margins(0.3, 0.3)
        sheet.center_horizontally()

        layout_header(self, workbook, sheet, data)

        cconcepto = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'vcenter',
        })
        cconcepto.set_align('center')
        cconcepto.set_font_size(10)
        sheet.set_row(8, 30)

        sheet.merge_range('A9:C9', "CONCEPTOS", cconcepto)
        sheet.write('D9:D9', "Filas", cconcepto)
        sheet.write('E9', "N", cconcepto)
        cconcepto.set_text_wrap()
        sheet.write('F9', "Plan Anual", cconcepto)
        sheet.write('G9', "Plan hasta la fecha", cconcepto)
        sheet.write('H9', "Real hasta la fecha", cconcepto)

        cconcepto_body = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'left',
        })
        cconcepto_body.set_font_size(10)
        cconcepto_body.set_text_wrap()
        # cconcepto_body.set_hidden()

        cnumber = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'right',
        })
        cnumber.set_font_size(10)
        row = 9
        for line in account_lines:
            if line['visible'] and line['level'] != 0:
                sheet.merge_range(row, 0, row, 2, " {}".format(line.get('name')), cconcepto_body)
                sheet.write(row, 3, line.get('sequence'), cnumber)
                sheet.write(row, 4, '', cnumber)
                sheet.write(row, 5, line.get('plan_anual', 0), cnumber)
                sheet.write(row, 6, line.get('apertura', ''), cnumber)
                sheet.write(row, 7, line.get('balance'), cnumber)
                row += 1

        layout_footer(self, workbook, sheet, data, row)

class ReportFinancialXlsxEGE(models.AbstractModel):
    _name = 'report.l10n_cu_reports_xlsx.report_financial_xls_ege'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_financial']
    _description = 'Report Financial XLSX 5924-04'

    def generate_xlsx_report(self, workbook, data, financial_report):
        account_lines = self.get_account_lines(data.get('form'))
        sheet = workbook.add_worksheet('Estado de Gastos por Elementos (5924-04)')
        sheet.set_margins(0.3, 0.3)
        sheet.center_horizontally()

        layout_header(self, workbook, sheet, data)

        cconcepto = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'vcenter',
        })
        cconcepto.set_align('center')
        cconcepto.set_font_size(10)
        sheet.set_row(8, 30)

        sheet.merge_range('A9:C9', "CONCEPTOS", cconcepto)
        sheet.write('D9:D9', "Filas", cconcepto)
        sheet.write('E9', "N", cconcepto)
        cconcepto.set_text_wrap()
        sheet.write('F9', "Plan Anual", cconcepto)
        sheet.write('G9', "Plan hasta la fecha", cconcepto)
        sheet.write('H9', "Real hasta la fecha", cconcepto)

        cconcepto_body = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'left',
        })
        cconcepto_body.set_font_size(10)
        cconcepto_body.set_text_wrap()

        cnumber = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'right',
        })
        cnumber.set_font_size(10)
        row = 9
        for line in account_lines:
            if line['visible'] and line['level'] != 0:
                sheet.merge_range(row, 0, row, 2, line.get('name'), cconcepto_body)
                sheet.write(row, 3, line.get('sequence'), cnumber)
                sheet.write(row, 4, '', cnumber)
                sheet.write(row, 5, line.get('plan_anual', 0), cnumber)
                sheet.write(row, 6, line.get('apertura', ''), cnumber)
                sheet.write(row, 7, line.get('balance'), cnumber)
                row += 1

        layout_footer(self, workbook, sheet, data, row)


class ReportFinancialXlsxEVAB(models.AbstractModel):
    _name = 'report.l10n_cu_reports_xlsx.report_financial_xls_evab'
    _inherit = ['report.report_xlsx.abstract', 'report.accounting_pdf_reports.report_financial']
    _description = 'Report Financial XLSX 5936-04'

    def generate_xlsx_report(self, workbook, data, financial_report):
        account_lines = self.get_account_lines(data.get('form'))
        sheet = workbook.add_worksheet('Estado de Valor Agregado Bruto (5926-04)')
        sheet.set_margins(0.3, 0.3)
        sheet.center_horizontally()

        layout_header(self, workbook, sheet, data)

        cconcepto = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'vcenter',
        })
        cconcepto.set_align('center')
        cconcepto.set_font_size(10)
        sheet.set_row(8, 30)

        sheet.merge_range('A9:D9', "CONCEPTOS", cconcepto)
        sheet.write('E9:D9', "Filas", cconcepto)
        cconcepto.set_text_wrap()
        sheet.write('F9', "Plan Anual", cconcepto)
        sheet.write('G9', "Plan hasta la fecha", cconcepto)
        sheet.write('H9', "Real hasta la fecha", cconcepto)

        cconcepto_body = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'left',
        })
        cconcepto_body.set_font_size(10)
        cconcepto_body.set_text_wrap()

        cnumber = workbook.add_format({
            'bold': True,
            'border': 1,
            'align': 'right',
        })
        cnumber.set_font_size(10)
        row = 9
        for line in account_lines:
            if line['visible'] and line['level'] != 0:
                sheet.merge_range(row, 0, row, 3, line.get('name'), cconcepto_body)
                sheet.write(row, 4, line.get('sequence'), cnumber)
                sheet.write(row, 5, line.get('plan_anual', 0), cnumber)
                sheet.write(row, 6, line.get('apertura', ''), cnumber)
                sheet.write(row, 7, line.get('balance'), cnumber)
                row += 1

        layout_footer(self, workbook, sheet, data, row)
