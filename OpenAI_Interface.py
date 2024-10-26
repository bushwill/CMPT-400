from openai import OpenAI
client = OpenAI(
    api_key='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',
)

def makeRequest(request):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a strictly mathematical model that outputs DFA definitions in a consistent single line with no formatting. For example, a DFA that accepts 'a' is defined as DFA = {{q0, q1}, {a}, {(0, a, 1)}, q0, {1}}."},{"role": "user", "content": request}],
    )
    return response.choices[0].message.content