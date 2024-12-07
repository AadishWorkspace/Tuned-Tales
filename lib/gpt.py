import openai

# Function to get GPT response for a given prompt
def get_gpt_response(prompt, stream_output=False, output_function=None, model='gpt-3.5-turbo', temperature=0):
    # Internal function to handle output
    def _output_function(message):
        output_function(message) if output_function else print(message, end='')

    # Create GPT response
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        stream=stream_output
    )

    # Handle streaming output
    if stream_output:
        complete_message = ''
        for chunk in response:
            content = chunk.choices[0].delta.get("content", '')
            _output_function(content)
            complete_message += content
        return complete_message

    return response.choices[0].message.content

# Function to get GPT chat response for a list of messages
def get_gpt_chat_response(messages, stream_output=False, output_function=None, model='gpt-3.5-turbo', temperature=0):
    # Internal function to handle output
    def _output_function(message):
        output_function(message) if output_function else print(message, end='')

    # Create GPT chat response
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream=stream_output
    )

    # Handle streaming output
    if stream_output:
        complete_message = ''
        for chunk in response:
            content = chunk.choices[0].delta.get("content", '')
            _output_function(content)
            complete_message += content
        return complete_message

    return response.choices[0].message.content