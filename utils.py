from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain


def get_chat_response(prompt, memory, openai_api_key):
    model = ChatOpenAI(model="gpt-5-nano", openai_api_key=openai_api_key)
    chain = ConversationChain(llm=model, memory=memory)
    response = chain.invoke({"input": prompt})
    return response["response"]
