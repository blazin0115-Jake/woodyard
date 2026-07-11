# Woodyard — An open workspace for autonomous AI agents
# Copyright (C) 2026 blazin0115-Jake
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#!/usr/bin/env python3
"""
UQLM Scorer -- Hallucination Detection Integration for DeepSeek v4-flash

Modes:
  - WhiteBox ($0 cost):   Uses token logprobs from single generation
  - BlackBox (Nx cost):   Multiple generations for deep verification
  - Fallback:             Heuristic when UQLM not available

Usage:
    from uqlm_scorer import UQLMScorer
    scorer = UQLMScorer()
    result = await scorer.confidence("1+1=?")     # WhiteBox, $0
    result = await scorer.deep_verify("Question")  # BlackBox, N=3
"""

import os
import sys
import io
import asyncio
import logging

# Force UTF-8 output on Windows CP1252 terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ('utf-8', 'utf8'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("uqlm_scorer")


class UQLMScorer:
    """UQLM hallucination detector wrapper for DeepSeek v4-flash"""

    def __init__(self, model_name: str = "deepseek-v4-flash",
                 api_key: str = None, auto_init: bool = True):
        self.model_name = model_name
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self._llm = None
        self._whitebox = None
        self._blackbox = None
        self._initialized = False
        if auto_init:
            self.init_sync()

    def init_sync(self):
        """Initialize LangChain ChatOpenAI (synchronous)"""
        try:
            from langchain_openai import ChatOpenAI
            self._llm = ChatOpenAI(
                model=self.model_name,
                api_key=self.api_key,
                base_url="https://api.deepseek.com/v1",
                temperature=0.3,
                max_tokens=2048,
                logprobs=True,
                top_logprobs=5,
                timeout=60,
            )
            log.info(f"UQLM LLM ready: {self.model_name}")
            self._initialized = True
        except Exception as e:
            log.warning(f"UQLM LLM init failed (fallback mode): {e}")
            self._initialized = False

    async def _get_whitebox(self):
        """Lazy init WhiteBoxUQ (single generation, $0 cost)"""
        if self._whitebox is not None:
            return self._whitebox
        try:
            from uqlm import WhiteBoxUQ
            self._whitebox = WhiteBoxUQ(
                llm=self._llm,
                scorers=["sequence_probability", "min_probability"]
            )
            log.info("WhiteBoxUQ ready ($0/run)")
        except Exception as e:
            log.error(f"WhiteBoxUQ init failed: {e}")
            self._whitebox = None
        return self._whitebox

    async def _get_blackbox(self):
        """Lazy init BlackBoxUQ (downloads NLI model on first use)"""
        if self._blackbox is not None:
            return self._blackbox
        try:
            from uqlm import BlackBoxUQ
            self._blackbox = BlackBoxUQ(
                llm=self._llm,
                scorers=["semantic_negentropy", "noncontradiction"],
                use_best=True,
                device="auto",
            )
            log.info("BlackBoxUQ ready (Nx cost)")
        except Exception as e:
            log.warning(f"BlackBoxUQ init failed (using no-NLI fallback): {e}")
            try:
                from uqlm import BlackBoxUQ
                self._blackbox = BlackBoxUQ(
                    llm=self._llm,
                    scorers=["exact_match", "cosine_sim"],
                    use_best=False,
                )
                log.info("BlackBoxUQ ready (no-NLI mode)")
            except Exception as e2:
                log.error(f"BlackBoxUQ no-NLI fallback also failed: {e2}")
                self._blackbox = None
        return self._blackbox

    async def confidence(self, prompt: str) -> dict:
        """
        Quick confidence score via WhiteBoxUQ ($0 cost)

        Returns:
            {"score": 0-1, "response": str, "method": str, "details": {}}
        """
        if not self._initialized:
            return self._fallback(prompt)

        wb = await self._get_whitebox()
        if wb:
            try:
                results = await wb.generate_and_score(prompts=[prompt])
                df = results.to_df()
                if df is not None and len(df) > 0:
                    row = df.iloc[0]
                    seq_score = float(row.get("sequence_probability", 0.5))
                    # sequence_probability is length-normalized joint probability
                    # It's the most stable scorer across response lengths
                    score = min(1.0, max(0.0, seq_score))
                    resp = str(row.get("response", ""))
                    return {
                        "score": score,
                        "sequence_probability": seq_score,
                        "response": resp,
                        "method": "whitebox",
                        "details": row.to_dict() if hasattr(row, "to_dict") else {},
                    }
            except Exception as e:
                log.warning(f"WhiteBox failed: {e}")

        return self._fallback(prompt)

    async def deep_verify(self, prompt: str, num_responses: int = 3) -> dict:
        """
        Deep verification via BlackBoxUQ (Nx cost)

        Args:
            prompt: Input prompt
            num_responses: 3=low latency, 5=standard, 10=high precision

        Returns:
            {"score": 0-1, "best_response": str, "method": str, "details": {}}
        """
        if not self._initialized:
            return self._fallback(prompt)

        bb = await self._get_blackbox()
        if bb:
            try:
                results = await bb.generate_and_score(
                    prompts=[prompt], num_responses=num_responses
                )
                df = results.to_df()
                if df is not None and len(df) > 0:
                    row = df.iloc[0]
                    score = float(row.get("semantic_negentropy",
                                row.get("exact_match", 0.5)))
                    resp = str(row.get("response", ""))
                    return {
                        "score": min(1.0, max(0.0, score)),
                        "best_response": resp,
                        "method": f"blackbox_n{num_responses}",
                        "details": row.to_dict() if hasattr(row, "to_dict") else {},
                    }
            except Exception as e:
                log.warning(f"BlackBox deep verify failed: {e}")

        return self._fallback(prompt)

    def _fallback(self, prompt: str) -> dict:
        """Fallback: return neutral confidence (0.5)"""
        return {
            "score": 0.5,
            "response": "",
            "method": "fallback_heuristic",
            "details": {"note": "UQLM unavailable, neutral confidence"},
        }


