# -*- coding: utf-8 -*-
import asyncio
import json
import pdfplumber

from loop.controller import tinyLLMLoop

async def single_test():
    name_tag0 = "TAG_cuda_syntax"
    with open(f"top/llm_kernel.cu", 'r') as f:
        initial_kernel = f.read()
    initial_kernel = f"```cuda{initial_kernel}```"
    
    object_dict_ = {
        "response": initial_kernel,
    }
    obj_file = f"top/syn_obj_.json"
    with open(obj_file, "w") as f:
        json.dump(object_dict_, f)

    tag0 = tinyLLMLoop(
        tag_path = name_tag0,
        max_loop_times = 10,
        _input_filename = obj_file,
        async_stamp = f"syn0",
        verbose = False,
    )
    task = asyncio.create_task(tag0.run())
    return await task


async def concurrent_test(concurrence : int = 10):
    
    name_tag0 = "TAG_cuda_syntax"

    def extract_text_from_pdf(pdf_path):
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            # 遍历每一页并提取文本
            for page in pdf.pages:
                text += page.extract_text()

        return text
    # 示例使用
    pdf_path = "TinyLLMLoop_Example-main/top/paper_test.pdf"
    text = extract_text_from_pdf(pdf_path)
    
    object_dict_ = {
        "response": text,
    }
    obj_file = f"top/syn_obj_.json"
    with open(obj_file, "w") as f:
        json.dump(object_dict_, f)


    tags = [
        tinyLLMLoop(
            tag_path = name_tag0,
            max_loop_times = 10,
            _input_filename = obj_file,
            async_stamp = f"syn{i}",
            verbose = False,
        ) for i in range(concurrence)
    ]
    tasks = [asyncio.create_task(tag.run()) for tag in tags]
    
    pending = set(tasks)
    while pending:
        done, pending = await asyncio.wait(
            pending,
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in done:
            result = task.result()
            print(f"[{name_tag0}] [async-{result['async_stamp']}] [loop-{result['cur_loop']}] [PASS] ['pass' : {result['pass']}]", flush = True)

            if result['pass']:
                for t in pending:
                    t.cancel()
                return result
    return result


if __name__ == "__main__":
    # res = asyncio.run(single_test())
    res = asyncio.run(concurrent_test())
    print(res)






