## -*- coding: utf-8 -*-
<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')

    %>

    %for purch in objects :
        <%
              quotation = purch.state == 'draft'
        %>

        <% setLang(purch.partner_id.lang) %>
        <div class="address">
            <table class="recipient">
                <tr><td class="name">${purch.partner_id.title and purch.partner_id.title.name or ''}  ${purch.partner_id.name }</td></tr>
                <tr><td>${purch.partner_address_id.street or ''}</td></tr>
                <tr><td>${purch.partner_address_id.street2 or ''}</td></tr>
                <tr><td>${purch.partner_address_id.zip or ''} ${purch.partner_address_id.city or ''}</td></tr>
                %if purch.partner_address_id.country_id :
                <tr><td>${purch.partner_address_id.country_id.name or ''} </td></tr>
                %endif
                %if purch.partner_address_id.phone :
                <tr><td>${_("Tel")}: ${purch.partner_address_id.phone}</td></tr>
                %endif
                %if purch.partner_address_id.fax :
                <tr><td>${_("Fax")}: ${purch.partner_address_id.fax}</td></tr>
                %endif
                %if purch.partner_address_id.email :
                <tr><td>${_("E-mail")}: ${purch.partner_address_id.email}</td></tr>
                %endif
                %if purch.partner_id.vat :
                <tr><td>${_("VAT")}: ${purch.partner_id.vat}</td></tr>
                %endif
            </table>

            %if purch.dest_address_id:
                <table class="shipping">
                    <tr><td class="address_title">${_("Shipping address:")}</td></tr>
                    <tr><td>${purch.partner_id.title and purch.partner_id.title.name or ''}  ${purch.partner_id.name }</td></tr>
                    <tr><td>${purch.dest_address_id.street or ''}</td></tr>
                    <tr><td>${purch.dest_address_id.street2 or ''}</td></tr>
                    <tr><td>${purch.dest_address_id.zip or ''} ${purch.dest_address_id.city or ''}</td></tr>
                    %if purch.dest_address_id.state_id:
                    <tr><td>${purch.dest_address_id.state_id.name or ''} </td></tr>
                    %endif
                    %if purch.dest_address_id.country_id:
                    <tr><td>${purch.dest_address_id.country_id.name or ''} </td></tr>
                    %endif
                </table>
            %endif
        </div>

        <h1 style="clear:both; padding-top: 20px;">${quotation and _(u'Quotation N°') or _(u'Purchase Order N°') } ${purch.name}</h1>

        <table class="basic_table" width="100%">
            <tr>
                <td>${_("Document")}</td>
                <td>${_("Your Order Reference")}</td>
                <td>${_("Date Ordered")}</td>
                <td>${_("Validated by")}</td>
            </tr>
            <tr>
                <td>${purch.name}</td>
                <td>${purch.partner_ref or ''}</td>
                <td>${formatLang(purch.date_order, date=True)}</td>
                <td>${purch.validator and purch.validator.name or ''  }</td>
            </tr>
        </table>

        <table class="list_table" width="100%" style="margin-top: 30px;">
            <thead>
                <tr>
                    <th>${_("Description")}</th>
                    <th>${_("Taxes")}</th>
                    <th>${_("Date Req.")}</th>
                    <th class="amount">${_("Qty")}</th>
                    <th class="amount">${_("Unit Price")}</th>
                    <th class="amount">${_("Net Price")}</th>
                </tr>
            </thead>
            <tbody>
            %for line in purch.order_line :
                <tr class="line">
                    <td>${line.name}</td>
                    <td>${ ', '.join([ tax.name or '' for tax in line.taxes_id ])}</td>
                    <td>${formatLang(line.date_order, date=True)}</td>
                    <td class="amount">${line.product_qty} ${line.product_uom.name}</td>
                    <td class="amount">${formatLang(line.price_unit, digits=get_digits(dp='Purchase Price'))}</td>
                    <td class="amount">${formatLang(line.price_subtotal, digits=get_digits(dp='Purchase Price'))} ${purch.pricelist_id.currency_id.symbol}</td>
                </tr>
                %if line.notes :
                    <tr class="line">
                        <td colspan="6" class="note">${line.notes  | carriage_returns}</td>
                    </tr>
                %endif
            %endfor
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="4" style="border-style:none"/>
                    <td style="border-top:2px solid"><b>${_("Net Total:")}</b></td>
                    <td class="amount" style="border-top:2px solid;">${formatLang(purch.amount_untaxed, digits=get_digits(dp='Purchase Price'))} ${purch.pricelist_id.currency_id.symbol}</td>
                </tr>
                <tr>
                    <td colspan="4" style="border-style:none"/>
                    <td style="border-style:none"><b>${_("Taxes:")}</b></td>
                    <td class="amount">${formatLang(purch.amount_tax, digits=get_digits(dp='Purchase Price'))} ${purch.pricelist_id.currency_id.symbol}</td>
                </tr>
                <tr>
                    <td colspan="4" style="border-style:none"/>
                    <td style="border-top:2px solid"><b>${_("Total:")}</b></td>
                    <td class="amount" style="border-top:2px solid;">${formatLang(purch.amount_total, digits=get_digits(dp='Purchase Price'))} ${purch.pricelist_id.currency_id.symbol}</td>
                </tr>
            </tfoot>
        </table>

        <p style="margin-top: 40px;">${purch.notes or '' | carriage_returns}</p>

        <p style="page-break-after:always"/>
        <br/>
	%endfor
</body>
</html>
