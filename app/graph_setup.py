from langgraph.graph import StateGraph, END

def build_graph():
    workflow = StateGraph(dict)

    def start_node(state):
        state["status"] = "ready"
        return state

    def ask_node(state):
        state["status"] = "asked"
        return state

    def answer_node(state):
        state["status"] = "answered"
        return state

    workflow.add_node("start", start_node)
    workflow.add_node("ask_question", ask_node)
    workflow.add_node("answer_question", answer_node)

    workflow.add_edge("start", "ask_question")
    workflow.add_edge("ask_question", "answer_question")
    workflow.add_edge("answer_question", END)

    workflow.set_entry_point("start")

    return workflow.compile()

graph = build_graph()
