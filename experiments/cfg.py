import itertools as it

experiments = ['cliff', 'wall', 'object_exploration']
rats = ['Test'] + ['VR-{}{}'.format(cage, num) for cage, num in it.product(range(1, 6), 'AB')]

# General settings
ARENA_FILENAME = './assets/arena3uv.obj'
ARENA_LIGHTING_DIFFUSE = 1., 1., 1.
ARENA_LIGHTING_SPECULAR = 0., 0., 0.
ARENA_LIGHTING_TEXTURE = './assets/uvgrid_bw.png'
ARENA_LIGHTING_FLAT_SHADING = True
PROJECTOR_FILENAME = './calibration/p2.pickle'
SCREEN = 1
FULLSCREEN = True

# Cliff experiment settings
CLIFF_FILENAME = './assets/viscliff3b.obj'
CLIFF_TYPE = 'Real'  # or VR, or Static
CLIFF_SIDE = 'R' # L or R
CLIFF_OBJECT_L = 'virArena'
CLIFF_OBJECT_R = 'virArena2'
CLIFF_OBJECT_REAL = 'RealArena'

# Wall experiment settings
VR_WALL_VISIBLE = True
VR_WALL_X_OFFSET = .0
VR_WALL_Y_OFFSET = .28
VR_WALL_SCALE = .5
VR_WALL_Y_ROTATION = 98.
VR_WALL_LIGHTING_DIFFUSE = 1., 1., 1.
VR_WALL_LIGHTING_SPECULAR = 0., 0., 0.
VR_WALL_LIGHTING_AMBIENT = 0., 0., 0.  #1., 1., 1.
VR_WALL_LIGHTING_TEXTURE = ARENA_LIGHTING_TEXTURE
VR_WALL_LIGHTING_FLAT_SHADING = True
VR_WALL_PHASE_1_DURATION_SECS = 1. #60
VR_WALL_PHASE_2_DURATION_SECS = 1.#60 * 4
VR_WALL_PHASE_3_DURATION_SECS = 100. #60 * 4
VR_WALL_PHASE_4_DURATION_SECS = 2 #60 * 4

# Object experiment settings
CIRCLE_SCALE = .07
POSITION_L = .230, -0.143, -.06
POSITION_R = -.195, -.14, .015#-.205, -.14, .015
VR_OBJECTS_FILENAME = './assets/Eng_AllObjs1.obj'
VR_OBJECT_VISIBLE = True
VR_OBJECT_NAMES = ['Snake', 'Torus', 'Monkey', 'Masher', 'Moon', 'Pyramid', 'Mine']
VR_OBJECT_NAME = 'Mine'
VR_OBJECT_SCALE = .01
VR_OBJECT_SIDE = 'L'
VR_OBJECT_LIGHTING_DIFFUSE = (1.3,) * 3
VR_OBJECT_LIGHTING_SPECULAR = ARENA_LIGHTING_SPECULAR
VR_OBJECT_LIGHTING_AMBIENT = 0.3, 0.3, 0.3# 1., 1., 1.
VR_OBJECT_LIGHTING_FLAT_SHADING = False
VR_OBJECT_LIGHTING_TEXTURE = None
VR_OBJECT_PHASE_1_DURATION_SECS = VR_WALL_PHASE_1_DURATION_SECS
VR_OBJECT_PHASE_2_DURATION_SECS = VR_WALL_PHASE_2_DURATION_SECS
VR_OBJECT_PHASE_3_DURATION_SECS = VR_WALL_PHASE_3_DURATION_SECS
VR_OBJECT_PHASE_4_DURATION_SECS = VR_WALL_PHASE_4_DURATION_SECS