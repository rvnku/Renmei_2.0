from core.errors import CompileError
from .response import Response
from io import StringIO
import contextlib, textwrap


latest = None

def get_latest():
    return latest


async def execute(code: str, env: dict) -> Response:
    global latest
    body = f'async def __exec_func__():\n{textwrap.indent(code, '    ')}'
    stdout = StringIO()

    try:
        exec(body, env)
    except Exception as exc:
        raise CompileError(exc)
    func = env['__exec_func__']

    try:
        with contextlib.redirect_stdout(stdout):
            result = await func()
    except Exception as exc:
        output = stdout.getvalue()
        raise RuntimeError(exc)
    else:
        output = stdout.getvalue()
        if result is not None:
            latest = result
        return Response(output, result)
