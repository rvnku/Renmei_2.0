from disnake import Colour
from disnake.ui import Container, Separator, TextDisplay
from .response import Response
from core.errors import CompileError
import traceback


async def compile_error_components(code: str, exception: CompileError):
    return Container(
        TextDisplay('## Compile Error'),
        Separator(),
        TextDisplay(f'### Code:\n```py\n{code}\n```'),
        Separator(),
        TextDisplay(f'### Output:\n```py\n{'\n'.join(traceback.format_exception(exception))}\n```'),
        accent_colour=Colour.brand_red()
    )

async def runtime_error_components(code: str, exception: RuntimeError):
    return Container(
        TextDisplay('## Runtime Error'),
        Separator(),
        TextDisplay(f'### Code:\n```py\n{code}\n```'),
        Separator(),
        TextDisplay(f'### Output:\n```py\n{'\n'.join(traceback.format_exception(exception))}\n```'),
        accent_colour=Colour.brand_red()
    )

async def output_result_components(code: str, response: Response):
    if not response.output and response.result is None:
        return TextDisplay('Success command')

    container = [
        TextDisplay('## Success Command'),
        Separator(),
        TextDisplay(f'### Code:\n```py\n{code}\n```'),
    ]
    if response.output:
        container.extend([
            Separator(),
            TextDisplay(f'### Output:\n```py\n{response.output}\n```'),
        ])
    if response.result is not None:
        container.extend([
            Separator(),
            TextDisplay(f'### Result:\n```py\n{response.result}\n```'),
        ])
    return Container(*container, accent_colour=Colour.brand_green())
