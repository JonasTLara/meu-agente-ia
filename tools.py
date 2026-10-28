from datetime import datetime
from pathlib import Path

NOTES_FILE = Path("notes.txt")


# --- Funções reais ---
def get_current_time() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def save_note(text: str) -> str:
    with NOTES_FILE.open("a", encoding="utf-8") as f:
        f.write(text + "\n")
    return "Nota salva com sucesso."


def read_notes() -> str:
    if not NOTES_FILE.exists():
        return "Nenhuma nota salva ainda."
    return NOTES_FILE.read_text(encoding="utf-8")


# --- Descrições para o modelo ---
TOOL_DEFINITIONS = [
    {
        "name": "get_current_time",
        "description": "Retorna a data e hora atuais. Use quando o usuário perguntar a hora ou data.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "save_note",
        "description": "Salva uma nota de texto para o usuário. Use quando ele pedir para anotar ou lembrar algo.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "O texto da nota a ser salva."}
            },
            "required": ["text"],
        },
    },
    {
        "name": "read_notes",
        "description": "Lê todas as notas salvas. Use quando o usuário quiser ver ou buscar suas anotações.",
        "input_schema": {"type": "object", "properties": {}},
    },
]

# --- Mapa nome -> função (para o loop encontrar o que executar) ---
TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "save_note": save_note,
    "read_notes": read_notes,
}