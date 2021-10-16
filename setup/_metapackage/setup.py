import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-purchase-reporting",
    description="Meta package for oca-purchase-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-purchase_incoming_products',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
