import genesis as gs
gs.init(backend=gs.metal)

scene = gs.Scene(
    sim_options=gs.options.SimOptions(),
    viewer_options=gs.options.ViewerOptions(
        res = (2560, 1600),
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
    gs.morphs.MJCF(file='xml/franka_emika_panda/panda.xml'),
)



scene.build()
for i in range(1000):
    scene.step()