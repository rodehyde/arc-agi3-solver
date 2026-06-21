"""tn36 Step 1 — initial scene inspection."""
import numpy as np
from arc_agi import Arcade, OperationMode

arcade = Arcade(operation_mode=OperationMode.OFFLINE)
env = arcade.make('tn36')
obs = env.observation_space

g = np.array(obs.frame[-1])

print(f"levels_completed={obs.levels_completed}  win_levels={obs.win_levels}")
print(f"available_actions={obs.available_actions}")
print(f"grid shape: {g.shape}")

# Find bounding box of non-zero content
rows, cols = np.where(g > 0)
r0, r1 = int(rows.min()), int(rows.max())
c0, c1 = int(cols.min()), int(cols.max())
print(f"content bounding box: rows {r0}–{r1}, cols {c0}–{c1}")

# Value inventory
vals, counts = np.unique(g, return_counts=True)
print("\nValue inventory:")
colour = {0:'white',1:'lt-grey',2:'md-grey',3:'dk-grey',4:'vdk-grey',5:'black',
          6:'pink',7:'lt-pink',8:'red',9:'blue',10:'lt-blue',11:'yellow',
          12:'orange',13:'maroon',14:'green',15:'purple'}
for v, c in zip(vals, counts):
    print(f"  {v} ({colour.get(int(v),'?')}): {c} cells")

# Char-map render
char = {0:'.',1:'f',2:'m',3:'d',4:'v',5:'#',6:'p',7:'q',8:'R',9:'B',
        10:'L',11:'Y',12:'O',13:'M',14:'G',15:'V'}

print(f"\nFull grid rows {r0}–{r1}, cols {c0}–{c1}:")
print('      ' + ''.join(f'{c%10}' for c in range(c0, c1+1)))
for r in range(r0, r1+1):
    row = ''.join(char.get(int(g[r, c]), '?') for c in range(c0, c1+1))
    print(f'{r:3d}   {row}')

# Check other frame layers
print(f"\nNumber of frame layers: {len(obs.frame)}")
for i, layer in enumerate(obs.frame):
    la = np.array(layer)
    vals_l = np.unique(la)
    print(f"  Layer {i}: values {vals_l}")

# Check all obs attributes
print(f"\nAll obs attributes: {[a for a in dir(obs) if not a.startswith('_')]}")
