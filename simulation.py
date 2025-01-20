import genesis as gs
import sys

sys.setrecursionlimit(2000)
def run_sim(scene, enable_vis):
    for i in range(1000):
        scene.step()
    if enable_vis:
        scene.viewer.stop()

gs.init(backend=gs.metal)
scene = gs.Scene(
    sim_options=gs.options.SimOptions(),
    viewer_options=gs.options.ViewerOptions(
        res = (3440, 1440),
        camera_pos=(5, 5, 2.5),
        camera_lookat=(-10, -5, 0.5),
        camera_fov=40,
    ),
    show_viewer=True,
    rigid_options=gs.options.RigidOptions(
        dt=0.01,
        gravity=(0.0, 0.0, -10.0),
    ),
)

plane = scene.add_entity(gs.morphs.Plane())
franka = scene.add_entity(
    # morph="/Users/bangseongjin/genesis/doosan-robot/dsr_description/urdf/e0509.urdf"
    # gs.morphs.URDF(file='/Users/bangseongjin/genesis/doosan-robot/dsr_description/urdf/e0509.urdf'),
    gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml'),
)

scene.build()
gs.tools.run_in_another_thread(
    fn=run_sim, 
    args=(scene, True))

scene.viewer.start()

