"""Optional LLM API exercise, completed with AI assistance."""

import os
import time
from typing import Any, Callable

OPENAI_MODEL = "deepseek-v4-pro"
OPENAI_MINI_MODEL = "deepseek-flash"
# Off-peak output rates (USD / 1K tokens), 06/11/2026.
COST_PER_1K_OUTPUT_TOKENS = {OPENAI_MODEL: 0.00198, OPENAI_MINI_MODEL: 0.0006}


def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY"),
                    base_url="https://api.deepseek.com")
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        reasoning_effort="none",
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or "", float(time.perf_counter() - start)


def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    return call_openai(prompt, OPENAI_MINI_MODEL, temperature, top_p, max_tokens)


def compare_models(prompt: str) -> dict:
    large_response, large_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)
    estimated_output_tokens = len(large_response.split()) / 0.75
    return {
        "gpt4o_response": large_response,
        "mini_response": mini_response,
        "gpt4o_latency": large_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": estimated_output_tokens / 1000 * COST_PER_1K_OUTPUT_TOKENS[OPENAI_MODEL],
    }


def streaming_chatbot() -> None:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY"),
                    base_url="https://api.deepseek.com")
    history: list[dict[str, str]] = []
    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in {"quit", "exit"}:
            return
        if not prompt:
            continue
        messages = history + [{"role": "user", "content": prompt}]
        stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            reasoning_effort="none",
            max_tokens=256,
            stream=True,
        )
        chunks = []
        print("Assistant: ", end="", flush=True)
        for item in stream:
            delta = item.choices[0].delta.content or ""
            chunks.append(delta)
            print(delta, end="", flush=True)
        print()
        history = (messages + [{"role": "assistant", "content": "".join(chunks)}])[-6:]


def retry_with_backoff(fn: Callable, max_retries: int = 3, base_delay: float = 0.1) -> Any:
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception:
            if attempt == max_retries:
                raise
            time.sleep(base_delay * 2 ** attempt)


def batch_compare(prompts: list[str]) -> list[dict]:
    return [{**compare_models(prompt), "prompt": prompt} for prompt in prompts]


def format_comparison_table(results: list[dict]) -> str:
    headers = "Prompt | GPT-4o Response | Mini Response | GPT-4o Latency | Mini Latency"
    rows = [headers, "-" * len(headers)]
    for result in results:
        rows.append(
            f"{str(result['prompt'])[:40]} | {str(result['gpt4o_response'])[:40]} | "
            f"{str(result['mini_response'])[:40]} | {result['gpt4o_latency']:.3f} | "
            f"{result['mini_latency']:.3f}"
        )
    return "\n".join(rows)
