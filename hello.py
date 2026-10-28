from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()  # lê ANTHROPIC_API_KEY do .env

resposta = client.messages.create(
    model="claude-haiku-5-5",  # modelo barato, bom para testes
    max_tokens=300,
    messages=[{"role": "user", "content": "Explique o que é um agente de IA em 2 frases."}],
)

print(resposta.content[0].text)