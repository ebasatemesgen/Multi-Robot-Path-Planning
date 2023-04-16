execute_process(COMMAND "/home/eba/multi_agent_ws/build/srv_tools/launch_tools/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/eba/multi_agent_ws/build/srv_tools/launch_tools/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
