from openai import OpenAI

def makeRequest(request, model = 'gpt-4o-mini'):
    client = OpenAI(api_key=getKey())
    
    gpt_description = "You are a strictly mathematical model that outputs DFA definitions in a consistent single line with no formatting. For example, a DFA that accepts 'a' is defined as DFA = {{q0, q1}, {a}, {(0, a, 1)}, q0, {1}}. Final states must be integer indices of states. Here are some positive examples from a language: "
    
    response = client.chat.completions.create(
        model = model,
        messages=[{"role": "user", "content": gpt_description + request}],
    )
    return response.choices[0].message.content

def getKey():
    f = open("APIKey.txt", "r")
    return f.readline().strip()

def main():
    request = "AAA, BBB"
    print(makeRequest(request))

if __name__ == "__main__":
    main()