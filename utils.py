from langchain_core.messages import HumanMessage, AIMessage

def serialize_message(message):
    return {
        'type': type(message).__name__,
        'content': message.content
    }

def deserialize_message(message_dict):
    if message_dict['type'] == 'HumanMessage':
        return HumanMessage(content=message_dict['content'])
    elif message_dict['type'] == 'AIMessage':
        return AIMessage(content=message_dict['content'])
    else:
        raise ValueError(f"Unknown message type: {message_dict['type']}")
