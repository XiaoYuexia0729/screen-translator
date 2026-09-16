"""
Optimized translation utility with caching and faster response
"""
import sys
import time

# Ensure UTF-8 encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Simple in-memory cache for recent translations
_translation_cache = {}
_cache_max_size = 100

def translate_text_cached(text, source='en', target='zh-CN'):
    """
    Translate with caching to speed up repeated text
    """
    cache_key = f"{text}_{source}_{target}"

    # Check cache first
    if cache_key in _translation_cache:
        return _translation_cache[cache_key]

    # Translate
    result = translate_text(text, source, target)

    # Store in cache
    if len(_translation_cache) >= _cache_max_size:
        # Remove oldest entry
        _translation_cache.pop(next(iter(_translation_cache)))
    _translation_cache[cache_key] = result

    return result


def translate_text(text, source='auto', target='zh-CN'):
    """
    Translate text using available services (prioritize fastest and most reliable)
    """
    if not text or not text.strip():
        return ""

    text = text.strip()

    # Method 1: Try translators library with Bing (most reliable for Chinese)
    try:
        import translators as ts
        result = ts.translate_text(
            query_text=text,
            translator='bing',
            from_language=source,
            to_language='zh',
            timeout=5
        )
        if result and isinstance(result, str) and len(result) > 0:
            return result
    except Exception as e:
        pass

    # Method 2: Try translators with Google
    try:
        import translators as ts
        result = ts.translate_text(
            query_text=text,
            translator='google',
            from_language=source,
            to_language='zh-CN',
            timeout=5
        )
        if result and isinstance(result, str) and len(result) > 0:
            return result
    except Exception as e:
        pass

    # Method 3: Try deep_translator with Google
    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source='auto', target='zh-CN')
        result = translator.translate(text)
        if result and isinstance(result, str) and len(result) > 0:
            return result
    except Exception as e:
        pass

    # Method 4: Try translators with Alibaba
    try:
        import translators as ts
        result = ts.translate_text(
            query_text=text,
            translator='alibaba',
            from_language=source,
            to_language='zh',
            timeout=5
        )
        if result and isinstance(result, str) and len(result) > 0:
            return result
    except Exception as e:
        pass

    # Method 5: Try translators with Baidu
    try:
        import translators as ts
        result = ts.translate_text(
            query_text=text,
            translator='baidu',
            from_language=source,
            to_language='zh',
            timeout=5
        )
        if result and isinstance(result, str) and len(result) > 0:
            return result
    except Exception as e:
        pass

    # All methods failed
    return "[翻译服务暂时不可用]"


if __name__ == '__main__':
    # Test translation
    test_texts = [
        "Hello World",
        "How are you?",
        "This is a test",
        "Machine Learning"
    ]

    print("Testing translation services...\n")
    for test_text in test_texts:
        result = translate_text(test_text)
        print(f"EN: {test_text}")
        print(f"ZH: {result}")
        print()
