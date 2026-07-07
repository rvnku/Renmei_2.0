import aiohttp
import asyncio
from disnake import Color
from collections import Counter
from io import BytesIO
from PIL import Image
import colorsys


async def get_primary_color(url: str) -> Color:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()

    def process_image(image_data: bytes) -> Color:
        with Image.open(BytesIO(image_data)) as image:
            resized = image.convert('RGB').resize((128, 128))

        size = 128
        radius = size // 2
        center = radius

        pixels = list(resized.getdata())  # type: ignore
        circular_pixels = [
            pixels[y * size + x]
            for y in range(size)
            for x in range(size)
            if (x - center) ** 2 + (y - center) ** 2 <= radius ** 2
        ]

        temp = Image.new('RGB', (1, len(circular_pixels)))
        temp.putdata(circular_pixels)

        quantized = temp.quantize(8)
        palette = quantized.getpalette() or []
        counts = Counter(quantized.getdata())  # type: ignore

        color, score = None, 0.0
        for i, c in counts.items():
            r = palette[i * 3]
            g = palette[i * 3 + 1]
            b = palette[i * 3 + 2]
            _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if c * s * v > score:
                score = c * s * v
                color = (r, g, b)

        if not color:
            i = max(counts.items(), key=lambda x: x[1])[0]
            color = (palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2])

        return Color.from_rgb(*color)

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, process_image, data)
