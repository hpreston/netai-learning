# LMStudio as a Local AI Client
While most AI use cases and tooling involves using a "cloud based" AI model like ChatGPT, Claude, Gemini, etc, there are good reasons to have an option to run your AI models locally, right on your computer.  Some of the reasons I go this direction include: 

* Data security - Sometimes I want to keep my interactions with AI completely private. Even with paid accounts and corporate security evaluations and agreements, using "cloud based" models require that prompts and responses are handled remotely.
* Working "disconnected" - Not all systems and work environments have access to the Internet. Maybe it's an airgapped network, or perhaps you're just working from a plane with no or poor wifi. Local LLMs mean you are still able to leverage AI with your work. 
* Experiment with different models - Most AI services are tied to a specific "model". While ChatGPT lets you switch between different releases and versions of ChatGPT, you can't try Claude, Llama, or Gemini. Or maybe there's an open source model that you want to test out. 
* Buiding AI tools, agents, and applications - Cloud based AI offers provide API access, but there are often costs, limitations, or hoops to jump through. By running an LLM locally, you can do your development without the extra costs or challenges. And as a bonus, if you do it right, you can change between "local" and "cloud" LLMs with limited code changes.  

## What's cool about LM Studio? 
[LMStudio](https://lmstudio.ai/) is not the only way to run LLMs locally, and it's not the only way I run them locally.  But I've found it to be a really easy to use tool that allowed me to get started with lots of experimentation easily.  For me what stands out is: 

* It provides a nice GUI.  I don't mind CLI based software, but the user friendly nature of a GUI when getting started is very nice. 
* It can take advantage of the GPU on my laptop without any extra effort. This makes the LLM interactions much faster than CPU only options 
* It can act as an [MCP client](https://lmstudio.ai/docs/app/plugins/mcp) to leverage "tools" from servers.  
* It has [programmable interfaces](https://lmstudio.ai/docs/app/api) so I can write Python code that uses LMStudio as the LLM. This includes an ["OpenAI compatible" API](https://lmstudio.ai/docs/app/api/endpoints/openai).

> If you'd like to get started with LMStudio, checkout the tutorial [Run Your Own LLM Locally For Free and with Ease](https://u.cisco.com/tutorials/run-your-own-llm-locally-for-free-with-ease-26602) on [Cisco U](https://u.cisco.com)

## Model Suggestions
With the LMStudio "Discover" interface, you have access to open source models from all over the Internet. Some from big companies like Meta, Gemini, Microsoft, etc... others from individual users.  

I'd recommend being careful which models you download and work with.  While they will run locally on your laptop, custom models can be trained with incorrect information, bias, or other aspects that you don't want to work with.  

For my use cases, here are models that I've been working with: 

* [Meta-Llama-3.1-8B-Instruct(https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF)]
* [microsoft/phi-4-reasoning-plus](https://lmstudio.ai/models/microsoft/phi-4-reasoning-plus)
* [google/gemma-2-9b](https://lmstudio.ai/models/google/gemma-2-9b)
* [qwen/qwen3-4b](https://lmstudio.ai/models/qwen/qwen3-4b)

As you look at models for different use cases, consider these characteristics: 

* Is the model trained for tool use?  This will be important if you're experimenting with MCP servers
* Is it a "reasonsing model"? Reasoning models "think" and "reflect" on the prompts and questions asked. They are slower to respond, but they generally provide better answers.
* Was it tuned for specific use cases? Some models may have been fine tuned for particular use cases. A model tuned for "math problems" may not be a good choice for general purpose questions.