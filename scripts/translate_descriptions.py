#!/usr/bin/env python3
"""
Batch translate description_en.txt to description_cn.txt

- If source text is English → uses Google Translate (free, fast)
- If source text is non-English (e.g. already Chinese) → uses LLM API
  (set NEVERSIGHT_API_KEY env var for LLM translation)

Usage:
    # Translate all missing Chinese descriptions
    python translate_descriptions.py
    
    # Only translate first 100 files (for testing)
    python translate_descriptions.py --limit 100
    
    # Start translation from file 200 (resume from checkpoint)
    python translate_descriptions.py --skip 200
    
    # Test mode
    python translate_descriptions.py --dry-run

    # Translate to Traditional Chinese (writes description_tw.txt by default)
    python translate_descriptions.py --target zh-TW

    # Translate to another language (writes description_<lang>.txt by default)
    python translate_descriptions.py --target ja

    # Fix "identical to en" (untranslated) files only (no overwrite of good translations)
    python translate_descriptions.py --target zh-TW --fix-identical
    python translate_descriptions.py --target ar --fix-identical
"""

import sys
import time
import argparse
from pathlib import Path
import os
import signal

# Base directory
BASE_DIR = Path(__file__).parent.parent / "data" / "skills-md"

_translator_cache: dict[tuple[str, str], object] = {}


def output_filename_for_target(target: str) -> str:
    """
    Decide output filename for a target language.

    Backward compatibility:
      - zh-CN -> description_cn.txt  (website expects this today)
      - zh-TW -> description_tw.txt
      - others -> description_<lang>.txt (sanitized)
    """
    t = (target or "").strip()
    t_norm = t.lower().replace("_", "-")
    if t_norm in {"zh-cn", "zh-hans", "zh-hans-cn"}:
        return "description_cn.txt"
    if t_norm in {"zh-tw", "zh-hant", "zh-hant-tw"}:
        return "description_tw.txt"
    safe = "".join(c if c.isalnum() or c in {"-", "_"} else "_" for c in t_norm).strip("_")
    safe = safe.replace("-", "_")
    return f"description_{safe or 'translated'}.txt"


def find_all_en_files() -> list[Path]:
    """Find all English description files that need translation.

    If the target translation file already exists (even if empty), we treat it as
    "already handled" to avoid overwriting manual edits.
    """
    en_files = []
    for en_file in BASE_DIR.rglob("description_en.txt"):
        out_file = en_file.parent / output_filename_for_target("zh-CN")
        # Only process files that don't have the default translation yet
        if not out_file.exists():
            en_files.append(en_file)
    return sorted(en_files)


def translate_with_google(text: str, source_lang: str, target_lang: str) -> str:
    """Translate using Google Translate (free)"""
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("Please install deep-translator: pip install deep-translator")
        sys.exit(1)
    
    key = (source_lang, target_lang)
    translator = _translator_cache.get(key)
    if translator is None:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        _translator_cache[key] = translator

    def _reset_translator() -> None:
        # In practice, Google Translate can temporarily block or return None.
        # Recreating the translator instance sometimes helps.
        _translator_cache.pop(key, None)
        _translator_cache[key] = GoogleTranslator(source=source_lang, target=target_lang)

    timeout_s = float(os.getenv("TRANSLATE_REQUEST_TIMEOUT_SECONDS", "20"))

    class _Timeout(Exception):
        pass

    def _alarm_handler(signum, frame):  # type: ignore[no-untyped-def]
        raise _Timeout(f"Translation request timed out after {timeout_s:.0f}s")

    old_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, _alarm_handler)

    # Add retry logic
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            signal.alarm(int(timeout_s))
            result = translator.translate(text)  # type: ignore[attr-defined]
            # deep-translator can occasionally return None on transient failures.
            if result is None:
                _reset_translator()
                raise RuntimeError("GoogleTranslator returned None")
            return str(result)
        except Exception as e:
            last_error = e
            if attempt < 2:
                _reset_translator()
                # Exponential-ish backoff. Allow overriding via env for local runs.
                base = float(os.getenv("TRANSLATE_RETRY_SLEEP_SECONDS", "3"))
                time.sleep(base * (attempt + 1))
            else:
                pass
        finally:
            signal.alarm(0)

    # Fallback: MyMemory (often works when Google blocks).
    try:
        from deep_translator import MyMemoryTranslator

        def _mm_lang(code: str) -> str:
            c = (code or "").strip().lower().replace("_", "-")
            if c in {"en", "en-us", "en-gb"}:
                return "english"
            if c in {"zh-cn", "zh-hans", "zh-hans-cn"}:
                return "chinese simplified"
            if c in {"zh-tw", "zh-hant", "zh-hant-tw"}:
                return "chinese traditional"
            if c == "es":
                return "spanish"
            if c == "fr":
                return "french"
            if c == "de":
                return "german"
            if c == "ja":
                return "japanese"
            if c == "ko":
                return "korean"
            return code

        mm = MyMemoryTranslator(source=_mm_lang(source_lang), target=_mm_lang(target_lang))
        signal.alarm(int(timeout_s))
        res = mm.translate(text)
        if res is None:
            raise RuntimeError("MyMemoryTranslator returned None")
        return str(res)
    except Exception as e:
        # Re-raise the last Google error if available; otherwise raise MyMemory error.
        if last_error is not None:
            raise last_error
        raise e
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


