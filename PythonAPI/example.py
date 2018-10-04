#!/usr/bin/env python

import sys

sys.path.append(
    'PythonAPI/carla-0.9.0-py%d.%d-linux-x86_64.egg' % (sys.version_info.major,
                                                        sys.version_info.minor))

import carla

import os
import random
import time


def main():
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    print('client version: %s' % client.get_client_version())
    print('server version: %s' % client.get_server_version())

    world = client.get_world()

    blueprint_library = world.get_blueprint_library()

    vehicle_blueprints = blueprint_library.filter('vehicle')

    actor_list = []

    try:

        bp = random.choice(vehicle_blueprints)

        transform = carla.Transform(
            carla.Location(x=180.0, y=199.0, z=40.0),
            carla.Rotation(yaw=0.0))
        vehicle = world.spawn_actor(bp, transform)
        vehicle.set_autopilot()

        camera_bp = blueprint_library.find('sensor.camera.semantic_segmentation')
        camera_transform = carla.Transform(carla.Location(x=0.4, y=0.0, z=1.4))
        camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        actor_list.append(camera)

        def save_the_fuck_out_of_this_image(image):
            n = image.frame_number
            image.save_to_disk('_out/%06d.png' % n)
            image.save_to_disk('_out/%06d.jpeg' % n)
            image.save_to_disk('_out/%06d.jpg' % n)
            image.save_to_disk('_out/%06d.tiff' % n)
            image.save_to_disk('_out/%06d_depth.jpeg' % n, color_converter='depth')
            image.save_to_disk('_out/%06d_depth.png' % n, color_converter='depth')
            image.save_to_disk('_out/%06d_depth.tiff' % n, color_converter='depth')
            image.save_to_disk('_out/%06d_logdepth.jpeg' % n, color_converter='logdepth')
            image.save_to_disk('_out/%06d_logdepth.png' % n, color_converter='logdepth')
            image.save_to_disk('_out/%06d_logdepth.tiff' % n, color_converter='logdepth')
            image.save_to_disk('_out/%06d_semseg.jpeg' % n, color_converter='semseg')
            image.save_to_disk('_out/%06d_semseg.png' % n, color_converter='semseg')
            image.save_to_disk('_out/%06d_semseg.tiff' % n, color_converter='semseg')
            image.save_to_disk('_out/%06d_unknown' % n)

        camera.listen(save_the_fuck_out_of_this_image)

        time.sleep(10)

    finally:

        for actor in actor_list:
            actor.destroy()


if __name__ == '__main__':

    main()
