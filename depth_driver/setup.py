from setuptools import setup

package_name = 'depth_driver'
examples = 'depth_driver.examples'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name, examples],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abdallah',
    maintainer_email='elsherbiny2023@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'kinect_v1_depth = depth_driver.examples.kinect_v1_depth_ex:main',
            'kinect_v2_depth = depth_driver.examples.kinect_v2_depth_ex:main',
            'mono_depth = depth_driver.examples.mono_depth_ex:main',
            'stereo_depth_publisher = depth_driver.examples.stereo_depth_publisher_ex:main',
            'stereo_depth_subscriber = depth_driver.examples.stereo_depth_subscriber_ex:main',
            # 'stereo_depth1 = depth_driver.stereo_depth.stereo_estimation:main',
            # 'stereo_depth2 = depth_driver.stereo_depth.stereo_2nd:main',
            # 'stereo_depth3 = depth_driver.stereo_depth.stereo_3rd:main',
            # 'stereo_depth4 = depth_driver.stereo_depth.stereo_4th:main',
            # 'stereo_depth5 = depth_driver.stereo_depth.depth_map.realtime:main',
        ],
    },
)