def is_english_text(text: str, threshold: float = 0.8) -> bool:
    """Return True if the text is primarily English (Latin alphabet).

    Counts only letter characters; if ≥ threshold fraction are ASCII letters,
    we treat the text as English and use Google Translate. Otherwise we fall
    back to the LLM which handles arbitrary source languages better.
    """
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return True  # no letters at all → treat as English (safe default)
    ascii_count = sum(1 for c in letters if ord(c) < 128)
    return (ascii_count / len(letters)) >= threshold


# Language code → human-readable name used in LLM prompts
_LLM_LANG_NAMES: dict[str, str] = {
    "zh-CN": "Simplified Chinese",
    "zh-TW": "Traditional Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "ru": "Russian",
    "ar": "Arabic",
    "pt": "Portuguese",
    "en": "English",
}


def translate_with_llm(text: str, target_lang: str) -> str:
    """Translate *text* to *target_lang* using the neversight LLM API.

    Requires the NEVERSIGHT_API_KEY environment variable.
    Used when the source text is not English (Google Translate produces poor
    results when the declared source language does not match the actual content).
    """
    try:
        import requests as _requests
    except ImportError:
        raise RuntimeError("Please install requests: pip install requests")

    api_key = os.getenv("NEVERSIGHT_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "NEVERSIGHT_API_KEY environment variable is not set. "
            "Cannot use LLM translation for non-English source text."
        )

    target_name = _LLM_LANG_NAMES.get(target_lang, target_lang)
    prompt = (
        f"Translate the following text to {target_name}. "
        "Output only the translated text with no extra explanations or comments:\n\n"
        f"{text}"
    )

    timeout_s = float(os.getenv("TRANSLATE_REQUEST_TIMEOUT_SECONDS", "60"))
    response = _requests.post(
        "https://api.neversight.dev/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "moonshotai/kimi-k2-latest",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=timeout_s,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def translate_with_mymemory(text: str, source_lang: str, target_lang: str) -> str:
    """Translate using MyMemory (fallback when Google returns wrong language)."""
    try:
        from deep_translator import MyMemoryTranslator
    except ImportError:
        raise RuntimeError("deep_translator required for MyMemory")
    c_map = {
        "en": "english", "zh-cn": "chinese simplified", "zh-tw": "chinese traditional",
        "es": "spanish", "fr": "french", "de": "german", "ja": "japanese", "ko": "korean",
        "it": "italian", "ru": "russian",
    }
    c = (source_lang or "").strip().lower().replace("_", "-")
    src = c_map.get(c, c)
    c = (target_lang or "").strip().lower().replace("_", "-")
    tgt = c_map.get(c, c)
    mm = MyMemoryTranslator(source=src, target=tgt)
    res = mm.translate(text)
    if res is None:
        raise RuntimeError("MyMemoryTranslator returned None")
    return str(res)


# ============= Main translation logic =============

def translate_file(
    en_file: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
    source_lang: str = "en",
    target_lang: str = "zh-CN",
) -> tuple[Path, bool, str]:
    """Translate a single file.

    Safety: if the output translation file already exists, we skip unless --force is provided.
    This prevents overwriting manually authored translations (or translations generated earlier).
    """
    try:
        out_name = output_filename_for_target(target_lang)
        out_file = en_file.parent / out_name
        if out_file.exists() and not force:
            return en_file, True, f"Skipped ({out_name} already exists)"

        # Read English content
        en_text = en_file.read_text(encoding="utf-8").strip()
        
        if not en_text:
            return en_file, False, "Empty file"

        # Path-like content: replace with a short translated phrase so target is no longer identical to en.
        if force and (en_text.strip().startswith((".", "/")) or (".." in en_text[:30] and "/" in en_text[:30])):
            placeholder_en = "See SKILL.md for full description."
            out_text = translate_with_google(placeholder_en, source_lang="en", target_lang=target_lang)
            if not dry_run:
                out_file.write_text(out_text + "\n", encoding="utf-8")
            return en_file, True, (out_text[:50] + "..." if len(out_text) > 50 else out_text)

        t_lang = target_lang.lower().strip().replace("_", "-")
        is_chinese_target = t_lang.startswith("zh")
        chinese_ratio = sum(1 for c in en_text if "\u4e00" <= c <= "\u9fff") / max(1, len(en_text))

        # ── Non-English source: fix description_en.txt first, then treat as English ─
        # If description_en.txt is actually in another language, translate it to English
        # and overwrite the file (same as fix_non_english_descriptions.py); then proceed
        # with normal Google translation to target.
        if not is_english_text(en_text):
            try:
                en_text = translate_with_llm(en_text, "en")
                if en_text is None:
                    raise RuntimeError("LLM returned None")
                en_text = str(en_text)
                if not dry_run:
                    en_file.write_text(en_text + "\n", encoding="utf-8")
            except Exception as e:
                return en_file, False, f"Fix en (LLM): {e}"
            chinese_ratio = sum(1 for c in en_text if "\u4e00" <= c <= "\u9fff") / max(1, len(en_text))

        # ── English source: use Google Translate (existing logic) ──────────────
        # If the "English" file is actually Chinese and target is Chinese: copy only when not force.
        # When force (fix-identical), always translate so that e.g. zh-CN -> zh-TW produces different (traditional) text.
        # When force and source is Chinese but target is ru/it/... use zh-CN as source so we get real translation.
        # When force and en is Japanese or Korean, use correct source so we don't get identical output.
        eff_source = source_lang
        if force and chinese_ratio > 0.3 and not is_chinese_target:
            eff_source = "zh-CN"
        if force and chinese_ratio <= 0.3:
            n = max(1, len(en_text))
            ja_ratio = sum(1 for c in en_text if "\u3040" <= c <= "\u30ff") / n
            ko_ratio = sum(1 for c in en_text if "\uac00" <= c <= "\ud7af") / n
            if ja_ratio > 0.1:
                eff_source = "ja"
            elif ko_ratio > 0.1:
                eff_source = "ko"
        if is_chinese_target and chinese_ratio > 0.3 and not force:
            out_text = en_text
        elif is_chinese_target and chinese_ratio > 0.3 and force and t_lang in {"zh-tw", "zh-hant", "zh-hant-tw"}:
            # If en is already Traditional Chinese, round-trip via zh-CN so we get different wording and break identical.
            if any(c in en_text for c in "當與會體來過為無時"):
                simplified = translate_with_google(en_text, source_lang="zh-TW", target_lang="zh-CN")
                out_text = translate_with_google(simplified, source_lang="zh-CN", target_lang="zh-TW")
            else:
                out_text = translate_with_google(en_text, source_lang="zh-CN", target_lang="zh-TW")
        elif is_chinese_target:
            out_text = translate_with_google(en_text, source_lang=eff_source, target_lang=target_lang)
        else:
            out_text = translate_with_google(en_text, source_lang=eff_source, target_lang=target_lang)
        if out_text is None:
            raise RuntimeError("Translation output is None")
        out_text = str(out_text)
        # When fixing identical: if source was Chinese but result still looks Chinese (e.g. Google returned original), try MyMemory.
        if force and not is_chinese_target and chinese_ratio > 0.3:
            out_cn = sum(1 for c in out_text if "\u4e00" <= c <= "\u9fff") / max(1, len(out_text))
            if out_cn > 0.3:
                try:
                    out_text = translate_with_mymemory(en_text, "zh-CN", target_lang)
                except Exception:
                    pass  # keep Google result if MyMemory fails
        # Write translated file
        if not dry_run:
            out_file.write_text(out_text + "\n", encoding="utf-8")
        
        return en_file, True, out_text[:50] + "..." if len(out_text) > 50 else out_text
        
    except Exception as e:
        return en_file, False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Batch translate description_en.txt to description_cn.txt (Google Translate)")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of files to translate (0 for all)")
    parser.add_argument("--skip", type=int, default=0, help="Skip first N files")
    parser.add_argument("--dry-run", action="store_true", help="Only show files to be translated, don't actually translate")
    parser.add_argument("--force", action="store_true", help="Force re-translate existing files")
    parser.add_argument("--fix-identical", action="store_true", help="Only re-translate files where target content starts identical to source (fix untranslated copies)")
    parser.add_argument("--source", type=str, default="en", help="Source language (default: en)")
    parser.add_argument("--target", type=str, default="zh-CN", help="Target language (default: zh-CN). Example: zh-TW, ja, ko")
    parser.add_argument("--sleep", type=float, default=float(os.getenv("TRANSLATE_SLEEP_SECONDS", "0.3")), help="Sleep seconds between files (default: 0.3, overridable via TRANSLATE_SLEEP_SECONDS)")
    
    args = parser.parse_args()
    
    # Find all files that need translation
    print("Scanning files...")
    
    out_name = output_filename_for_target(args.target)
    if args.fix_identical:
        # Only files where target exists and first 55 chars match source (untranslated copy).
        en_files = []
        for en_file in BASE_DIR.rglob("description_en.txt"):
            out_file = en_file.parent / out_name
            if not out_file.exists():
                continue
            try:
                en_t = en_file.read_text(encoding="utf-8").strip().replace("\n", " ")[:55]
                xx_t = out_file.read_text(encoding="utf-8").strip().replace("\n", " ")[:55]
            except Exception:
                continue
            if en_t.strip() and xx_t.strip() and en_t.strip() == xx_t.strip():
                en_files.append(en_file)
        en_files = sorted(en_files)
        args.force = True  # overwrite the identical (untranslated) content
    elif args.force:
        en_files = list(BASE_DIR.rglob("description_en.txt"))
        en_files = sorted(en_files)
    else:
        # In non-force mode, only translate missing files for the selected target.
        en_files = []
        for en_file in BASE_DIR.rglob("description_en.txt"):
            out_file = en_file.parent / out_name
            if not out_file.exists():
                en_files.append(en_file)
        en_files = sorted(en_files)
    
    # Apply skip and limit
    if args.skip > 0:
        en_files = en_files[args.skip:]
    if args.limit > 0:
        en_files = en_files[:args.limit]
    
    total = len(en_files)
    print(f"Found {total} files to translate")
    
    if total == 0:
        print("No files need translation")
        return
    
    if args.dry_run:
        print("\n[DRY RUN] The following files will be translated:")
        for f in en_files[:20]:
            print(f"  - {f.relative_to(BASE_DIR)}")
        if total > 20:
            print(f"  ... and {total - 20} more files")
        return
    
    # Start translation
    out_name = output_filename_for_target(args.target)
    print(f"\nStarting translation (English source → Google Translate; non-English source → LLM)...")
    print(f"Source: {args.source}  Target: {args.target}  Output: {out_name}")
    print("-" * 60)
    
    completed = 0
    failed = 0
    start_time = time.time()
    
    for en_file in en_files:
        en_file, success, message = translate_file(
            en_file,
            dry_run=args.dry_run,
            force=args.force,
            source_lang=args.source,
            target_lang=args.target,
        )
        completed += 1
        
        if success:
            print(f"[{completed}/{total}] ✓ {en_file.parent.name}: {message}")
        else:
            failed += 1
            print(f"[{completed}/{total}] ✗ {en_file.parent.name}: {message}")
        
        # Show progress
        if completed % 100 == 0:
            elapsed = time.time() - start_time
            rate = completed / elapsed
            remaining = (total - completed) / rate if rate > 0 else 0
            print(f"\n--- Progress: {completed}/{total} ({completed/total*100:.1f}%), "
                  f"Rate: {rate:.1f}/sec, Estimated remaining: {remaining/60:.1f} min ---\n")
        
        # Add delay to avoid rate limiting
        time.sleep(max(0.0, float(args.sleep)))
    
    # Final statistics
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"Translation completed!")
    print(f"  Success: {completed - failed}")
    print(f"  Failed: {failed}")
    print(f"  Time: {elapsed/60:.1f} min")
    print(f"  Rate: {completed/elapsed:.1f} files/sec")


if __name__ == "__main__":
    main()
