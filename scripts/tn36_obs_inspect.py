"""Full inspection of the observation object — all attributes, all frame layers.
Goal: find what information is available to an agent that might correspond to
the animation/cycling behaviour the user sees visually.
"""
import numpy as np
from arc_agi import Arcade, OperationMode
from arcengine import GameAction

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('tn36')
obs = env.observation_space

print("="*60)
print("ALL OBS ATTRIBUTES (initial state)")
print("="*60)
for attr in sorted(dir(obs)):
    if attr.startswith('_'):
        continue
    try:
        val = getattr(obs, attr)
        if callable(val):
            print(f"  {attr}: <method>")
        elif isinstance(val, (list, np.ndarray)):
            if hasattr(val, '__len__'):
                print(f"  {attr}: [{type(val).__name__} len={len(val)}]")
                if isinstance(val, list) and len(val) <= 10:
                    for i, v in enumerate(val):
                        if isinstance(v, (list, np.ndarray)):
                            arr = np.array(v)
                            print(f"    [{i}]: shape={arr.shape}, dtype={arr.dtype}, "
                                  f"min={arr.min()}, max={arr.max()}, "
                                  f"unique={sorted(set(arr.flatten().tolist()))[:10]}")
                        else:
                            print(f"    [{i}]: {v}")
        else:
            print(f"  {attr}: {val}")
    except Exception as e:
        print(f"  {attr}: ERROR({e})")

print("\n" + "="*60)
print("ALL FRAME LAYERS (initial state)")
print("="*60)
print(f"Number of layers: {len(obs.frame)}")
for i, layer in enumerate(obs.frame):
    arr = np.array(layer)
    unique = sorted(set(arr.flatten().tolist()))
    print(f"\nLayer {i}: shape={arr.shape}, unique values={unique}")
    # Show where non-zero (non-background) cells are
    nz = np.argwhere(arr > 0)
    if len(nz):
        print(f"  Non-zero cells: {len(nz)}, "
              f"rows {int(nz[:,0].min())}–{int(nz[:,0].max())}, "
              f"cols {int(nz[:,1].min())}–{int(nz[:,1].max())}")
    else:
        print("  All zero")

# Check for any env methods beyond step/observation_space
print("\n" + "="*60)
print("ENV ATTRIBUTES AND METHODS")
print("="*60)
for attr in sorted(dir(env)):
    if attr.startswith('_'):
        continue
    try:
        val = getattr(env, attr)
        if callable(val):
            print(f"  {attr}: <method>")
        else:
            print(f"  {attr}: {type(val).__name__} = {str(val)[:80]}")
    except Exception as e:
        print(f"  {attr}: ERROR({e})")

# Now click the blue oval and inspect the FULL observation
print("\n" + "="*60)
print("CLICK BLUE OVAL — full obs comparison")
print("="*60)

# Capture initial frame layers
layers_before = [np.array(l).copy() for l in obs.frame]

obs2 = env.step(GameAction.ACTION6, {'x': 36, 'y': 55})

print("\nALL ATTRIBUTES AFTER OVAL CLICK:")
for attr in sorted(dir(obs2)):
    if attr.startswith('_'):
        continue
    try:
        val = getattr(obs2, attr)
        if callable(val):
            continue
        elif isinstance(val, (list, np.ndarray)):
            if hasattr(val, '__len__'):
                # Compare with before if same structure
                val_str = f"[len={len(val)}]"
                print(f"  {attr}: {val_str}")
        else:
            print(f"  {attr}: {val}")
    except Exception as e:
        print(f"  {attr}: ERROR({e})")

layers_after = [np.array(l) for l in obs2.frame]
print(f"\nFrame layers after click: {len(layers_after)}")
for i, (lb, la) in enumerate(zip(layers_before, layers_after)):
    diff = np.argwhere(lb != la)
    if len(diff):
        trans = {}
        for r, c in diff:
            k = (int(lb[r,c]), int(la[r,c]))
            trans[k] = trans.get(k, 0) + 1
        print(f"  Layer {i}: {len(diff)} cells changed — {trans}")
    else:
        print(f"  Layer {i}: no change")

# Take more clicks and watch all layers
print("\n" + "="*60)
print("5 MORE OVAL CLICKS — all layer diffs")
print("="*60)
for click_n in range(1, 6):
    prev_layers = [np.array(l).copy() for l in obs2.frame]
    obs2 = env.step(GameAction.ACTION6, {'x': 36, 'y': 55})
    cur_layers = [np.array(l) for l in obs2.frame]
    changes = []
    for i, (lb, la) in enumerate(zip(prev_layers, cur_layers)):
        diff = np.argwhere(lb != la)
        if len(diff):
            trans = {}
            for r, c in diff:
                k = (int(lb[r,c]), int(la[r,c]))
                trans[k] = trans.get(k, 0) + 1
            changes.append(f"L{i}:{dict(trans)}")
    print(f"  Oval click {click_n}: {' | '.join(changes) if changes else 'no layer changes'}")
    print(f"    levels={obs2.levels_completed}  score={getattr(obs2,'score',None)}")

# Finally: check if there are any streaming or event APIs
print("\n" + "="*60)
print("CHECK FOR ADDITIONAL GAME STATE FIELDS")
print("="*60)
# Try common fields that might carry animation/event data
for field in ['events', 'info', 'render', 'state', 'metadata', 'score',
              'message', 'reward', 'done', 'truncated', 'step_count',
              'animation', 'highlight', 'selected', 'cursor']:
    try:
        val = getattr(obs2, field, None)
        if val is not None:
            print(f"  obs.{field} = {val}")
        else:
            print(f"  obs.{field} = None/missing")
    except Exception as e:
        print(f"  obs.{field}: ERROR({e})")
