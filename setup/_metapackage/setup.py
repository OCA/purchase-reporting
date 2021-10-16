import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-purchase-reporting",
    description="Meta package for oca-purchase-reporting Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-purchase_reporting_weight',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 9.0',
    ]
)
