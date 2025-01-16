# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Apply monkey-patch function to models
"""

#### Open Source Models

def apply_monkey_patch_to_llama():
    from transformers.models.llama.modeling_llama import LlamaFlashAttention2
    from verl.models.transformers.llama import llama_flash_attn_forward
    LlamaFlashAttention2.forward = llama_flash_attn_forward


_PATCH_NAME_TO_FUNC = {
    'llama': apply_monkey_patch_to_llama,
    # 'qwen2': apply_monkey_patch_to_qwen2,
}

from transformers import PretrainedConfig


def apply_monkey_patch(config: PretrainedConfig, verbose=True):
    success_apply_monkey_patch = False
    if config.model_type in _PATCH_NAME_TO_FUNC:
        _PATCH_NAME_TO_FUNC[config.model_type]()
        success_apply_monkey_patch = True

    if success_apply_monkey_patch and verbose:
        print(f'Applying monkey patch to model {config.model_type}')

    return success_apply_monkey_patch
