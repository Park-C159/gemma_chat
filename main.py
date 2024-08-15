import sys

sys.path.append("/kaggle/working/gemma_pytorch/")
from gemma.config import GemmaConfig, get_model_config
from gemma.model import GemmaForCausalLM
from gemma.tokenizer import Tokenizer
import contextlib
import os
import torch

# Load the model
VARIANT = "2b-v2"
MACHINE_TYPE = "cpu"
weights_dir = './models/gemma-2-2b-it'
weights_file = os.path.join(weights_dir, "model.ckpt")


@contextlib.contextmanager
def _set_default_tensor_type(dtype: torch.dtype):
    """Sets the default torch dtype to the given dtype."""
    torch.set_default_dtype(dtype)
    yield
    torch.set_default_dtype(torch.float)


model_config = get_model_config(VARIANT)
model_config.tokenizer = os.path.join(weights_dir, "tokenizer.model")

device = torch.device(MACHINE_TYPE)
with _set_default_tensor_type(model_config.get_dtype()):
    model = GemmaForCausalLM(model_config)
    model.load_weights(weights_file)
    model = model.to(device).eval()

# Use the model

USER_CHAT_TEMPLATE = "<start_of_turn>user\n{prompt}<end_of_turn><eos>\n"
MODEL_CHAT_TEMPLATE = "<start_of_turn>model\n{prompt}<end_of_turn><eos>\n"

prompt = (
    USER_CHAT_TEMPLATE.format(
        prompt="请用中文回答，后面的所有问题"
    )
    # + MODEL_CHAT_TEMPLATE.format(prompt="California.")
    # + USER_CHAT_TEMPLATE.format(prompt="What can I do in California?")
    # + "<start_of_turn>model\n"
)

chat_history = USER_CHAT_TEMPLATE.format(prompt="请用中文回答后面所有的问题。")

while True:

    user_input = input("你: ")
    if user_input.lower() == 'exit':
        break

    chat_history += USER_CHAT_TEMPLATE.format(prompt=user_input) + "<start_of_turn>model\n"
    # Generate and display the model's response
    print("模型: ", end="")
    model_ans = model.generate_and_stream(
        prompts=chat_history,
        device=device,
        output_len=512,
    )
    chat_history += model_ans + "<end_of_turn><eos>\n"

# output = model.generate(
#     USER_CHAT_TEMPLATE.format(prompt=prompt),
#     device=device,
#     output_len=512,
# )
# print(output)

# 调用生成并实时输出的函数
# model.generate_and_stream(
#     prompts=USER_CHAT_TEMPLATE.format(prompt=prompt),  # 使用命名参数
#     device=device,
#     output_len=512,
# )
