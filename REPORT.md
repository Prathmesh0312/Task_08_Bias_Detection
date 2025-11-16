1. Executive Summary
This project explores whether different language models give different answers when asked about the same cricket bowling data. The main idea was to see if the way a question is asked can influence the model’s interpretation, even when the data does not change. Three types of bias were tested: framing bias, confirmation bias, and nationality bias. For each one, we created a pair of prompts that were almost the same, with only one small change in wording. These prompts were then given to ChatGPT, Gemini, and DeepSeek.
Overall, the models showed noticeable differences in how they responded. When questions were framed in a negative way, the models focused more on poor performance or weaknesses. Neutral questions led to more balanced answers. When a prompt suggested that Indian bowlers performed well, the models often chose an Indian player, even in situations where another player had stronger statistics. This showed signs of confirmation bias. Nationality-related patterns also appeared, with Indian bowlers mentioned more often across several responses.
There were a few accuracy issues as well. Some models referred to players not present in the dataset, and at times they gave statistics that did not match the real numbers. These errors highlight the need to check model outputs carefully, especially when using them for data analysis.
In the end, the experiment showed that language models can be influenced by small changes in how a question is written. This affects which players they highlight, the tone they use, and even the facts they choose to mention. These results suggest that prompt design and verification steps are important when using LLMs to help analyze or summarize numerical data.


2. Methodology
This project uses a cricket bowling dataset containing overs, wickets, economy rate, and team information. The goal was to see how different LLMs respond to the same data when the questions are framed in different ways.
Three main types of bias were tested.
First, framing bias: how models change their answer when the question sounds positive or negative.
Second, confirmation bias: whether a model agrees with a hint or assumption in the prompt.
Third, nationality influence: whether mentioning a specific team changes which players the model talks about.
For each bias type, two prompts were written. One was neutral, and the other changed only a few words to shift the focus. For example, “Which bowler performed best?” vs “Which bowler is struggling?” This kept the experiment controlled, since the only difference between the prompts was the wording.
Three models were used: ChatGPT, Gemini, and DeepSeek. Each model answered all six prompts. Because free API limits blocked automation, the responses were recorded manually in CSV files. Each entry included the timestamp, model name, hypothesis, prompt type, and the model’s answer.
For analysis, Python scripts were used. One script measured the sentiment of each response and counted how often each bowler or team was mentioned. Another script checked the answers for accuracy by comparing them with the real values in the dataset. This helped identify hallucinated names or incorrect statistics. A Jupyter notebook was used to create visual charts like bar graphs and heatmaps so the differences were easy to see.
Overall, this method made it possible to compare how each model reacted to small changes in the questions, while keeping the data and structure consistent across all tests.


3. Results
Across all models, the wording of the prompt clearly affected the responses. When the question used negative language, the answers also became more negative. For positive or neutral prompts, the models focused more on strengths or general patterns.
When we added the assumption that Indian bowlers performed best, the models shifted toward choosing Indian players, even in cases where other bowlers had stronger statistics. This showed a pattern of confirmation bias.
We also saw nationality effects. Indian bowlers were mentioned more than expected compared to players from New Zealand or South Africa. This happened even when the neutral prompts did not mention nationality.
A few hallucinations appeared. Some models mentioned players who were not in the dataset. There were also smaller errors, such as slight differences in economy rates or wicket counts.
The graphs helped show clear differences in tone, player mentions, and how strongly each model reacted to prompt framing.


4. Bias Catalogue
Framing bias
Models became more negative when the prompt used negative wording.
Seen in all three models.

Confirmation bias
When told that Indian bowlers dominated, models picked Indian players more often.
Strongest in Gemini.

Nationality bias
Indian bowlers are mentioned more frequently across prompts.
Mild but consistent.

Hallucinations
Some players were mentioned who did not exist in the dataset.
Occasionally across models.

Stat mistakes
Some economy or wicket numbers were inaccurate or missing.
Mostly small errors.

5. Mitigation Strategies
Start prompts with phrases like “Based only on the data provided” to limit drift.
Avoid giving assumptions in the prompt unless needed.
Provide the data in table form so the model has clear structure to follow.
Run the same prompt through more than one model and compare answers.
Keep temperature low so the model responds more consistently.
Use a validation step to check for hallucinations or wrong numbers.
Add rules such as “Only use names from this list of players.”

6. Limitations
The experiment had a small sample size because free models have strict limits. We only tested three types of bias, so there may be other forms that were not covered. The dataset is focused on cricket, so results may not fully apply to other fields. Some of the analysis steps were manual, which might introduce minor human error. Sentiment tools can also misread very short answers. Lastly, LLMs change quickly, so results may not stay the same with future versions of these models.
