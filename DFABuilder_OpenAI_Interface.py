from openai import OpenAI

def makeRequest(request):
    client = OpenAI(api_key=getKey())
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a strictly mathematical model that outputs DFA definitions in a consistent single line with no formatting. For example, a DFA that accepts 'a' is defined as DFA = {{q0, q1}, {a}, {(0, a, 1)}, q0, {1}}."},{"role": "user", "content": request}],
    )
    return response.choices[0].message.content

def getKey():
    f = open("APIKey.txt", "r")
    return f.readline().strip()

def main():
    request = "AAA or BBB"
    print(makeRequest(request))

if __name__ == "__main__":
    main()