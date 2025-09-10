from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import StrOutputParser

### System prompt ###
template = '''### SYSTEM ###
{system}

### TASK ###
{task}

answer in the following mood: {mood}
answer in this language: {language}
'''

### Invoke AI ###
def invoke_ai(system, task, mood, language, temperature, model):
    llm = OllamaLLM(
        model=model,
        temperature=temperature,
    )

    ### Prompt ###
    prompt = PromptTemplate(
        input_variables=['system', 'task', 'mood'],
        template=template
    )
    
    ### Output Parser ###
    output_parser = StrOutputParser()

    ### Chain ###
    chain = prompt | llm | output_parser
    response = chain.invoke(
        {
            'system': system,
            'task': task,
            'mood': mood,
            'language': language
        }
    )
    return response