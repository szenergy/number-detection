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


generate_messages(
  DEPENDENCIES
    geometry_msgs
    sensor_msgs
    std_msgs
)

install(DIRECTORY
launch
DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

catkin_package()

include_directories()