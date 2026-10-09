# omniedu

Official toolkit for **[Omni-Edu](https://huggingface.co/OpenDCAI)** — open K-12
learning and teaching models at 4B / 9B / 27B, fine-tuned from the Qwen3.5/3.8
family on the Omni-Edu instruction mixture.

The toolkit wraps the parts everyone rewrites by hand: picking a checkpoint,
building the chat messages, attaching images, choosing one of the teaching task
instructions, and running a JSONL batch. The official evaluation harness lives
outside this package — this is the model-calling layer only.

## Install

```bash
pip install omniedu                 # talk to a vLLM / OpenAI-compatible server
pip install "omniedu[transformers]" # also run the weights locally
```

Model weights stay on Hugging Face and are downloaded on demand — the package
contains code and task instructions only.

## Quickstart

```python
from omniedu import OmniEdu

model = OmniEdu.from_pretrained("27B", base_url="http://127.0.0.1:8000/v1")

response = model.chat(
    text="帮我判断学生这一步哪里错了，先给提示。",
    image="student_work.png",
    task="diagnose_and_correct",
)
print(response.text)
```

`model.chat(...)` is the synchronous form. Inside an event loop, use
`await model.achat(...)` instead.

## Serving the model

The recommended backend is vLLM with an OpenAI-compatible endpoint:

```bash
vllm serve OpenDCAI/Omni-Edu-27B \
  --served-model-name omniedu-27b \
  --max-model-len 32768 \
  --tensor-parallel-size 4 \
  --limit-mm-per-prompt '{"image": 12}' \
  --trust-remote-code
```

`omniedu serve --model 27B --tensor-parallel-size 4` prints the same command.
The models are trained no-think, so every request disables thinking
(`chat_template_kwargs.enable_thinking = false`) and decodes greedily with
`temperature=0` — the same protocol used for the paper's numbers.

## Teaching task instructions

These are the system instructions the models were **fine-tuned with**: stage 6 of
the data pipeline attaches one to every education-specific training row. The
package ships the paper's 19 templates, all defined in one place. Use them by id:

```python
from omniedu import list_tasks

for task in list_tasks().values():
    print(task.id, "|", task.category)

model.chat(text="...", task="solve_reasoned")
```

| Category | Task ids |
|---|---|
| Solving | `solve_answer_only`, `solve_reasoned`, `reading_comprehension` |
| Diagnosis and feedback | `diagnose_and_correct`, `answer_assessment`, `writing_feedback` |
| Curriculum grounding | `knowledge_point`, `mathfish_strict`, `mathfish_multirelation` |
| Tutoring and scaffolding | `mathtutor_scaffolding`, `mathtutor_pedagogy_following`, `tutorbench`, `active_probe`, `multihint`, `multiturn_socratic`, `oatutor_guidance`, `socratic_question_chain`, `direct_explanation`, `longtutor_official` |

`register_task(id, instruction)` adds your own without touching the package.

General-purpose examples are never remapped: they keep the system prompt they
came with, so the pipeline defines no generic template for them. Pass your own
with `system=` when you need one.

Two consequences worth knowing:

* `chat()` and `batch()` send **no** system prompt unless you pass `task=` or
  `system=`. The default path matches the way the models were trained and the
  paper's inference protocol.
* The paper's benchmark numbers were produced **without** these instructions —
  the evaluation protocol explicitly does not add pedagogical system prompts
  (`evaluation/PROTOCOL.md`). To reproduce a benchmark score, do not pass
  `task=`.

## Batch inference

JSONL in, JSONL out, resumable:

```bash
omniedu batch --input problems.jsonl --output predictions.jsonl \
  --model 27B --base-url http://127.0.0.1:8000/v1 \
  --task solve_reasoned --concurrency 32
```

Input rows may be ShareGPT-style (`messages` + `images`) or flat
(`text` / `prompt` / `question`, plus `image` / `images`). `<image>` markers
inside the text are replaced by the supplied images in order.

Each output row records the model, task, decoding parameters and the SHA-256 of
the system prompt, so a prediction file can be traced back to the exact
instruction that produced it. Rows that fail are retried on the next run; only
successful rows are treated as done, and the output file is compacted so a
retry never leaves two lines for the same sample.

## Python API

```python
from omniedu import OmniEdu

OmniEdu.from_pretrained("4B")                                   # OpenDCAI/Omni-Edu-4B
OmniEdu.from_pretrained("OpenDCAI/Omni-Edu-9B")                 # any HF id
OmniEdu.from_pretrained("/models/Omni-Edu-4B")                  # local path
OmniEdu.from_pretrained("4B", base_url="http://host:8000/v1")   # remote endpoint

model.chat(text="...", task="solve_reasoned", max_new_tokens=4096)
model.chat(messages=[{"role": "user", "content": "..."}])
model.batch("in.jsonl", out="out.jsonl", task="solve_reasoned")
```

## License

The toolkit is licensed under [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).
Model weights keep their upstream licence and are never redistributed here.
