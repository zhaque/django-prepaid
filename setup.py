from setuptools import setup, find_packages

setup(name="django-prepaid",
           version="0.1",
           description="Django application supporting expiring units",
           author="SaaS kit",
           author_email="admin@saaskit.org",
           packages=find_packages(),
           include_package_data=True,
)

