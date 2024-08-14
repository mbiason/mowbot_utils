from setuptools import find_packages, setup

package_name = 'mowbot_utils'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Matt Biason',
    maintainer_email='mattbiason@gmail.com',
    description='Utils for the mowbot one',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joy_remap_node = mowbot_utils.joy_remap:main'
        ],
    },
)
