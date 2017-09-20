import json
from watson_developer_cloud import ConversationV1
from constants import conversation_creds

conversation = ConversationV1(
  username=conversation_creds.get("username"),
  password=conversation_creds.get("password"),
  version=conversation_creds.get("version")
)

workspace = conversation_creds.get("workspace")

def getConversationResponse(query):
    context = {}
    response = conversation.message(
      workspace_id=workspace,
      message_input={'text': query},
      context=context
    )
    return response

if __name__ == '__main__':
    getConversationResponse('Can you play Attention from Shawn Mendes')
