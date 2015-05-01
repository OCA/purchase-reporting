## -*- coding: utf-8 -*-
<html>
<head>
     <style type="text/css">
        ${css}

.list_main_table {
border:thin solid #E3E4EA;
text-align:center;
border-collapse: collapse;
}
table.list_main_table {
    margin-top: 20px;
}
.list_main_headers {
    padding: 0;
}
.list_main_headers th {
    border: thin solid #000000;
    padding-right:3px;
    padding-left:3px;
    background-color: #EEEEEE;
    text-align:center;
    font-size:12;
    font-weight:bold;
}
.list_main_table td {
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_main_lines
.list_main_lines td,
.list_main_lines td {
    border-bottom:thin solid #EEEEEE
}
.nobreak {
    page-break-inside: avoid;
}
caption.formatted_note {
    text-align:left;
    border-right:thin solid #EEEEEE;
    border-left:thin solid #EEEEEE;
    border-top:thin solid #EEEEEE;
    padding-left:10px;
    font-size:11;
    caption-side: bottom;
}
caption.formatted_note p {
    margin: 0;
}
.address {
    font-size: 12px;
    margin-left: 350px;
    margin-right: 120px;
    float: right;
}
.req_line_col1 {
    width: 60%;
    text-align:left;
    vertical-align:top;
}
.req_line_col2 {
    width: 20%;
    text-align:center;
    vertical-align:top;
}
.req_line_col3 {
    width: 20%;
    text-align:center;
    vertical-align:top;
}
.po_line_col1 {
    width: 60%;
    text-align:left;
    vertical-align:top;
}
.po_line_col2 {
    width: 20%;
    text-align:center;
    vertical-align:top;
}
.po_line_col3 {
    width: 20%;
    text-align:center;
    vertical-align:top;
}
    </style>

</head>
<body>
    <%page expression_filter="entity"/>

    <%def name="address(partner, commercial_partner=None)">
        <%doc>
            XXX add a helper for address in report_webkit module as this won't be suported in v8.0
        </%doc>
        <% company_partner = False %>
        %if commercial_partner:
            %if commercial_partner.id != partner.id:
                <% company_partner = commercial_partner %>
            %endif
        %elif partner.parent_id:
            <% company_partner = partner.parent_id %>
        %endif

        %if company_partner:
            <tr><td class="name">${company_partner.name or ''}</td></tr>
            <tr><td>${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n")[1:] %>
        %else:
            <tr><td class="name">${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
            <% address_lines = partner.contact_address.split("\n") %>
        %endif
        %for part in address_lines:
            % if part:
                <tr><td>${part}</td></tr>
            % endif
        %endfor
    </%def>

    %for requisition in objects :
        <h3 style="clear: both; padding-top: 20px;">
        	${_(u'Requisition') } ${requisition.name}
        </h3>
        <table class="basic_table" width="100%">
            <tr>
                <th style="text-align:center">${_("Requisition Reference")}</th>
                <th class="date">${_("Requisition Date")}</th>
                <th style="text-align:center">${_("Type")}</th>
                <th style="text-align:center">${_("Origin")}</th>
            </tr>
            <tr>
                <td style="text-align:center">${requisition.name}</td>
                <td class="date">${formatLang(requisition.date_start, date_time=True)}</td>
                <td style="text-align:center">${requisition.exclusive == 'multiple' and 'Multiple Requisitions' or requisition.exclusive == 'exclusive' and 'Purchase Requisitions (exclusive)'}</td>
                <th style="text-align:center">${requisition.origin or ''}</th>
            </tr>
        </table>
        <h4 style="clear: both; padding-top: 20px;">
            ${_(u'Product Detail')}
        </h4>
        <table class="list_main_table" width="100%" >
            <thead>
              <tr class="list_main_headers">
                <th class="req_line_col1">${_("Description")}</th>
                <th class="req_line_col2">${_("Qty")}</th>
                <th class="req_line_col3">${_("UoM")}</th>
              </tr>
            </thead>
            <tbody>
            %for line in requisition.line_ids :
              <tr class="list_main_lines">
                <td class="req_line_col1">${line.name.replace('\n','<br/>') or '' | n}</td>
                <td style="text-align:center" class="amount req_line_col2">${formatLang(line.product_qty)}</td>
                <td style="text-align:center" class="req_line_col3">${line.product_uom_id.name}</td>
              </tr>
           %endfor
            </tbody>
        </table>
        %if requisition.purchase_ids:
            <h4 style="clear: both; padding-top: 20px;">
                ${_(u'Quotation Detail')}
            </h4>
            <table class="list_main_table" width="100%" >
                <thead>
                  <tr class="list_main_headers">
                    <th class="po_line_col1">${_("Supplier")}</th>
                    <th class="po_line_col2">${_("Date Ordered")}</th>
                    <th class="po_line_col3">${_("Order Reference")}</th>
                  </tr>
                </thead>
                <tbody>
                %for purchase in requisition.purchase_ids :
                  <tr class="list_main_lines">
                    <td class="po_line_col1">${purchase.partner_id.name}</td>
                    <td style="text-align:center" class="po_line_col2">${formatLang(purchase.date_order, date=True)}</td>
                    <td style="text-align:center" class="po_line_col3">${purchase.name}</td>
                  </tr>
               %endfor
                </tbody>
            </table>
        %endif
        <p style="page-break-after:always"/>
        <br/>
	%endfor
</body>
</html>
