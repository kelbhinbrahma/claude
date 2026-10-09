python3 gen.py >/dev/null && node render.js && python3 -c "
from PIL import Image;import glob
fs=sorted(glob.glob('export/*.png'));W=620;H=877
m=Image.new('RGB',(W*3+40,H*2+30),'white')
for i,f in enumerate(fs):m.paste(Image.open(f).resize((W,H)),(10+(i%3)*(W+10),10+(i//3)*(H+10)))
m.save('/tmp/claude-0/-home-user-claude/754fd4d9-9c35-5e08-ac9d-02d1949dd969/scratchpad/m.png')"
