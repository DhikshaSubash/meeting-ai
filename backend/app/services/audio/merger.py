def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS format."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def merge_transcript_with_speakers(
    whisper_segments: list[dict],
    diarization_segments: list[dict]
) -> list[dict]:
    """
    Match each Whisper text segment to the most overlapping diarization speaker.
    Returns merged segments with speaker labels + text.
    """
    merged = []

    for w_seg in whisper_segments:
        w_start = w_seg["start"]
        w_end   = w_seg["end"]
        w_text  = w_seg["text"].strip()

        if not w_text:
            continue

        # Find best matching speaker by overlap
        best_speaker = "UNKNOWN"
        best_overlap = 0.0

        for d_seg in diarization_segments:
            d_start = d_seg["start"]
            d_end   = d_seg["end"]

            # Calculate overlap between whisper segment and diarization segment
            overlap_start = max(w_start, d_start)
            overlap_end   = min(w_end,   d_end)
            overlap       = max(0.0, overlap_end - overlap_start)

            if overlap > best_overlap:
                best_overlap = overlap
                best_speaker = d_seg["speaker"]

        merged.append({
            "start":     w_start,
            "end":       w_end,
            "timestamp": format_timestamp(w_start),
            "speaker":   best_speaker,
            "text":      w_text,
        })

    return merged


def clean_text(text: str) -> str:
    """
    Remove filler words and clean up transcript text.
    """
    import re

    fillers = [
        r"\buh\b", r"\bum\b", r"\bhmm\b", r"\blike\b",
        r"\byou know\b", r"\bkind of\b", r"\bsort of\b",
        r"\bbasically\b", r"\bactually\b", r"\bright\b",
        r"\bokay so\b", r"\bso yeah\b",
    ]

    for filler in fillers:
        text = re.sub(filler, "", text, flags=re.IGNORECASE)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Capitalize first letter
    if text:
        text = text[0].upper() + text[1:]

    return text


def build_readable_transcript(merged_segments: list[dict]) -> str:
    """
    Build a human-readable transcript string.
    """
    lines = []
    for seg in merged_segments:
        lines.append(f"[{seg['timestamp']}] {seg['speaker']}: {seg['text']}")
    return "\n".join(lines)