from moviepy import VideoClip, AudioFileClip, CompositeVideoClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from math import sin, pi

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
W, H = 1280, 720
duration = 25
fps = 120

font = ImageFont.load_default()

# Draw frame
def draw_frame(t):
    img = Image.new("RGB", (W, H), color=(245, 245, 250))
    draw = ImageDraw.Draw(img)

    # Tube parameters
    tube_positions = [W // 3 - 80, 2 * W // 3 - 80]
    tube_y = 120
    tube_w = 160
    tube_h = 420
    tube_bottom = tube_y + tube_h
    h = tube_w / 2

    # Draw tubes
    for tube_x in tube_positions:
        draw.line(
            [(tube_x, tube_y + 20), (tube_x, tube_bottom - 20)],
            fill=(40, 40, 60),
            width=4,
        )
        draw.line(
            [(tube_x + tube_w, tube_y + 20), (tube_x + tube_w, tube_bottom - 20)],
            fill=(40, 40, 60),
            width=4,
        )
        draw.ellipse(
            [tube_x, tube_y, tube_x + tube_w, tube_y + 40],
            outline=(40, 40, 60),
            width=4,
        )
        parabola_points = [
            (tube_x + i, int(tube_bottom - 10 - 0.0025 * (i - h) ** 2))
            for i in range(tube_w + 1)
        ]
        draw.line(parabola_points, fill=(40, 40, 60), width=4)

    # Fill sample solution
    fill_start = 5
    fill_end = 8
    fill_progress = min(max((t - fill_start) / (fill_end - fill_start), 0), 1)
    liquid_min_height = tube_bottom - 10
    liquid_max_height = tube_bottom - 180
    liquid_top = int(
        liquid_min_height - (liquid_min_height - liquid_max_height) * fill_progress
    )
    sample_color = (100, 160, 255)  # light blue

    tube_brown = [False, False]

    #  NaOH drop
    drop_start_1, drop_end_1 = 10, 12
    tube_x1 = tube_positions[0]
    if drop_start_1 <= t <= drop_end_1:
        p = (t - drop_start_1) / (drop_end_1 - drop_start_1)
        drop_y = int(80 + (liquid_top - 80) * p)
        drop_x = tube_x1 + tube_w // 2 - 10 + 10 * sin(p * pi)
        draw.ellipse([drop_x, drop_y, drop_x + 20, drop_y + 20], fill=(0, 0, 150))
        draw.text((drop_x - 10, drop_y - 25), "NaOH", font=font, fill=(0, 0, 150))
    if t >= drop_end_1:
        tube_brown[0] = True

    # NH4OH drop
    drop_start_2, drop_end_2 = 15, 17
    tube_x2 = tube_positions[1]
    if drop_start_2 <= t <= drop_end_2:
        p = (t - drop_start_2) / (drop_end_2 - drop_start_2)
        drop_y = int(80 + (liquid_top - 80) * p)
        drop_x = tube_x2 + tube_w // 2 - 10 + 10 * sin(p * pi)
        draw.ellipse([drop_x, drop_y, drop_x + 20, drop_y + 20], fill=(0, 0, 150))
        draw.text((drop_x - 20, drop_y - 25), "NH₄OH", font=font, fill=(0, 0, 150))

    if t >= drop_end_2:
        tube_brown[1] = True

    # Draw liquid
    for i, tube_x in enumerate(tube_positions):
        color = (139, 69, 19) if tube_brown[i] else sample_color
        top_points = [
            (tube_x + i, int(liquid_top - 0.002 * (i - h) ** 2))
            for i in range(tube_w + 1)
        ]
        bottom_points = [
            (tube_x + i, int(tube_bottom - 10 - 0.0015 * (i - h) ** 2))
            for i in range(tube_w + 1)
        ]
        liquid_points = top_points + bottom_points[::-1]
        draw.polygon(liquid_points, fill=color)

    # Title
    draw.text((40, 20), "Fe³⁺ Ion Test", font=font, fill=(10, 30, 60))

    return np.array(img)


video = VideoClip(draw_frame, duration=duration)
audio = AudioFileClip("narration.mp3")
video = video.with_audio(audio)
final = CompositeVideoClip([video])
final.write_videofile("Fe3+ Ion test.mp4", fps=fps, codec="libx264", audio_codec="aac")

print("Video created!")