# -- Test harness --
# To avoid NLI download hang, test whitebox only by default.
# Run deep_verify test separately.

def test_llm_connect():
    """Quick sync test: verify LLM connectivity"""
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="deepseek-v4-flash",
        api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
        base_url="https://api.deepseek.com/v1",
        temperature=0.3,
        max_tokens=100,
        logprobs=True,
        top_logprobs=5,
        timeout=30,
    )
    result = llm.invoke("Say hello")
    print(f"LLM response: {result.content[:100]}")
    print(f"Logprobs returned: {'response_metadata' in dir(result) or bool(getattr(result, 'response_metadata', {}))}")


async def test_whitebox():
    """Test whitebox mode ($0 cost)"""
    scorer = UQLMScorer(auto_init=True)
    if not scorer._initialized:
        print("[FAIL] LLM init failed")
        return False

    prompts = ["What is the capital of Malaysia?", "1+1=?", "Write a haiku."]
    print()
    print("=" * 60)
    print("  UQLM WhiteBox Test ($0 cost)")
    print("=" * 60)
    all_ok = True
    for p in prompts:
        print(f"\n  Prompt: {p}")
        r = await scorer.confidence(p)
        print(f"  Confidence: {r['score']:.4f}")
        print(f"  Method: {r['method']}")
        print(f"  Response: {r['response'][:80]}...")
        if r['method'] == 'whitebox':
            print("  [OK] WhiteBox working")
        else:
            print("  [WARN] Fallback used")
            all_ok = False

    print(f"\n  Result: {'ALL PASS' if all_ok else 'SOME FAILED'}")
    print("=" * 60)
    return all_ok


async def test_deep_verify():
    """Test deep verify mode (N=3, downloads NLI model on first call)"""
    scorer = UQLMScorer(auto_init=True)
    if not scorer._initialized:
        print("[FAIL] LLM init failed")
        return False

    print()
    print("=" * 60)
    print("  UQLM BlackBox Deep Verify Test (N=3)")
    print("  Note: First run downloads NLI model (~1.5GB)")
    print("=" * 60)

    r = await scorer.deep_verify("What is the capital of Malaysia?", num_responses=3)
    print(f"\n  Confidence: {r['score']:.4f}")
    print(f"  Method: {r['method']}")
    print(f"  Best response: {r['best_response'][:80]}...")
    ok = r['method'].startswith('blackbox')
    print(f"  Result: {'[OK]' if ok else '[WARN]'}")
    return ok


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--deep":
        asyncio.run(test_deep_verify())
    elif len(sys.argv) > 1 and sys.argv[1] == "--llm":
        test_llm_connect()
    else:
        asyncio.run(test_whitebox())
