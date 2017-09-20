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
    import subprocess
    result = getConversationResponse('Tell me a joke')
    subprocess.Popen(["python", "watson_tts.py", result.get("output", {}).get("text", [""])[0], 'en-US_AllisonVoice'] , stdout=subprocess.PIPE)
    
