"""Optimize the authorized portrait and produce a local social preview image."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
portrait=Image.open(ROOT/'assets/matt-miller.png').convert('RGBA')
portrait.save(ROOT/'assets/matt-miller.webp',quality=88,method=6)
canvas=Image.new('RGB',(1200,630),'#183e3b')
draw=ImageDraw.Draw(canvas)
fontroot=Path('C:/Windows/Fonts')
serif=ImageFont.truetype(str(fontroot/'georgia.ttf'),60)
sans=ImageFont.truetype(str(fontroot/'segoeui.ttf'),23)
small=ImageFont.truetype(str(fontroot/'segoeui.ttf'),17)
draw.text((65,55),'NOLAPATENT',font=sans,fill='#e0bd82')
draw.text((65,115),'A lawyer who\nunderstands\ntechnology.',font=serif,fill='#f6f3e9',spacing=8)
draw.line((65,355,600,355),fill='#637f6e',width=1)
draw.text((65,390),'Matt Miller',font=sans,fill='#f6f3e9')
draw.text((65,432),'Patent & intellectual property attorney',font=small,fill='#d3dfcf')
draw.text((65,466),'Special Counsel · Kean Miller · New Orleans',font=small,fill='#d3dfcf')
draw.text((65,558),'nolapatent.com',font=small,fill='#e0bd82')
head=portrait.resize((565,565),Image.Resampling.LANCZOS)
draw.ellipse((660,65,1170,575),fill='#a6b39b')
canvas.paste(head,(635,65),head)
canvas.save(ROOT/'assets/social-card.jpg',quality=90,optimize=True)
print('Portrait and social preview created.')
