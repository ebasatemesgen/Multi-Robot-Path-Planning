#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/eba/multi_agent_ws/src/srv_tools/plot_tools"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/eba/multi_agent_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/eba/multi_agent_ws/install/lib/python2.7/dist-packages:/home/eba/multi_agent_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/eba/multi_agent_ws/build" \
    "/usr/bin/python2" \
    "/home/eba/multi_agent_ws/src/srv_tools/plot_tools/setup.py" \
     \
    build --build-base "/home/eba/multi_agent_ws/build/srv_tools/plot_tools" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/eba/multi_agent_ws/install" --install-scripts="/home/eba/multi_agent_ws/install/bin"
