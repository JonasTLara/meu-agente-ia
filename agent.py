from dotenv import load_dotenv
import anthropic
from tools import TOOL_DEFINITIONS, TOOL_FUNCTIONS

load_dotenv()
client = anthropic.Anthropic()

MODEL = "claude-sonnet-5-5"
MAX_STEPS = 10  # trava de segurança contra loops infinitos (e gastos)

SYSTEM_PROMPT = (
    "Você é um assistente pessoal prestativo. Responda em português do Brasil. "
    "Use as ferramentas disponíveis quando fizer sentido."
)


def run_agent(messages: list) -> None:
    """Roda o loop do agente imprimindo a resposta em streaming."""
    for _ in range(MAX_STEPS):
        # 1. Abre o stream e imprime cada pedaço de texto assim que chega
        with client.messages.stream(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)

            # 2. Quando o stream termina, pega a mensagem completa
            response = stream.get_final_message()

            print(
            f"\n  [uso] entrada: {response.usage.input_tokens} | "
            f"saída: {response.usage.output_tokens} tokens",
            end="",
            )

        # Guarda a resposta do modelo no histórico
        messages.append({"role": "assistant", "content": response.content})

        # Se não pediu ferramenta, é a resposta final
        if response.stop_reason != "tool_use":
            print()  # quebra de linha ao final
            return

        # Se chegou aqui, o modelo pediu ferramentas
        print()  # separa o texto parcial do log das ferramentas
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            print(f"  [ferramenta] {block.name}({block.input})")
            func = TOOL_FUNCTIONS.get(block.name)

            try:
                if func is None:
                    raise ValueError(f"Ferramenta desconhecida: {block.name}")
                output = func(**block.input)
                is_error = False
            except Exception as e:
                output = f"Erro ao executar a ferramenta: {e}"
                is_error = True

            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": output,
                "is_error": is_error,
            })

        # Devolve os resultados ao modelo e repete o loop
        messages.append({"role": "user", "content": results})

    print("\nAtingi o limite de passos sem concluir a tarefa.")


def main():
    messages = []
    print("Agente pronto! Digite 'sair' para encerrar.\n")
    while True:
        try:
            user_input = input("Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAté logo!")
            break

        if user_input.lower() in ("sair", "exit"):
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        print("Agente: ", end="", flush=True)
        run_agent(messages)
        print()


if __name__ == "__main__":
    main()