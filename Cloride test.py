from moviepy import VideoClip, AudioFileClip, CompositeVideoClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from math import *

narration = (
    "আজ আমরা শিখবো কিভাবে ক্লোরাইড আয়ন শনাক্ত করা হয়। "
    "প্রথমে টেস্টটিউবে নমুনা দ্রবণ নিন। "
    "এরপর dilute nitric acid যোগ করুন। "
    "এবার silver nitrate solution যোগ করলে প্রতিক্রিয়া হবে। "
    "দেখুন, সাদা অবসাদ তৈরি হলো। "
    "এটি প্রমাণ করে নমুনায় ক্লোরাইড আয়ন উপস্থিত আছে। "
    "সবসময় নিরাপত্তা সরঞ্জাম ব্যবহার করতে ভুলবেন না।"
)

tts = gTTS(text=narration, lang="bn")
tts.save("narration.mp3")

W, H = 1280, 720
duration = 30
fps = 12

try:
    font = ImageFont.truetype("DejaVuSans.ttf", 32)
except:
    font = ImageFont.load_default()

# Drwaing Frames


def draw_frame(t):
    img = Image.new("RGB", (W, H), color=(245, 245, 250))
    draw = ImageDraw.Draw(img)
    # Tube parameters
    tube_x = W // 2 - 80
    tube_y = 120
    tube_w = 160
    tube_h = 420
    tube_bottom = tube_y + tube_h
    h = tube_w / 2

    # Tube outline
    draw.line(
        [(tube_x, tube_y + 20), (tube_x, tube_bottom - 20)], fill=(40, 40, 60), width=4
    )
    draw.line(
        [(tube_x + tube_w, tube_y + 20), (tube_x + tube_w, tube_bottom - 20)],
        fill=(40, 40, 60),
        width=4,
    )
    draw.ellipse(
        [tube_x, tube_y, tube_x + tube_w, tube_y + 40], outline=(40, 40, 60), width=4
    )
    a_bottom = 0.0025
    parabola_points = [
        (tube_x + i, int(tube_bottom - 10 - a_bottom * (i - h) ** 2))
        for i in range(tube_w + 1)
    ]
    draw.line(parabola_points, fill=(40, 40, 60), width=4)

    # Blue solution
    liquid_fill_start = 5
    liquid_fill_end = 8
    liquid_max_height = tube_bottom - 5
    liquid_min_height = tube_bottom - 180

    if t < liquid_fill_start:
        liquid_height = liquid_max_height
    elif t <= liquid_fill_end:
        p = (t - liquid_fill_start) / (liquid_fill_end - liquid_fill_start)
        liquid_height = int(
            liquid_max_height - (liquid_max_height - liquid_min_height) * p
        )
    else:
        liquid_height = liquid_min_height

    # Top & bottom parabola points for liquid
    a_top = 0.002
    k_top = liquid_height
    top_points = [
        (tube_x + i, int(k_top - a_top * (i - h) ** 2)) for i in range(tube_w + 1)
    ]
    a_bottom_liquid = 0.0015
    k_bottom_liquid = tube_bottom - 10
    bottom_points = [
        (tube_x + i, int(k_bottom_liquid - a_bottom_liquid * (i - h) ** 2))
        for i in range(tube_w + 1)
    ]
    liquid_points = top_points + bottom_points[::-1]
    draw.polygon(liquid_points, fill=(100, 160, 255))

    # Drops animation

    # HNO3 drop
    drop_start = 9
    drop_end = 12
    if drop_start <= t <= drop_end:
        p = (t - drop_start) / (drop_end - drop_start)
        drop_y = int(80 + (liquid_min_height - 80) * p)
        drop_x = tube_x + tube_w // 2 - 20 + 10 * sin(p * pi)
        draw.text((drop_x, drop_y), "HNO₃", fill=(0, 0, 150), font=font)

    # AgNO3 drop
    if 12 <= t <= 15:
        p = (t - 12) / 3
        drop_y = int(80 + (liquid_min_height - 80) * p)
        drop_x = tube_x + tube_w // 2 + 20 * sin(p * pi)
        draw.text((drop_x, drop_y), "AgNO₃", fill=(150, 0, 0), font=font)

    # White precipitate

    precipitate_start = 18
    if t >= precipitate_start:
        total_slide_time = 3
        slide_progress = min((t - precipitate_start) / total_slide_time, 1.0)

        for i in range(60):
            xx = tube_x + 20 + (i * 17 % (tube_w - 40))
            yy_start = liquid_min_height + 20 + (i * 13 % 160)
            yy_end = tube_bottom - 20
            yy = int(yy_start + (yy_end - yy_start) * slide_progress)
            rr = 3 + (i % 3)
            draw.ellipse([xx - rr, yy - rr, xx + rr, yy + rr], fill=(250, 250, 250))
    # Title
    draw.text((40, 20), "Chloride Ion Test", font=font, fill=(10, 30, 60))

    return np.array(img)


def make_frame(t):
    return draw_frame(t)


video = VideoClip(make_frame, duration=duration)
audio = AudioFileClip("narration.mp3")
video = video.with_audio(audio)
final = CompositeVideoClip([video])
final.write_videofile("chloride test.mp4", fps=fps, codec="libx264", audio_codec="aac")

print("Video Created")
