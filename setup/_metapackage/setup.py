import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo8-addons-oca-purchase-reporting",
    description="Meta package for oca-purchase-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo8-addon-purchase_order_webkit',
        'odoo8-addon-purchase_order_webkit_with_notes',
        'odoo8-addon-purchase_stock_analysis',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
