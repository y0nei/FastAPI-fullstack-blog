import sass
from src.core.logging import logger

input = "src/static/scss"
output = "src/static/css/compiled"

async def compile_sass():
    try:
        sass.compile(dirname=(input, output), output_style="compressed")
        logger.info("Compiled your css.")
    except sass.CompileError:
        logger.exception("Sass compilation error.")
