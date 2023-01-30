# ReplicateAI (WIP)
AI profle replication for twitter, instagram etc.
# Part 1 
Scrape the data of the person you want to replicate from the desired social media.
- This formats and exports the data into a format that the AI can train on (JSONL)
- For instagram the prompt is image alt text and the completions are captions

# Part 2 
Generate the content for the new profile using the fine-tuned AI
- For image generation, the prompt should be the captions it generates
- For text generation the prompt will be img alt text

# Part 3
Make a bot to auto upload the content.


