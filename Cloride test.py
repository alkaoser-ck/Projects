from moviepy import VideoClip, AudioFileClip, CompositeVideoClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from math import sin, pi

# Narration

narration = (
    "Now we will learn to detect Iron 3+ Ion......... "
    "First, take the sample solution in two test tubes.... "
    "Adding NaOH will produce a brown precipitate.... "
    "Adding NH4OH will also produce a brown precipitate.... "
    "It proves that the sample solution has Iron 3+ Ion in it. "
    "Always remember to use safety equipment."
)

tts = gTTS(text=narration, lang="en")
tts.save("narration.mp3")

# Video parameters

w, h = 1280, 720
duration = 25
fps = 120
font = ImageFont.load_default()


# Drawing frame
def draw_frame(t):
    img = Image.new("RGB", (w, h), color=(245, 245, 250))
    draw = ImageDraw.Draw(img)

    # Tube parameters
    tp = [w // 3 - 80, 2 * w // 3 - 80]
    ty = 120
    tw = 160
    th = 420
    tb = ty + th
    ht = tw / 2

    # Draw tubes
    for tx in tp:
        draw.line([(tx, ty + 20), (tx, tb - 20)], fill=(40, 40, 60), width=4)
        draw.line([(tx + tw, ty + 20), (tx + tw, tb - 20)], fill=(40, 40, 60), width=4)
        draw.ellipse([tx, ty, tx + tw, ty + 40], outline=(40, 40, 60), width=4)
        parabola = [
            (tx + i, int(tb - 10 - 0.0025 * (i - ht) ** 2)) for i in range(tw + 1)
        ]
        draw.line(parabola, fill=(40, 40, 60), width=4)

    # Fill sample solution (light blue)

    fstart = 5
    fend = 8
    fp = min(max((t - fstart) / (fend - fstart), 0), 1)
    min_h = tb - 10
    max_h = tb - 180
    liquid_top = int(min_h - (min_h - max_h) * fp)
    sample_color = (100, 160, 255)  # light blue

    # Track which tube should turn brown
    tube_brown = [False, False]

    # Animate NaOH drop on tube 1
    drop_st, drop_end = 10, 12
    tube_x1 = tp[0]
    if drop_st <= t <= drop_end:
        p = (t - drop_st) / (drop_end - drop_st)
        drop_y = int(80 + (liquid_top - 80) * p)
        drop_x = tube_x1 + tw // 2 - 10 + 10 * sin(p * pi)
        draw.ellipse([drop_x, drop_y, drop_x + 20, drop_y + 20], fill=(0, 0, 150))
        draw.text((drop_x - 10, drop_y - 25), "NaOH", font=font, fill=(0, 0, 150))
    if t >= drop_end:
        tube_brown[0] = True

    # Animate NH4OH drop on tube 2
    drop_st, drop_end = 15, 17
    tube_x2 = tp[1]
    if drop_st <= t <= drop_end:
        p = (t - drop_st) / (drop_end - drop_st)
        drop_y = int(80 + (liquid_top - 80) * p)
        drop_x = tube_x2 + tw // 2 - 10 + 10 * sin(p * pi)
        draw.ellipse([drop_x, drop_y, drop_x + 20, drop_y + 20], fill=(0, 0, 150))
        draw.text((drop_x - 20, drop_y - 25), "NH₄OH", font=font, fill=(0, 0, 150))

    if t >= drop_end:
        tube_brown[1] = True

    # Draw liquid
    for i, tx in enumerate(tp):
        color = (139, 69, 19) if tube_brown[i] else sample_color
        tp = [(tx + i, int(liquid_top - 0.002 * (i - h) ** 2)) for i in range(tw + 1)]
        bp = [(tx + i, int(tb - 10 - 0.0015 * (i - h) ** 2)) for i in range(tw + 1)]
        lp = tp + bp[::-1]
        draw.polygon(lp, fill=color)

    # Title
    draw.text((40, 20), "Fe³⁺ Ion Test", font=font, fill=(10, 30, 60))

    return np.array(img)


# Make video
video = VideoClip(draw_frame, duration=duration)
audio = AudioFileClip("narration.mp3")
video = video.with_audio(audio)
final = CompositeVideoClip([video])
final.write_videofile("Fe3+ Ion test.mp4", fps=fps, codec="libx264", audio_codec="aac")

print("Video created")
