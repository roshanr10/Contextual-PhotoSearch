from langchain import PromptTemplate, LLMChain
from langchain.llms import Cohere
from search import query, print_result

llm = Cohere(cohere_api_key="<COHERE API KEY>", temperature=0)
llm_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(
        "Come up with a list of potential image search queries based on this initial query: {query}"
    )
)

if __name__ == '__main__':
    print_result(query(llm_chain("people hanging out at a bar")["text"]))
    print_result(query(llm_chain("playing pool")["text"]))
    print_result(query(llm_chain("phone app demo at social mixer")["text"]))
