from __future__ import print_function

import itertools
from app import motive, RatcaveApp
import ratcave as rc
import cfg
import pyglet
import events
import subprocess
from psychopy.gui import DlgFromDict
import sys
from datetime import datetime
import utils
from pypixxlib import propixx
from numpy import random

projector = propixx.PROPixx()

# Show User-Defined Experiment Settings
conditions = {'RAT': cfg.RAT,
              'EXPERIMENTER': cfg.EXPERIMENTER,
              'PAPER_LOG_CODE': cfg.PAPER_LOG_CODE,
              }

dlg = DlgFromDict(conditions, title='{} Experiment Settings'.format(cfg.VR_ACUITY_EXPERIMENT_NAME),
                  order=['RAT', 'EXPERIMENTER', 'PAPER_LOG_CODE'])
if dlg.OK:
    log_code = dlg.dictionary['PAPER_LOG_CODE']
    if not dlg.dictionary['RAT'].lower() in ['test', 'demo']:
        if len(log_code) != 7 or log_code[3] != '-':
            raise ValueError("Invalid PAPER_LOG_CODE.  Please try again.")
        subprocess.Popen(['holdtimer'])  # Launch the timer program

    dlg.dictionary['EXPERIMENT'] = cfg.VR_ACUITY_EXPERIMENT_NAME
    cfg.__dict__.update(dlg.dictionary)
else:
    sys.exit()


projector.setSleepMode(not cfg.PROJECTOR_TURNED_ON)
projector.setLampLED(cfg.PROJECTOR_LED_ON)
proj_brightness = cfg.VR_OBJECT_PROJECTOR_LED_INTENSITY if not 'demo' in cfg.RAT.lower() else '100.0'
projector.setLedIntensity(proj_brightness)

# Create Virtual Scenes
object_reader = rc.WavefrontReader(rc.resources.obj_primitives)
cylinder = object_reader.get_mesh('Cylinder', scale=.6)
cylinder.position.xyz =cfg.VR_ACUITY_CYLINDER_POSITION
cylinder.uniforms['diffuse'] = cfg.VR_ACUITY_LIGHTING_DIFFUSE
cylinder.uniforms['specular'] = cfg.VR_ACUITY_LIGHTING_SPECULAR
cylinder.uniforms['spec_weight'] = cfg.VR_ACUITY_LIGHTING_SPEC_WEIGHT
cylinder.uniforms['ambient'] = cfg.VR_ACUITY_LIGHTING_AMBIENT
# cylinder.uniforms['flat_shading'] = cfg.VR_ACUITY_LIGHTING_FLAT_SHADING
cylinder.texture = rc.Texture.from_image(img_filename=cfg.VR_ACUITY_CYLINDER_TEXTURE)
cylinder.speed = 5.
vr_scene = rc.Scene(meshes=[cylinder], name="Cylinder Scene")
cylinder.arrays[2][:] *= 2




# Configure Ratcave App and register the virtual Scenes.
app = RatcaveApp(arena_objfile=cfg.ARENA_FILENAME, projector_file=cfg.PROJECTOR_FILENAME,
                 fullscreen=cfg.FULLSCREEN, screen=cfg.SCREEN, antialiasing=cfg.ANTIALIASING,
                 fps_mode=cfg.FIRST_PERSON_MODE)
app.set_mouse_visible(cfg.MOUSE_CURSOR_VISIBLE)
app.arena.uniforms['flat_shading'] = cfg.ARENA_LIGHTING_FLAT_SHADING

app.register_vr_scene(vr_scene)
app.current_vr_scene = vr_scene


circle = object_reader.get_mesh('Circle', scale=.2)
circle.parent = app.arena
circle.position.xyz = 0., 0., 0.
circle.uniforms['diffuse'] = .5, .5, .5
circle.uniforms['flat_shading'] = True
circle.rotation.x = 90
app.active_scene.meshes.append(circle)

cylinder_speed = 4.



# Build experiment event sequence
seq = []
for speed in random.permutation(cfg.VR_ACUITY_CYLINDER_SPEEDS):
    for direction in [1, -1]:
        phase_seq = [
            events.update_attribute(cylinder, 'speed', speed * direction),
            events.wait_duration(cfg.VR_ACUITY_PHASE_DURATION_SECS),
        ]
        seq.extend(phase_seq)
seq.append(events.close_app(app=app))

# # Make logfiles and set filenames
# if cfg.RAT.lower() not in ['demo']:
#     now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#     filename = '{expname}_{datetime}_{RAT}_{OBJECT_TYPE}_{FAMILIAR_POSITION}_{NOVEL_POSITION}_{object_name}_{person}_{log_code}'.format(
#         expname=cfg.VR_ACUITY_EXPERIMENT_NAME, datetime=now, RAT=cfg.RAT,
#         FAMILIAR_POSITION=cfg.VR_SPATIAL_NOVELTY_FAMILIAR_POSITION,
#         NOVEL_POSITION=cfg.VR_SPATIAL_NOVELTY_NOVEL_POSITION,
#         OBJECT_TYPE=cfg.VR_SPATIAL_NOVELTY_OBJECT_TYPE,
#         object_name=cfg.VR_SPATIAL_NOVELTY_OBJECT_NAME,
#         person=cfg.EXPERIMENTER[0:3].upper(),
#         log_code=cfg.PAPER_LOG_CODE)
#     utils.create_and_configure_experiment_logs(filename=filename, motive_client=motive,
#                                                exclude_subnames=['WALL', 'CLIFF', 'OBJECT'])

def rotate_cylinder(dt):
    global cylinder
    cylinder.rotation.y += cylinder.speed * dt
pyglet.clock.schedule(rotate_cylinder)


exp = events.chain_events(seq, log=True, motive_client=motive)
exp.next()




# Schedule the event sequence and run the VR App!
pyglet.clock.schedule(exp.send)
app.run()
