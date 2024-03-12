This module backports the Blanket order report feature from Odoo v15.0.

In v14.0 the report from purchase requisition module is meant to be used only for
call for tenders although it could be used for Blanket orders as well.

This module changes the title printed on the report according to agreement type,
and displays the price unit on the lines in case the type is a blanket order.
