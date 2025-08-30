import json
import sys
import logging
import os
import asyncio
import time

import subprocess as sp
#from loop.utils import extract_code, extract_error_lines
import pdb


logger = logging.getLogger(__name__)

def get_eva_inputs() -> str:
    dir_name = sys.argv[1]
    cur_loop = sys.argv[2]
    async_stamp = sys.argv[3]
    return dir_name, cur_loop, async_stamp

async def evaluate(
    dir_name: str,
    cur_loop: int,
    async_stamp: str,
) -> dict:

    file_path = f"./{dir_name}/results-{async_stamp}/loop-{cur_loop}_begin_.json" 
    with open(file_path, "r") as f:
        object_dict_ = json.load(f)
    response_text = object_dict_["response"]
    word_count = len(response_text.split())

    if word_count < 4700:
        returncode = 1
    elif word_count > 5300:
        returncode = 2
    else:
        returncode = 0
    new_kernel = response_text
    # new_kernel = extract_code(object_dict_["response"], "cuda")
    #
    # ## write new kernel for nvcc compile
    # file_path = f"./{dir_name}/results-{async_stamp}/loop-{cur_loop}_kernel.cu"
    # with open(file_path, "w") as f:
    #     f.write(new_kernel)
    #
    # print(f"[{dir_name}] [async-{async_stamp}] [loop-{cur_loop}] [NVCC] nvcc compile start at {time.time()}", flush=True)
    # process = await asyncio.create_subprocess_exec(
    #     "make",
    #     "-f",
    #     f"./{dir_name}/Makefile",
    #     f"src_cu={dir_name}/results-{async_stamp}/loop-{cur_loop}_kernel.cu",
    #     "--silent",
    #     stdout=asyncio.subprocess.PIPE,
    #     stderr=asyncio.subprocess.PIPE
    # )
    # stdout, stderr = await process.communicate()
    #
    # print(f"[{dir_name}] [async-{async_stamp}] [loop-{cur_loop}] [NVCC] nvcc compile end at {time.time()}", flush=True)
    # err_messages = extract_error_lines(stderr.decode())
    # returncode = process.returncode

    if returncode == 0:
        return {
            'pass' : True,
            'async_stamp': async_stamp,
            'cur_loop': cur_loop,
            'cur_kernel': new_kernel,
            'error_message' : "",
        }

    elif returncode == 1:
        return {
            'pass': False,
            'async_stamp': async_stamp,
            'cur_loop': cur_loop,
            'cur_kernel': new_kernel,
            'error_message' : "The word count of this article is somewhat low. Please help me expand it so that the total word count increases by 200 to 300 words.",
        }
    else:
        return {
            'pass': False,
            'async_stamp': async_stamp,
            'cur_loop': cur_loop,
            'cur_kernel': new_kernel,
            'error_message': "The word count of this article is quite high. Please help me summarize it so that the total word count is reduced by 200 to 300 words.",
        }


if __name__ == "__main__":
    dir_name, cur_loop, async_stamp = get_eva_inputs()
    result = asyncio.run(evaluate(dir_name, cur_loop, async_stamp))
    with open(f"./{dir_name}/results-{async_stamp}/loop-{cur_loop}_evaluate_.json", "w") as f:
        json.dump(result, f) 
    
    






