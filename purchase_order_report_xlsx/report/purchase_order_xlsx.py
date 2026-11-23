# 2026 Copyright ForgeFlow(https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models

from odoo.addons.report_xlsx_helper.report.report_xlsx_format import (
    FORMATS,
    XLS_HEADERS,
)


class PurchaseOrderXlsx(models.AbstractModel):
    _name = "report.purchase_order_report_xlsx.purchase_order_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Purchase Order XLSX Report"

    def _get_ws_params(self, wb, data, objects):
        col_specs = {}
        col_specs.update(self.env["purchase.order"]._report_xlsx_template())
        wanted_list = self.env["purchase.order"]._report_xlsx_fields()
        title = objects.name if len(objects) == 1 else self.env._("Purchase Orders")
        return [
            {
                "ws_name": title,
                "generate_ws_method": "_generate_purchase_order_ws",
                "title": title,
                "wanted_list": wanted_list,
                "col_specs": col_specs,
            }
        ]

    def _generate_purchase_order_ws(self, workbook, ws, ws_params, data, objects):
        ws.set_landscape()
        ws.fit_to_pages(1, 0)
        ws.set_header(XLS_HEADERS["xls_headers"]["standard"])
        ws.set_footer(XLS_HEADERS["xls_footers"]["standard"])
        self._set_column_width(ws, ws_params)
        row_pos = 0
        row_pos = self._write_ws_title(ws, row_pos, ws_params)
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=FORMATS["format_theader_yellow_left"],
        )
        ws.freeze_panes(row_pos, 0)
        last_col = len(ws_params["wanted_list"]) - 1
        for order in objects:
            for line in order.order_line:
                if line.display_type:
                    ws.merge_range(
                        row_pos,
                        0,
                        row_pos,
                        last_col,
                        line.name,
                        FORMATS["format_theader_yellow_left"],
                    )
                    row_pos += 1
                else:
                    row_pos = self._write_line(
                        ws,
                        row_pos,
                        ws_params,
                        col_specs_section="data",
                        render_space={"order_line": line},
                        default_format=FORMATS["format_tcell_left"],
                    )
