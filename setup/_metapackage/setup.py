import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-purchase-reporting",
    description="Meta package for oca-purchase-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-purchase_backorder>=16.0dev,<16.1dev',
        'odoo-addon-purchase_comment_template>=16.0dev,<16.1dev',
        'odoo-addon-purchase_report_date_format>=16.0dev,<16.1dev',
        'odoo-addon-purchase_report_payment_term>=16.0dev,<16.1dev',
        'odoo-addon-purchase_report_shipping_address>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
