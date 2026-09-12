"""Create a deterministic synthetic vision fixture, not encyclopedia content."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

image = Image.new('RGB', (640, 280), 'white')
draw = ImageDraw.Draw(image)
font = ImageFont.load_default(size=26)
draw.text((160, 25), 'Synthetic vision test', fill='black', font=font)
draw.rectangle((40,100,260,220), outline='black', width=3)
draw.rectangle((380,100,600,220), outline='black', width=3)
draw.text((105,145), 'Client', fill='black', font=font)
draw.text((465,145), 'API', fill='black', font=font)
draw.line((260,160,370,160), fill='black', width=3)
draw.polygon([(380,160),(366,151),(366,169)], fill='black')
draw.text((272,177), 'request', fill='black', font=ImageFont.load_default(size=20))
image.save(Path(__file__).with_name('synthetic-architecture.png'))
