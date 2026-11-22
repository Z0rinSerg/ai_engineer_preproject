def main() -> None:
    print("Hello from ai-engineer-preproject!")


# Готовая функция чанкинга
def chunk_text(text: str, max_chars: int = 800, min_chars: int = 50) -> list[str]:
    """Режет Markdown по заголовкам ##; длинные секции дробит по параграфам.
    Параметры:
        text: исходный Markdown-текст
        max_chars: максимальная длина одного чанка в символах
        min_chars: минимальная длина чанка - чанки короче выбрасываются
    Возвращает:
        Список текстовых чанков
    """
    lines = text.split("\n")
    sections, current = [], []
    for line in lines:
        if line.startswith("## ") and current:
            sections.append("\n".join(current).strip())
            current = [line]
        else:
            current.append(line)
    if current:
        sections.append("\n".join(current).strip())

    chunks = []
    for section in sections:
        if not section:
            continue
        if len(section) <= max_chars:
            chunks.append(section)
            continue
        # Длинную секцию дробим по двойным переносам (параграфам)
        buf = ""
        for paragraph in section.split("\n\n"):
            if len(buf) + len(paragraph) + 2 <= max_chars:
                buf = f"{buf}\n\n{paragraph}" if buf else paragraph
            else:
                if buf:
                    chunks.append(buf.strip())
                buf = paragraph
        if buf:
            chunks.append(buf.strip())

    return [c for c in chunks if len(c) >= min_chars]