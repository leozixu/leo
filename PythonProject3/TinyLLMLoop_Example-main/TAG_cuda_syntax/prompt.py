import json
import sys
import logging

logger = logging.getLogger(__name__)

def get_prompt_inputs():
    try:
        dir_name = sys.argv[1]
        cur_loop = sys.argv[2]
        async_stamp = sys.argv[3]
        return dir_name, cur_loop, async_stamp

    except Exception as e:
        logger.error(f"Error in getting prompt inputs: {str(e)}")
        return 0

def prompt_const(
    evaluate_result: dict,
):

    strategy_message = '''
        You are a paper summarizer, responsible for concisely summarizing long articles without losing the key content of the paper.
        # Input: You will receive a plain text content.

        # HARDWARE: Nvidia 3080 GPU with Tensor Cores and Shared Memory

        # TARGET: Understand the received paper content and summarize it.
        
        # GOAL: The final word count of the text should meet the requirements, and it must remain faithful to the author's original intent.

        
        # SUCCESS CRITERIA:
        - **word count**: The word count should be adjusted to meet the required length of the article.
        - **Loyalty**: When modifying the original word count, it should stay true to the meaning of the original text.



        '''

    format_message = '''
        The word count of this article does not meet the requirements. Please simplify or expand it according to the requirements, but without distorting the meaning.\n
        '''

    user_message = '''
        Please adjust the word count of this article appropriately to meet the requirements.:\n
        ''' + evaluate_result["cur_kernel"] + evaluate_result["error_message"]

    return {
        "system": strategy_message + format_message,
        "user": user_message,
    }

if __name__ == "__main__":

    dir_name, cur_loop, async_stamp = get_prompt_inputs()
    with open(f"./{dir_name}/results-{async_stamp}/loop-{cur_loop}_evaluate_.json", "r") as f:
        evaluate_result = json.load(f)

    result = prompt_const(evaluate_result)

    with open(f"./{dir_name}/results-{async_stamp}/loop-{cur_loop}_prompt_.json", "w") as f:
        json.dump(result, f) 
    

