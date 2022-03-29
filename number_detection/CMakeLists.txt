cmake_minimum_required(VERSION 3.0.2)
project(number_detection)


find_package(catkin REQUIRED
  COMPONENTS
    geometry_msgs
    sensor_msgs
    std_msgs
    message_generation)


add_message_files(
  FILES
    BoundingBox.msg
    BoundingBoxes.msg
)


# install python modules by invoking setup.py
catkin_python_setup()


generate_messages(
  DEPENDENCIES
    geometry_msgs
    sensor_msgs
    std_msgs
)


# makes python nodes visible for the launch file
catkin_install_python(
  PROGRAMS 
    src/detect.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})


# makes launch files visible
install(
  DIRECTORY
    launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

catkin_package()

include_directories()